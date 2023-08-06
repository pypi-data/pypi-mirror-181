import json, os, re, sys, csv
import numpy as np
from dataclasses import dataclass
from torch.utils.data import Dataset, DataLoader
from xxnlp.types import Generator, Optional

csv.field_size_limit(sys.maxsize)


class Data:
    keys = ['train', 'val', 'test', 'aug']
    def apply(self, func, **data):
        for mode, old_data in data.items():
            assert mode in self.keys, "%s must be one of %s"%(mode, self.keys)
            new_data = func(old_data or getattr(self, mode))
            if isinstance(new_data, Generator):
                setattr(self, mode, list(zip(*new_data)))
            else:
                setattr(self, mode, new_data)
    def __iter__(self):
        for mode in self.keys: 
            yield getattr(self, mode)
            
@dataclass
class Datasets(Data):
    """Class for keeping track of datasets"""
    train: Optional[Dataset] = None
    test: Optional[Dataset] = None
    val: Optional[Dataset] = None
    aug: Optional[Dataset] = None

@dataclass
class Dataloaders(Data):
    """Class for keeping track of dataloaders"""
    train: DataLoader
    test: DataLoader 
    val: Optional[DataLoader] = None
    aug: Optional[Dataset] = None

