from xxnlp import Registry
from xxnlp.data.base import Dataloaders, Datasets
from functools import partial

import torch
from torch.utils.data import random_split, DataLoader, Subset

from torchtext.data.functional import to_map_style_dataset
from torchtext.datasets import DATASETS

TT_CLASS_DATA = Registry('data:classification')


def dfn(name, data_path, split_ratio):
    """dataset function for train/test data"""
    train_iter, test_iter = DATASETS[name](data_path)
    train_dataset = to_map_style_dataset(train_iter)
    test_dataset = to_map_style_dataset(test_iter)
    num_train = int(len(train_dataset) * split_ratio)
    split_train_, split_valid_ = random_split(
        train_dataset, [num_train, len(train_dataset) - num_train]
    )
    return Datasets( train=split_train_, val=split_valid_, test=test_dataset)  # type: ignore


_TTEXT_DATA = {
    'AG_NEWS': ('ag_news', dfn)
}


for name, (register_name, fn) in _TTEXT_DATA.items():
    TT_CLASS_DATA(
        fn=partial(fn, name=name), name=register_name
    )