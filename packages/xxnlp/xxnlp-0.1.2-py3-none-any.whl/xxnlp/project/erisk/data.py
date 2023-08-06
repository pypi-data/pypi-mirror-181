from xxnlp.utils import pickle_load, ojoin, pickle_dump, set_directory, owalk, cache_results
from xxnlp.data import DataLoader, Dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from collections import namedtuple
from tqdm import tqdm
import pytorch_lightning as pl
with set_directory():
    from constant import ERISK_PATH as DATA_PATH
import torch, numpy as np

Instance = namedtuple('Instance', ['text', 'label'])

# ------------------------ 0. load data (flatten ==> focus on each post)
def train_split(test_size=0.1):
    data = pickle_load(ojoin(DATA_PATH, 'full_token_data.pkl'))
    all_text, all_label = zip(*[(x['text'], float(x['label'])) for sub in data for x in sub])
    return train_test_split(
        all_text, all_label, random_state=101, test_size=test_size
    )

# ------------------------ 1. tf-idf vectorization
def tf_idf(test_size=0.1):
    train_text, dev_text, train_y, dev_y = train_split(test_size)
    vec = TfidfVectorizer(analyzer='word', lowercase=True, max_features=1000)
    train_x = vec.fit_transform(train_text)
    dev_x = vec.transform(dev_text)
    pickle_dump({
        'trainX': train_x, 'testX': dev_x, 
        'trainY': train_y, 'testY': dev_y
    }, ojoin(DATA_PATH, 'tfidf_token_data.pkl'))

# ------------------------ 2. 
def collate_fn(data):
    labels, batch = [], []
    for item, label in data:
        user_feats = {}
        for k, v in item.items():
            user_feats[k] = torch.LongTensor(v)
        batch.append(user_feats); labels.append(label)
    labels = torch.FloatTensor(np.array(labels))
    return batch, labels

class HierDataset(Dataset):
    def __init__(self, input_dir, tokenizer, max_len, split="train", max_posts=64, limit=-1):
        assert split in {"train", "test"}
        self.input_dir = input_dir
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.max_posts = max_posts
        (self.labels, self.datas), = self.process(
            _cache_fp=[ojoin(input_dir, f'{split}.pkl')], _refresh=False, folder=ojoin(input_dir, split)
        )
        if limit > 0:
            self.datas, self.labels = self.datas[:limit], self.labels[:limit]
        
    @cache_results()
    def process(self, folder, **kwargs):
        labels, datas = [], []
        for dir, fname in tqdm(owalk(folder, ext='txt')):
            label = float(fname[-5])   # '000000_0.txt'
            posts = open(ojoin(dir, fname), encoding="utf-8").read().strip().split("\n")[:self.max_posts]
            data = self.tokenizer(posts, truncation=True, padding='max_length', max_length=self.max_len)
            labels.append(label); datas.append(data)
        return labels, datas

    def __len__(self) -> int:
        return len(self.datas)

    def __getitem__(self, index: int):
        return self.datas[index], self.labels[index]
    
class EriskDataModule(pl.LightningDataModule):

    def __init__(self, batch_size, input_dir, tokenizer, max_len):
        super().__init__()
        self.bs = batch_size
        self.input_dir = input_dir
        self.tokenizer = tokenizer
        self.max_len = max_len
    
    def setup(self, stage):
        if stage == "fit":
            self.train_set = HierDataset(self.input_dir, self.tokenizer, self.max_len, "train")
            self.test_set = HierDataset(self.input_dir, self.tokenizer, self.max_len, "test")
        elif stage == "test":
            self.test_set = HierDataset(self.input_dir, self.tokenizer, self.max_len, "test")

    def train_dataloader(self):
        return DataLoader(self.train_set, batch_size=self.bs, collate_fn=collate_fn, shuffle=True, pin_memory=False, num_workers=4)

    def val_dataloader(self):
        return DataLoader(self.test_set, batch_size=self.bs, collate_fn=collate_fn, pin_memory=False, num_workers=4)
    

if __name__ == '__main__':
    tf_idf()