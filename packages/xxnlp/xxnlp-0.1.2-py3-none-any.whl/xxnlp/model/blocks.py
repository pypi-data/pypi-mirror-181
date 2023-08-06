import torch
import torch.nn as nn
from typing import List, Dict, Tuple


def make_fc(input_dim, hidden_sizes):
    r"""Returns a ModuleList of fully connected layers. 
    
    .. note::
    
        All submodules can be automatically tracked because it uses nn.ModuleList. One can
        use this function to generate parameters in :class:`BaseNetwork`. 
    
    Example::
    
        >>> make_fc(3, [4, 5, 6])
        ModuleList(
          (0): Linear(in_features=3, out_features=4, bias=True)
          (1): Linear(in_features=4, out_features=5, bias=True)
          (2): Linear(in_features=5, out_features=6, bias=True)
        )
    
    Args:
        input_dim (int): input dimension in the first fully connected layer. 
        hidden_sizes (list): a list of hidden sizes, each for one fully connected layer. 
    
    Returns:
        nn.ModuleList: A ModuleList of fully connected layers.     
    """
    assert isinstance(hidden_sizes, list), f'expected list, got {type(hidden_sizes)}'
    
    hidden_sizes = [input_dim] + hidden_sizes
    
    fc = []
    for in_features, out_features in zip(hidden_sizes[:-1], hidden_sizes[1:]):
        fc.append(nn.Linear(in_features=in_features, out_features=out_features))
    
    fc = nn.ModuleList(fc)
    
    return fc

def make_dnn(input_dim: int, hidden_sizes: List[int], hidden_units: List[str] = 'relu', dropouts: List[float] = 0.0, bias=True, init_weight=True, last_act=False):
    return DNN(
        input_dim, hidden_sizes, hidden_units, dropouts, bias, init_weight, last_act
    )

class DNN(nn.Sequential):
    def __init__(
        self, input_dim: int, hidden_sizes: List[int], hidden_units: List[str] = 'relu', dropouts: List[float] = 0.0,  bias=True, init_weight=True, last_act='identity'
    ):
        n = len(hidden_sizes)
        hidden_sizes = self.check_list(hidden_sizes, n)
        hidden_units = self.activate(*(
            self.check_list(hidden_units, n-1) + self.check_list(last_act)
        ))
        dropouts = self.check_list(dropouts, n)
        hidden_sizes = [input_dim] + hidden_sizes
        fc = []
        for i,(in_dim, out_dim) in enumerate(zip(hidden_sizes[:-1], hidden_sizes[1:])):
            fc.extend([
                nn.Dropout(p=dropouts[i]),
                nn.Linear(
                    in_features=in_dim, out_features=out_dim, bias=bias
                ),
                hidden_units[i]
            ])
        super(DNN, self).__init__(*fc)
        if init_weight: self.apply(make_weight)

    @property
    def output_dim(self):
        return self[-2].out_features

    @staticmethod
    def activate(*units):
        def f(unit):
            if unit == 'relu': return nn.ReLU(True)
            elif unit == 'prelu': return nn.PReLU()
            elif unit == 'lrelu': return nn.LeakyReLU(0.2, True)
            elif unit == 'tanh': return nn.Tanh()
            elif unit == 'sigmoid': return nn.Sigmoid()
            elif unit == 'identity': return nn.Identity()
        return list(map(f, filter(None, units)))

    @staticmethod
    def check_list(x, n=1):
        if not isinstance(x, (tuple, list)):
            x = [x] * n
        return x[:n]
        

def clip_weight(layer, min_value=0.0, max_value=1.0):
    def func(m):
        cls = m.__class__.__name__
        if cls.find('Linear') != -1:
            with torch.no_grad():
                m.weight.clamp_(min_value, max_value)
    layer.apply(func)

def make_weight(m):
    cls = m.__class__.__name__
    if cls.find('Conv') != -1:
        nn.init.normal_(m.weight, 0.0, 0.02)
    elif cls.find('BatchNorm') != -1:
        nn.init.normal_(m.weight, 1.0, 0.02)
        if m.bias is not None: nn.init.zeros_(m.bias)
    elif cls.find('Linear') != -1:
        nn.init.kaiming_uniform_(m.weight, a=1)
        if m.bias is not None: nn.init.constant_(m.bias, 0)


def make_cnn(input_channel, channels, kernels, strides, paddings):
    r"""Returns a ModuleList of 2D convolution layers. 
    
    .. note::
    
        All submodules can be automatically tracked because it uses nn.ModuleList. One can
        use this function to generate parameters in :class:`BaseNetwork`. 
        
    Example::
    
        >>> make_cnn(input_channel=3, channels=[16, 32], kernels=[4, 3], strides=[2, 1], paddings=[1, 0])
        ModuleList(
          (0): Conv2d(3, 16, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1))
          (1): Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1))
        )
    
    Args:
        input_channel (int): input channel in the first convolution layer. 
        channels (list): a list of channels, each for one convolution layer.
        kernels (list): a list of kernels, each for one convolution layer.
        strides (list): a list of strides, each for one convolution layer. 
        paddings (list): a list of paddings, each for one convolution layer. 
    
    Returns:
        nn.ModuleList: A ModuleList of 2D convolution layers.
    """
    N = len(channels)
    
    for item in [channels, kernels, strides, paddings]:
        assert isinstance(item, list), f'expected as list, got {type(item)}'
        assert len(item) == N, f'expected length {N}, got {len(item)}'
    
    channels = [input_channel] + channels
    
    cnn = []
    for i in range(N):
        cnn.append(nn.Conv2d(in_channels=channels[i], 
                             out_channels=channels[i+1], 
                             kernel_size=kernels[i], 
                             stride=strides[i], 
                             padding=paddings[i], 
                             dilation=1, 
                             groups=1))
    
    cnn = nn.ModuleList(cnn)
    
    return cnn


def make_transposed_cnn(input_channel, channels, kernels, strides, paddings, output_paddings):
    r"""Returns a ModuleList of 2D transposed convolution layers. 
    
    .. note::
    
        All submodules can be automatically tracked because it uses nn.ModuleList. One can
        use this function to generate parameters in :class:`BaseNetwork`. 
        
    Example::
    
        make_transposed_cnn(input_channel=3, 
                            channels=[16, 32], 
                            kernels=[4, 3], 
                            strides=[2, 1], 
                            paddings=[1, 0], 
                            output_paddings=[1, 0])
        ModuleList(
          (0): ConvTranspose2d(3, 16, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), output_padding=(1, 1))
          (1): ConvTranspose2d(16, 32, kernel_size=(3, 3), stride=(1, 1))
        )
    
    Args:
        input_channel (int): input channel in the first transposed convolution layer. 
        channels (list): a list of channels, each for one transposed convolution layer.
        kernels (list): a list of kernels, each for one transposed convolution layer.
        strides (list): a list of strides, each for one transposed convolution layer. 
        paddings (list): a list of paddings, each for one transposed convolution layer. 
        output_paddings (list): a list of output paddings, each for one transposed convolution layer. 
    
    Returns:
        nn.ModuleList: A ModuleList of 2D transposed convolution layers.
    """
    N = len(channels)
    
    for item in [channels, kernels, strides, paddings, output_paddings]:
        assert isinstance(item, list), f'expected as list, got {type(item)}'
        assert len(item) == N, f'expected length {N}, got {len(item)}'
    
    channels = [input_channel] + channels
    
    transposed_cnn = []
    for i in range(N):
        transposed_cnn.append(nn.ConvTranspose2d(in_channels=channels[i], 
                                                 out_channels=channels[i+1], 
                                                 kernel_size=kernels[i], 
                                                 stride=strides[i], 
                                                 padding=paddings[i], 
                                                 output_padding=output_paddings[i],
                                                 dilation=1, 
                                                 groups=1))
    
    transposed_cnn = nn.ModuleList(transposed_cnn)
    
    return transposed_cnn

