from ..types import *
from .logging import *
from .xtools import *
from ..tools.contribute import color_str

import re, os, pickle, cloudpickle, yaml, torch, random, sys, inspect
import numpy as np
from contextlib import contextmanager
from functools import reduce, wraps

from datetime import timedelta, datetime
from time import perf_counter
from fastNLP import DataSet

log = Logger.get()



def timeit(_func=None, *, color='green', bold=False):
    def decorator_timeit(f):
        r"""Print the runtime of the decorated function. """
        @wraps(f)
        def wrapper_timeit(*args, **kwargs):
            t = perf_counter()
            out = f(*args, **kwargs)
            total_time = timedelta(seconds=round(perf_counter() - t))
            timestamp = datetime.now().isoformat(' ', 'seconds')
            print(color_str(string=f'\nTotal time: {total_time} at {timestamp}', color=color, bold=bold))
            return out
        return wrapper_timeit
    if _func is None:
        return decorator_timeit
    else:
        return decorator_timeit(_func)

def cache_results(*_cache_fp, _refresh=False):
    r""" a decorator to cache function results
    @reference: FastNLP::core::utils
    :param str `_cache_fp`:     where to read the cache from
    :param bool `_refresh`:     whether to regenerate cache
    """
    def wrapper_(func):
        def wrapper(*args, **kwargs):
            refresh = kwargs.pop('_refresh', _refresh)
            cache_fp = kwargs.pop('_cache_fp', _cache_fp)
            if kwargs.pop('_skipit', False):
                return func(*args, **kwargs)
            if isinstance(cache_fp, str): cache_fp = [cache_fp]
            cond = cache_fp and not refresh and oexists(*cache_fp)
            if not cond:
                omake(*cache_fp)
                results = func(*args, **kwargs)
                if not results:
                    raise RuntimeError("The return value is None. Delete the decorator.")
                if len(cache_fp) == 1 and isinstance(results, Mapping):
                    results = [results]
                for path, result in zip(cache_fp, results):
                    pickle_dump(result, path)
            else:
                for fp in cache_fp: log.info(f'read cache from {color_str(fp)}')
            return map(pickle_load, cache_fp)
        return wrapper
    return wrapper_



def one_time(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_been_run:
            wrapper.has_been_run = True
            return func(*args, **kwargs)
    wrapper.has_been_run = False
    return wrapper

def check_in_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def get_dir():
    """get execute directory of main program """
    if check_in_ipython():
        return os.getcwd()
    return odir(sys.argv[0])

def find_dotenv(path_name='', file_name='.env'):
    """find .env in current and all its parent"""
    path = path_name or get_dir(); path = Path(path)
    while path.as_posix() != path.root:
        attempt = path/file_name
        if attempt.exists(): return attempt
        path = path.parent
    return None

def ojoin(*args, create_if_not_exist=False):
    path = os.path.join(*args)
    if create_if_not_exist: 
        omake(path)
    return path

def oreplace(path, toreplace: str):
    parent = odir(path)
    return ojoin(parent, toreplace)

def owalk(*args, limit=-1, ext=None):
    for path in args:
        for name in sorted(os.listdir(path)):
            if ext and not name.endswith(ext): continue
            yield path, name
            if limit > 0: limit -= 1
            if limit == 0: break 
        else: continue  # only execute if inner loop not break
        break

def omake(*args):
    for path in map(odir, args):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

def odir(path, has_extension=True):
    _root, _ext = os.path.splitext(path)
    if has_extension and _ext != '':
        _root = os.path.dirname(_root)
    return _root

def ofind(path, pattern):
    r"""Find path with given patterns
    """
    pattern = re.compile(pattern)
    for p,_,file in os.walk(path):
        for each in file:
            if pattern.search(each):
                yield ojoin(path, each)

def osplit(path, sep='_'):
    """split xxxx/ag_news/s=1_ngram=2.vocab' 
    >>> {'s': 1, 'ngram': 2}
    """
    _root, _ext = os.path.splitext(path)
    names = os.path.basename(_root)
    return dict(x.split('=') for x in names.split('_'))

def oexists(*path):
    def check_exist(path):
        return os.path.exists(path)
    return all(check_exist(p) for p in path)

def opath(path):
    return os.path.abspath(path)    



def pickle_load(f, ext='.pkl', encode="ASCII"):
    r"""Read a pickled data from a file. 
    """
    if not f: raise FileNotFoundError()
    if isinstance(f, Path):
        f = f.as_posix() 
        f += [ext,''][f[-4:]==ext]

    with open(f, 'rb') as file:
        return cloudpickle.load(file, encoding=encode)

def pickle_loads(*f):
    for sf in f: 
        yield pickle_load(sf)

def pickle_dump(obj, f, ext='.pkl'):
    r"""Serialize an object using pickling and save in a file. 
    
    Args:
        obj (object): a serializable object
        f (str/Path): file path
        ext (str, optional): file extension. Default: .pkl
    """
    if isinstance(f, Path):
        f = f.as_posix()
        f += [ext,''][f[-4:]==ext]
    
    with open(f, 'wb') as file:
        return cloudpickle.dump(obj=obj, file=file, protocol=pickle.HIGHEST_PROTOCOL)


def yaml_load(f):
    r"""Read the data from a YAML file. 
    """
    if isinstance(f, Path):
        f = f.as_posix()
    
    with open(f, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def yaml_dump(obj, f, ext='.yml'):
    r"""Serialize a Python object using YAML and save in a file. 
    
    Args:
        obj (object): a serializable object
        f (str/Path): file path
        ext (str, optional): file extension. Default: .yml
        
    """
    if isinstance(f, Path):
        f = f.as_posix()
    with open(f+ext, 'w') as file:
        return yaml.dump(obj, file, sort_keys=False)

    
class CloudpickleWrapper(object):
    r"""Uses cloudpickle to serialize contents (multiprocessing uses pickle by default)
    
    This is useful when passing lambda definition through Process arguments.
    """
    def __init__(self, x):
        self.x = x
        
    def __call__(self, *args, **kwargs):
        return self.x(*args, **kwargs)
    
    def __getattr__(self, name):
        return getattr(self.x, name)
    
    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.x)
    
    def __setstate__(self, ob):
        import pickle
        self.x = pickle.loads(ob)

        
@contextmanager
def set_directory(path = None, start_from_home = False):
    r"""Sets the cwd within the context, cd back to original path
    
    """
    if not path: path = get_dir()
    elif start_from_home: path = Path.home()/path
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)

def seed_all(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    generator = torch.Generator()
    generator.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

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

def get4d(dataDict, keyList):
    def get(key):
        return reduce(dict.get, key.split("."), dataDict)
    return list(map(get, keyList))

def _flatten(lst):
    for x in lst:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from _flatten(x)
        else:
            yield x

def _flatten_dict(dct, prefix=''):
    if isinstance(dct, (Mapping, Dict)):
        if prefix: prefix += '.'
        for k, v in dct.items():
            yield from _flatten_dict(v, prefix+str(k))
    else:
        yield prefix, dct
    
def flatten_dict(dct, rtn_dct=True):
    if rtn_dct:
        return dict(_flatten_dict(dct))
    else:
        return _flatten_dict(dct)

def flatten(lst, rtn_lst=True):
    if rtn_lst:
        return list(_flatten(lst))
    else:
        return _flatten(lst)

def filter_empty(*lst, empty=None, remove_index=[]):
    idx, rtn = zip(*filter(lambda c: c[1] != empty and c[0] not in remove_index, enumerate(lst[0])))
    rtn_lst = [list(rtn)]
    for l in lst[1:]: rtn_lst.append([l[i] for i in idx])
    return rtn_lst
