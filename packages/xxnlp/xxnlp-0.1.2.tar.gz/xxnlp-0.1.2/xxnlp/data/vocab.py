from xxnlp import Registry
from xxnlp.utils import cache_results, osplit
from torchtext.vocab import build_vocab_from_iterator
from torchtext.data.utils import ngrams_iterator
from collections import namedtuple

VOCAB = Registry('vocab')
Record = namedtuple('Item', ['name', 'fn', 'metadata'])

def ngram_based(vocab_path, data, tokenizer, ngrams, use_cache=True):
    param_d = osplit(vocab_path)
    def yield_tokens(data_iter, ngrams):
        for _, text in data_iter:
            yield ngrams_iterator(tokenizer(text), ngrams)
    if use_cache and param_d['ngrams'] == str(ngrams):
        re_generate = False
    else:
        re_generate = True
    @cache_results(vocab_path, _refresh=re_generate)
    def process():
        vocab = build_vocab_from_iterator(
            yield_tokens(data, ngrams), specials=["<unk>"]
        )
        vocab.set_default_index(vocab['<unk>'])
        return vocab
    return process()


_VOCAB_DATA = [
    Record('ag_news', ngram_based, dict(mode='ngram'))
]

for name, fn, metadata in _VOCAB_DATA:
    VOCAB(fn=fn, name=name, **metadata)
    