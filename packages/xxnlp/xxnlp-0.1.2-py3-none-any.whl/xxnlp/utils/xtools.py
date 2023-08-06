from typing import Union, Dict, List, Callable, Any, Iterable, Mapping
from collections import OrderedDict, defaultdict
from xxnlp.model import seq_len_to_mask
from itertools import zip_longest
import torch, numpy as np

__all__ = ['xtable', 'xlen', 'xpad', 'xmove', 'xrank', 'xgroup']



    
def xtable(
    dicts: List[Dict], 
    keys: List[str] = None, 
    pads: List[str] = None, 
    fcodes: List[str] = None, 
    convert_headers: Dict[str, Callable] = None, 
    header_names: List[str] = None, 
    skip_none_lines: bool = False, 
    skip_head_lines: bool = False,
    replace_values: Dict[str, Any] = None, index: List[str] = None
):
    """ Generate ascii table from dictionary
        Copyright: https://stackoverflow.com/questions/40056747/print-a-list-of-dictionaries-in-table-form
    dicts: input dictionary list; empty lists make keys OR header_names mandatory
    keys: order list of keys to generate columns for; no key/dict-key should suffix with '____' else adjust code-suffix
    pads: indicate padding direction and size, eg <10 to right pad alias left-align
    fcodes: formating codes for respective column type, eg .3f
    convert_headers: apply converters(dict) on column keys k, eg timestamps
    header_names: supply for custom column headers instead of keys
    skip_none_lines: skip line if contains None
    replace_values: specify per column keys k a map from seen value to new value;
                    new value must comply with the columns fcode; CAUTION: modifies input (due speed)
    """
    # optional arg prelude
    def infer_type(v):
        if isinstance(v, float): return ('.4f', '>8') 
        elif isinstance(v, int): return ('d', '>6')
        else: return ('s', '<8')
    if index is not None:
        dicts = [{'index': y, **x} for x,y in zip(dicts, index)]
    if keys is None:
        if len(dicts) > 0:
            keys = dicts[0].keys()
        elif header_names is not None:
            keys = header_names
        else:
            raise ValueError('keys or header_names mandatory on empty input list')
    if pads is None  and fcodes is None:
        fcodes, pads = zip(*map(infer_type, dicts[0].values()))
    N_keys, N_pads, N_codes = len(keys), len(pads), len(fcodes)
    if N_pads != N_keys:
        raise ValueError(f'bad pad length {len(pads)}, expected: {N_keys}')
    elif N_codes != N_keys:
        raise ValueError(f'bad fcodes length {len(fcodes)}, expected: {N_keys}')
    if convert_headers is None: convert_headers = {}
    if header_names is None: header_names = keys
    if replace_values is None: replace_values = {}
    # build header
    headline = '│'.join(f"{v:{pad}}" for v, pad in zip_longest(header_names, pads))
    underline = '─' * len(headline)
    # suffix special keys to apply converters to later on
    marked_keys = [h + '____' if h in convert_headers else h for h in keys]
    marked_values = {}
    s = '│'.join(f"{{{h}:{pad}{fcode}}}" for h, pad, fcode in zip_longest(marked_keys, pads, fcodes))
    if skip_head_lines:
        lines = []
    else:
        lines = [headline, underline, ]
    for d in dicts:
        none_keys = [k for k, v in d.items() if v is None]
        if skip_none_lines and none_keys:
            continue
        elif replace_values:
            for k in d.keys():
                if k in replace_values and d[k] in replace_values[k]:
                    d[k] = replace_values[k][d[k]]
                if d[k] is None:
                    raise ValueError(f"bad or no mapping for key '{k}' is None. Use skip or change replace mapping.")
        elif none_keys:
            raise ValueError(f'keys {none_keys} are None in {d}. Do skip or use replace mapping.')
        for h in convert_headers:
            if h in keys:
                converter = convert_headers[h]
                marked_values[h + '____'] = converter(d)
        line = s.format(**d, **marked_values)
        lines.append(line)
    return '\n'.join(lines)

def _isnested(arr):
    """whether `arr` is nested iterable object
    >>> _isnested([1,2,3]) #should be False
    """
    try:
        return any(len(x) > 1 for x in arr)
    except TypeError:
        return False
    
def xlen(arr):
    """infer shape of nested list
    >>> lst = [[1,], [2,3], [2]]
    >>> xlen(lst) # [3,2]
    """
    if isinstance(arr, str) or not isinstance(arr, Iterable) or not _isnested(arr):
        return len(arr)
    carr = [xlen(x) for x in arr]    
    if not _isnested(carr):
        return [len(arr), max(carr)]
    else:
        return [len(arr)] + list(map(max, zip_longest(*carr, fillvalue=0)))

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
        else: 
            shape = xlen(arr)
    out = helper(arr, *shape)
    if rtn_type == 'tensor':
        return torch.from_numpy(out)
    return out

def xmove(args, device):
    if not torch.cuda.is_available() or device is None:
        return
    if isinstance(args, list):
        for arg in args: xmove(arg, device)
    elif isinstance(args, Mapping):
        for key, value in args.items():
            if isinstance(value, torch.Tensor):
                args[key] = value.to(device)
    else:
        raise TypeError("only dictionary inputs are supported, please change your collate function")

def xrank(tensor, dim=0, topk=0, mode='max', pad=0., seq_len=None):
    """
    """
    if mode == 'max':
        try:
            attn, idx = tensor.max(dim=dim)
        except IndexError:
            pass
        largest, invalid =True, float('-inf')
    else:
        attn, idx = tensor.min(dim=dim)
        largest, invalid =False, float('inf')
    if topk <= 0 or attn.size(-1) <= topk: 
        return attn, idx
    if seq_len is not None:
        mask = seq_len_to_mask(seq_len) 
        attn.masked_fill_(~mask, invalid)
    else:
        mask = torch.ones_like(attn).bool()
    _, i = attn.topk(topk, largest=largest, dim=-1)
    attn.masked_fill_(mask.scatter(-1,i,False), pad)
    return attn, i
    

def xgroup(iterable, ndigits=None):
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