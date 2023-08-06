from xxnlp.utils import set_directory, ojoin, owalk, cache_results
from sentence_transformers import SentenceTransformer
from joblib import Parallel, delayed 
from tqdm import tqdm, trange
from functools import reduce
from operator import itemgetter
import xml.dom.minidom as M
import numpy as np
import re, heapq
from sklearn.metrics.pairwise import cosine_similarity


with set_directory():
    from constant import ERISK_PATH as DATA_PATH, SINGLE, ALERT

def get_embedding(*text):
    ENCODER = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    for x in text:
        yield ENCODER.encode(x, convert_to_tensor=False, show_progress_bar=True)

def get_data(fpath):
    post_num = 0
    dom = M.parse(fpath)
    collection = dom.documentElement
    title = collection.getElementsByTagName('TITLE')
    text = collection.getElementsByTagName('TEXT')
    posts = []
    for i in range(len(title)):
        post = title[i].firstChild.data + ' ' + text[i].firstChild.data
        post = re.sub('\n', ' ', post)
        if len(post) > 0:
            posts.append(post.strip())
            post_num = post_num + 1
    return posts, post_num

def get_embed(base_path, name):
    train_posts, train_tags, train_mappings, test_posts, test_tags, test_mappings = [[] for _ in range(6)]
    posts, post_num = get_data(ojoin(base_path, name))
    if "anonymous" in base_path:
        mapping_, post_, tag_ = train_mappings, train_posts, train_tags
    else:
        mapping_, post_, tag_ = test_mappings, test_posts, test_tags
    mapping_.append(list(range(len(post_), len(post_)+post_num)))
    post_.extend(posts)
    tag_.append(int('positive' in base_path))
    return dict(rp=train_posts, rt=train_tags, rm=train_mappings, tp=test_posts, tt=test_tags, tm=test_mappings)

def prepare_embed(n_jobs, limit):
    def f(lst): # list reduction
        return reduce(lambda x, y: x+y, lst)
    basepath = ["negative_examples_anonymous", "negative_examples_test", "positive_examples_anonymous", "positive_examples_test"]
    output = Parallel(n_jobs=n_jobs)(
        delayed(get_embed)(*fpath) for fpath in tqdm(owalk(*[ojoin(DATA_PATH, p) for p in basepath], limit=limit))
    )
    return map(f, zip(*[itemgetter('rp','rt','rm','tp','tt','tm')(x) for x in output]))

@cache_results(ojoin(DATA_PATH, 'miniLM_L6_embs.pkl'))
def final_embed(_refresh=False, n_jobs=1, limit=-1):
    train_posts, train_tags, train_mappings, test_posts, test_tags, test_mappings = prepare_embed(n_jobs, limit)
    train_embs, test_embs = get_embedding(train_posts, test_posts)
    return dict(
        train_posts=train_posts, train_mappings=train_mappings, train_labels=train_tags, train_embs=train_embs,
        test_posts=test_posts, test_mappings=test_mappings, test_labels=test_tags, test_embs=test_embs
    )


def get_topk_helper(posts, mappings, labels, emb, q_emb, d_emb, mode, topk, n_jobs):
    def process(id, post, y, k, paths, scores):
        for key in paths:
            if key == 'last':
                path, top_post = paths[key], post[-k:]
            else:
                path, score = paths[key], scores[key]
                top_i = sorted(heapq.nlargest(k, range(len(score)), score.take))
                top_post = [post[j] for j in top_i]
            with open(ojoin(path, f'{id:06}_{y}.txt'), 'w') as f:
                f.write("\n".join(x.replace("\n", " ") for x in top_post))
    def prepare(i):
        mapping, label = mappings[i], labels[i]
        post = [posts[j] for j in mapping]
        scores = {
            'depress': d_sim[mapping, 0],
            'question': q_sim[mapping].max(axis=1),
            'together': c_sim[mapping].max(axis=1),
            'last': None
        }; paths = {}
        for k in scores:
            paths[k] = ojoin(DATA_PATH, f'{k}_top{topk}', mode, create_if_not_exist=True)
        return i, post, label, topk, paths, scores
    d_sim = cosine_similarity(emb, d_emb)   # (batch_size, num_alert)
    q_sim = cosine_similarity(emb, q_emb)   # (batch_size, num_question)
    c_sim = np.concatenate([d_sim, q_sim], axis=1)
    num_records = len(labels)
    Parallel(n_jobs=n_jobs)(
        delayed(process)(*prepare(i)) for i in trange(num_records)
    )
        
def get_topk(k=16, n_jobs=1):
    """{topk} high risky posts"""
    data,  = final_embed(n_jobs=20)
    q_emb, d_emb = get_embedding(SINGLE, ALERT)
    for mode in ('train', 'test'):
        strings = '{0}_{1}, {0}_{2}, {0}_{3}, {0}_{4}'.format(mode, 'posts', 'mappings', 'labels', 'embs')
        post, mapping, label, emb = itemgetter(*strings.split(', '))(data)
        get_topk_helper(post, mapping, label, emb, q_emb, d_emb, mode, k, n_jobs)


if __name__ == '__main__':
    get_topk() 