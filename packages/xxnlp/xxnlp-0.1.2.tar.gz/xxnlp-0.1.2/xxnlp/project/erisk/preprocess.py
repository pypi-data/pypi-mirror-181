import xml.etree.ElementTree as ET
import warnings, re, os, random, numpy as np, csv, pandas as pd, cupy, heapq as hq
warnings.filterwarnings("ignore", category=UserWarning)

from datetime import datetime as DT
from xxnlp import Args
from xxnlp.utils import ojoin, pickle_load, oexists, cache_results
from joblib import Parallel, delayed 
from tqdm import tqdm
from operator import itemgetter
from itertools import product, groupby
from collections import namedtuple
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

T = namedtuple('T', ['id', 'label', 'date', 'embed', 'text', 'sim', 'sent', 'e2p'])
L = namedtuple('L', ['ppl', 'lbl', 'path'])
O = namedtuple('O', ['word', 'freq', 'embed'])

home = os.getenv('PROJECT')
args = Args(
    _post_init_ = True,
    # --------------- general settings ------------------------ # 
    datapath = ojoin(home, 'data'),
    nerpath = ojoin(home, 'data/pretrained/ner'),
    modelname="mental/mental-bert-base-uncased",
    # --------------- data generation ------------------------ # 
    max_doc = 128,
    device='--int: 0',
)


def tokenize_text(posts, process_ner=True):

    def clean_text(text):
        text = re.sub(r'http\S+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def tokenize_text(text):
        return ' '.join(TOKENIZER.tokenize(text, truncation=True))

    for post in posts:
        text = post['text']
        if text != '':
            text = clean_text(text)
            text = tokenize_text(text)
        if process_ner:
            doc = NLP(text)
            post['ner'] = [(e.text, e.start, e.end) for e in doc.ents]
        post['text'] = text
    return posts


# ------------------------ 0. turn all data into standard format
"""
required format
[
    {'text': ..., 'date': ...(datetime), '_id': ..., 'label': ...}
    ...
]
"""
def accumulate(l):
    it = groupby(l, itemgetter(1))
    for ppl, subiter in it:
       yield [x[0] for x in subiter]

def sort_sublist(l):
    l = [x for sub in l for x in sub]
    return sorted(l, key = itemgetter('date'), reverse=True)
       
def collect_information(label_file, path_fn, n_chunk=10, n_jobs=1, limit=None):
    with open(label_file, 'r') as f:
        lines = f.readlines()
    labels = list(filter(None, [tuple(line.split()) for line in lines]))[:limit]
    output = Parallel(n_jobs=n_jobs, timeout=99999)(
            delayed(process_tensor)(*path_fn(*x,k)) for (x,k) in tqdm(product(labels, range(1, n_chunk+1)))
    )
    return list(map(sort_sublist, accumulate(output)))
    

def process_tensor(ppl, lbl, path):
    if not oexists(path): return
    with open(path, 'r') as fin:
        tree = ET.parse(fin)
    dataset = []
    for elem in tree.findall('WRITING'):
        cond = elem.find('TEXT').text and elem.find('DATE').text
        if not cond: continue
        dataset.append({
            "text": elem.find('TEXT').text.replace('\n', '. ').strip(' '),
            "date": DT.strptime(elem.find('DATE').text.strip(' '),'%Y-%m-%d %H:%M:%S'),
            "_id": ppl,
            "label": lbl
        })
    return dataset, ppl

@cache_results(ojoin(args.datapath, 'ERISK/processed/full_raw_data.pkl', create_if_not_exist=True))
def erisk_data(path = ojoin(args.datapath, 'ERISK-2/2017-t1'), **kwargs):
    # --- train data
    def train_path_fn(ppl, lbl, chunk):
        name = 'positive' if lbl == '1' else 'negative'
        return L(path=ojoin(path, f'train/{name}_examples_anonymous_chunks/chunk {chunk}/{ppl}_{chunk}.xml'), ppl=ppl.lstrip('train_'), lbl=lbl)
    label_file = ojoin(path, 'train/risk_golden_truth.txt')
    train_output = collect_information(label_file, train_path_fn, **kwargs)
    # --- test data
    def test_path_fn(ppl, lbl, chunk):
        return L(path=ojoin(path, f'test/chunk {chunk}/{ppl}_{chunk}.xml'), ppl=ppl.lstrip('test_'), lbl=lbl)
    label_file = ojoin(path, 'test/test_golden_truth.txt')
    test_output = collect_information(label_file, test_path_fn, **kwargs)
    # --- erisk 2018
    path = ojoin(args.datapath, 'ERISK-2/2018-t1')
    def get_path_fn(ppl, lbl, chunk):
        return L(path=ojoin(path, f'chunk{chunk}/{ppl}_{chunk}.xml'), ppl=ppl, lbl=lbl)
    label_file = ojoin(path, 'risk-golden-truth-test.txt')
    final_output = collect_information(label_file, get_path_fn, **kwargs)
    return [train_output + test_output + final_output]


@cache_results(ojoin(args.datapath, 'TWITTER/processed/full_raw_data.pkl', create_if_not_exist=True))
def twitter_data(**kwargs):
    pos = pickle_load(ojoin(args.datapath, 'TWITTER/full_raw_positive.pkl'))
    neg = pickle_load(ojoin(args.datapath, 'TWITTER/full_raw_negative.pkl'))
    final = sum([[x[1:] for x in pos], neg], [])
    return [final]


def step0():
    # --- collection data
    data, = erisk_data(_refresh=False, n_jobs=20, n_chunk=10, limit=None)
    data, = twitter_data(_refresh=False)

# ------------------------ 1. clean data

@cache_results()
def do_clean(input_path, n_jobs=1, **kwargs):
    from xxnlp.tools.cleaner import CleanTransformer
    global CLEANER
    CLEANER = CleanTransformer(
        no_urls=True, no_emails=True, no_phone_numbers=True, no_currency_symbols=True, no_repeat=True, no_user=True, no_emoji=True, no_line_breaks=True
    )
    data = pickle_load(input_path)
    output = Parallel(n_jobs=n_jobs)( delayed(clean_text_helper)(p) for p in tqdm(data))
    return [output]

def clean_text_helper(posts):
    texts = CLEANER.transform(
        [decode_unicode_references(p['text']) for p in posts]
    )
    for i, text in enumerate(texts):
        posts[i]['text'] = text
    return posts

def decode_unicode_references(data):
    def _callback(matches):
        _id = matches.group(1)
        try: return chr(int(_id))
        except: return _id
    return re.sub("\s?#(\d+)(;|(?=\s))", _callback, data)

def step1():
    for name in ('twitter', 'erisk'):
        path = ojoin(args.datapath, name.upper(), 'processed')
        kwargs = dict(limit = None, n_jobs=20, _refresh=True)
        do_clean(
            input_path=ojoin(path, 'full_raw_data.pkl'),
            _cache_fp=ojoin(path, 'full_clean_data.pkl'), **kwargs
        )

# ------------------------ 2. embedding and similarity matrix
"""
required format
T = namedtuple('T', ['id', 'label', 'date', 'embed', 'text', 'sim', 'sent'])
{
    id: xxx, label: xxx, date: xxx, embed: xxx, text: xxx, sim-matrix: xxx, sent: xxx
}
"""

def ner_extract_helper(posts, limit=None): # one person history
    entities = []
    posts = [p for p in posts if p['text'] != '']
    for post, doc in zip(posts, NER.pipe([p['text'] for p in posts])):
        kwargs = dict(date=post['date'], id=post['_id'], label=post['label'])
        entity = []
        for ent in doc.ents:
            embed = get_ner_embedding(ent); sent = ent.sent.text
            sim = cosine_similarity(embed.reshape(1,-1), ONTOLOGY.embed) # (169, 1)
            sim = np.multiply(sim, ONTOLOGY.freq)
            entity.append(T(
                text=ent.text, embed=embed, sent=sent, sim=sim, **kwargs
            ))
        entities.append(entity)
    return entities

@cache_results()
def do_ner(input_path, limit, **kwargs):
    data = pickle_load(input_path)[:limit]
    output = []
    for usr_hist in tqdm(data):
        output.append(ner_extract_helper(usr_hist))
    return [output]

def get_ner_embedding(doc):
    if doc.ents: #there is only one per each ontogloy
        return np.average([x.vector.get() for x in doc.ents], axis=0)
    return np.average(doc._.trf_token_vecs.get(), axis=0)

def step2():
    import spacy
    spacy.util.fix_random_seed(0)
    spacy.require_gpu()
    from xxnlp.spacy import create_different_label
    with cupy.cuda.Device(args.device):
        # --- ner extraction
        global NER, ONTOLOGY
        NER = spacy.load(args.nerpath) 
        NER.add_pipe('sentencizer', first=True)
        NER.add_pipe('trf_vectors', last=True)
        ONTOLOGY = load_ontology(with_ner_embed=True)
        kwargs = dict(limit = None, _refresh=True)
        dataname = ['erisk', 'twitter'][args.device]
        path = ojoin(args.datapath, dataname.upper(), 'processed')
        do_ner(
            input_path=ojoin(path, 'full_clean_data.pkl'),
            _cache_fp=ojoin(path, 'full_ner_data.pkl'), **kwargs
        )

# ------------------------ 3. testdataset and data augmentation
"""
0. 
1. further process data to make it compatible to current design
T = namedtuple('T', [
    'id', 'label', 'date', 'embed', 'text', 'sim', 'sent', 'e2d']
)   # 最后一个映射 # entity --> # post
"""
import requests


def query(source, targets):
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE')}"}
    payload = {
        "inputs": {
            "source_sentence": source,
            "sentences":targets
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def load_ontology(with_ner_embedding=False):
    with open(ojoin(args.datapath, 'EMBEDDING/depression_ontology_word_list.csv'), mode='r') as f:
        reader = csv.reader(f); header = next(reader)
        words, freqs = zip(*[(w,f) for w,f in reader])
        freqs = np.array([float(x) for x in freqs])
    embeds = None
    if with_ner_embedding: embeds = np.stack([get_ner_embedding(d) for d in NER.pipe(words)])
    return O(words, freqs, embeds)


def do_transform_helper(this_usr_posts, ontology):
    def get_label(l): #list of post -> subject label and id
        for x in l: 
            if x != []: return (x[0].label, x[0].id)
        return (-1, -1)
    def get_data(l):
        for i,post in enumerate(l):
            for doc in post:
                yield (doc.embed, doc.sent, doc.text, doc.date, i)
    def get_top(s, k): #similarity -> top k similar word
        return hq.nlargest(k, range(len(s)), s.__getitem__)
    def get_sim():
        embed_ontology = MODEL.encode(ontology.word)
        embed_text = MODEL.encode(texts)
        return util.cos_sim(embed_text, embed_ontology)
    label, usr = get_label(this_usr_posts)
    if label == -1: return
    embeds, sents, texts, dates, e2ps = zip(*get_data(this_usr_posts))
    return T(
        id=usr,label=label,date=dates,embed=np.array(embeds),text=texts,sim=get_sim(),sent=sents,e2p=e2ps
    )
    
@cache_results()
def do_transform(input_path, limit=None, n_jobs=1, device=0, **kwargs):
    global MODEL
    MODEL = SentenceTransformer('all-roberta-large-v1', device=device)
    ontology = load_ontology()
    data = pickle_load(input_path)[:limit]
    output = []
    for u in tqdm(data):
        out = do_transform_helper(u, ontology)
        if out is not None:
            output.append(out)
    return [output]


    
def step3():
    dataname = ['erisk', 'twitter'][args.device]
    path = ojoin(args.datapath, dataname.upper(), 'processed')
    kwargs = dict(limit = None, n_jobs=1, _refresh=True, device=args.device)
    do_transform(
        input_path=ojoin(path, 'full_ner_data.pkl'),
        _cache_fp=ojoin(path, 'full_full_data.pkl'), **kwargs
    )


    

if __name__ == '__main__':
    # step0()
    # step1()
    # step2()
    step3()