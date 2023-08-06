import torch, inspect
import torch.nn as nn
import numpy as np, functools
from torch.nn.utils import rnn
from functools import reduce
from fastNLP.embeddings.torch.utils import get_embeddings, get_sinusoid_encoding_table
from typing import List, Dict

def make_optim_helper(module, **lr_settings):
    # input: backbone.alpha
    all_param = {k: p for k,p in module.named_parameters() if p.requires_grad==True}
    lr_paramd = []
    for module_name, lr in lr_settings.items():
        params = [p for k,p in all_param.items() if k.startswith(module_name)]
        all_param = {k: v for k,v in all_param.items() if not k.startswith(module_name)}
        lr_paramd.append({'params': params, 'lr': lr, 'name': module_name})
    lr_paramd.append({'params': [p for k, p in all_param.items()], 'name': 'rest'})
    return lr_paramd

def make_optim(model, lr, optim_name='AdamW', add_lr={}, weight_decay=1e-2):
    if optim_name == 'Adam':
        optim = torch.optim.Adam
    elif optim_name == 'SGD':
        optim = functools.partial(torch.optim.SGD, momentum=0.9, weight_decay=0)
    elif optim_name == 'AdamW':
        optim = torch.optim.AdamW
    else:
        raise ValueError('optim not defined')
    # scheduler = torch.optim.lr_scheduler.StepLR(optim, step_size=30, gamma=0.1)
    return optim(make_optim_helper(model, **add_lr), lr=lr)

def get_pos_embed(embed_type, max_position, embed_dim):
    if embed_type == 'sin':
        return nn.Embedding.from_pretrained(
            get_sinusoid_encoding_table(max_position + 1, embed_dim, padding_idx=0),
            freeze=True) 
    elif embed_type == 'learned':
        return get_embeddings((max_position + 1, embed_dim), padding_idx=0)
    else:
        return None


def tween(lst, item, add_last=False):
    """
    >>> a, b = [1,2,3], ['#','$']
    >>> tween(a,b)
    [1, '#', '$', 2, '#', '$', 3]
    >>> tween(a,b,True)
    [1, '#', '$', 2, '#', '$', 3, '#', '$']
    """
    if not isinstance(item, list):
        item = [item]
    if add_last:
        return reduce(lambda r,v: r+[v]+item, lst, [])
    else:
        return reduce(lambda r,v: r+item+[v], lst[1:], lst[:1])

def build_args(func, **kwargs):
    spect = inspect.getfullargspec(func)
    if spect.varkw is not None: 
        return kwargs
    needed_args = set(spect.args)
    if spect.defaults is not None:
        defaults = [arg for arg in spect.defaults]
    else:
        defaults = []
    start_idx = len(spect.args) - len(defaults)
    output = {name: default for name, default in zip(spect.args[start_idx:], defaults)}
    output.update({name: val for name, val in kwargs.items() if name in needed_args})
    return output

def match_args(func, *args, **kwargs) -> dict:
    spect = inspect.signature(func)
    parameters = spect.parameters
    parameters = {
        k:v for k,v in spect.parameters.items() if k not in ('self', 'kwargs')
    }
    spect._parameters = parameters
    args = (*args, *kwargs.pop('args', ()))
    kwargs = {k: v for k,v in kwargs.items() if k in parameters}
    args = spect.bind_partial(*args, **kwargs)
    args.apply_defaults()
    return dict(args.arguments)

class xpack:

    def __init__(self, data, length, batch_first=True, enforce_sorted=False):
        if length.is_cuda: length = length.cpu()
        self.length = length
        self.data, self.batch_sizes, self.sorted_indices, self.unsorted_indices = rnn.pack_padded_sequence(data, length, batch_first=batch_first, enforce_sorted=enforce_sorted)
        self.extra = {}   # to help memorizing other stuff
    
    @property
    def sequence(self):
        return rnn.PackedSequence(
            data=self.data, batch_sizes=self.batch_sizes,
            sorted_indices=self.sorted_indices, unsorted_indices=self.unsorted_indices
        )
    
    def pad(self, data=None, batch_first=True, padding_value=0, total_length=None, **kwargs):
        if data is None: data = self.data
        if not isinstance(data, rnn.PackedSequence):
            batch_sizes = kwargs.get('batch_sizes', self.batch_sizes)
            sorted_indices = kwargs.get('sorted_indices', self.sorted_indices)
            unsorted_indices = kwargs.get('unsorted_indices', self.unsorted_indices)
            data = rnn.PackedSequence(
                data, batch_sizes, sorted_indices, unsorted_indices
            )
        rtn, _ = rnn.pad_packed_sequence(
            data, batch_first=batch_first, padding_value=padding_value, total_length=total_length
        )
        return rtn

    def pack(self, data, batch_first=True, enforce_sorted=False, return_sequence=False):
        seq =  rnn.pack_padded_sequence(data, self.length, batch_first=batch_first, enforce_sorted=enforce_sorted)
        return seq if return_sequence else seq.data

    def repeat(self, data):
        idx = torch.cat([self.sorted_indices[:i] for i in self.batch_sizes])
        if not isinstance(data, torch.Tensor):
            idx = idx.cpu().numpy()
        return data[idx]
    
    def np_pack(self, data):
        idx, size = self.sorted_indices.cpu().numpy(), self.batch_sizes.numpy()
        rtn = []
        for i, size in enumerate(self.batch_sizes):
            rtn.extend(data[idx[:size],i])
        return np.array(rtn)

class Model(nn.Module):

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance._init_params_d = match_args(instance.__init__, *args, **kwargs)
        return instance

    @property
    def init_parms_d(self):
        return self._init_params_d

    @classmethod
    def restore_from_checkpoint(cls, checkpoint):
        try:
            ckpt = torch.load(checkpoint)
            model = cls(**ckpt['init_params'])
            model.load_state_dict(ckpt['state_dict'], strict=False)
            return model
        except OSError: 
            pass # start training from scratch
    
    def save_to_checkpoint(self, ckpt_fp, **metadata):
        torch.save({
            'metadata': metadata,
            'state_dict': self.state_dict(),
            'init_params': self.init_parms_d
        }, ckpt_fp)

    def forward(self, **kwargs):
        """return output"""
        raise NotImplementedError
    
    def train_step(self, x, y):
        pred = self(x)
        return {"loss": self.loss_fn(pred, y)}

    def evaluate_step(self, x, y):
        pred = self(x)
        pred = torch.max(pred, dim=-1)[1]
        return {"pred": pred, "target": y}
    
    

    
def seq_len_to_mask(seq_len, max_len=None):
    """
    >>> size = torch.randint(3, 10, (3,)) # e.g., [3,6,6]
    >>> seq_len_to_mask(size).shape == torch.Size([3,size.max()])
    True
    >>> seq_len_to_mask(size, 10).shape   # True/False matrix
    torch.Size([3, 10])
    """
    if isinstance(seq_len, np.ndarray):
        assert len(np.shape(seq_len)) == 1, f"seq_len can only have one dimension, got {len(np.shape(seq_len))}."
        max_len = int(max_len) if max_len else int(seq_len.max())
        broad_cast_seq_len = np.tile(np.arange(max_len), (len(seq_len), 1))
        mask = broad_cast_seq_len < seq_len.reshape(-1, 1)

    elif isinstance(seq_len, torch.Tensor):
        assert seq_len.dim() == 1, f"seq_len can only have one dimension, got {seq_len.dim() == 1}."
        batch_size = seq_len.size(0)
        max_len = int(max_len) if max_len else seq_len.max().long()
        broad_cast_seq_len = torch.arange(max_len).expand(batch_size, -1).to(seq_len)
        mask = broad_cast_seq_len.lt(seq_len.unsqueeze(1))
        
    else:
        raise TypeError("Only support 1-d numpy.ndarray or 1-d torch.Tensor.")

    return mask

    
def xpad(arr, *shape, pad_value=0, dtype=float, rtn_type='numpy'):
    def helper(arr, *shape):
        if not shape: return 
        if len(shape) == 1: return np.array(arr, dtype=dtype)
        _arr = np.full(shape, fill_value=pad_value, dtype=dtype)
        for i, x in enumerate(arr):
            if isinstance(x, np.ndarray):
                size = min(shape[1], len(x))
                _arr[i, :size] = x[:size]
            else:
                rtn = helper(x, *shape[1:])
                _arr[i, :len(rtn)] = rtn
        return _arr
    if not shape:
        if hasattr(arr, 'shape'): shape = arr.shape
        else: shape = [len(arr)]
    out = helper(arr, *shape)
    if rtn_type == 'tensor':
        return torch.from_numpy(out)
    return out

def xmove(args, device):
    if not torch.cuda.is_available() or device is None:
        return
    if isinstance(args, list):
        for arg in args: xmove(arg, device)
    elif isinstance(args, dict):
        for key, value in args.items():
            if isinstance(value, torch.Tensor):
                args[key] = value.to(device)
    else:
        raise TypeError("only dictionary inputs are supported, please change your collate function")

def xgroup(iterable, ndigits=None):
    from collections import defaultdict
    def rd(num, digit=None):
        if digit: num = round(num, digit)
        return num
    out = defaultdict(dict)
    for key in iterable:
        if '|' in key:
            left,right = key.rsplit('|',1)
            out[right][left] = rd(iterable[key], ndigits)
            if '|' in left:
                out[right] = xgroup(out[right])
        else:
            out[key] = rd(iterable[key], ndigits)
    return out