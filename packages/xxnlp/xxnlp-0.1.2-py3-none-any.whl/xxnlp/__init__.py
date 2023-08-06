import sys, shutil, itertools, ast, re, argparse
from pathlib import Path
from dotenv import load_dotenv
from copy import deepcopy
from pprint import pformat
from operator import attrgetter
from xxnlp.utils import get_dir, find_dotenv, flatten_dict, one_time, ojoin
from xxnlp.utils.logging import Logger, Recorder
from xxnlp.types import Mapping, Any, Callable, Dict
from xxnlp.model import Model

@one_time
def load_env():
    load_dotenv(find_dotenv(get_dir()))
load_env()

def search_api(key, obj):
    if key in obj: return obj.get(key)
    for nested in filter(lambda _: isinstance(_, (Args, Dict)), obj.values()):
        if (y := search_api(key, nested)) is not None:
            return y
    return None

def to_dict(args):
    rtn_dict = {}
    for k, v in args.items():
        if isinstance(v, Path):
            rtn_dict[k] = str(v)
        elif isinstance(v, Args):
            rtn_dict[k] = to_dict(v)
        rtn_dict[k] = v
    return rtn_dict

class Args(Mapping):

    def __init__(self, level=1, **kwargs):
        for key, value in kwargs.items():
            self.set(key, self.init_helper(value, level=level))
        if kwargs.pop('_post_init_', False):
            self.post_init()

    def to_string(self):
        return '_'.join([f'{k}={v}' for k,v in sorted(self.items())])
    
    @classmethod
    def init_helper(cls, value, level=1):
        if level > 1 and isinstance(value, (Dict, cls)):
            value = cls(level=level-1, **value)
        return value

    def search(self, key): #recursively find key in obj
        return search_api(key, self)

    def set(self, __name, __value):
        key, *subkey = __name.split('.', 1)
        if not subkey:
            setattr(self, key, __value)
        else:
            rtn_value = self.pop(key, Args())
            rtn_value.set(subkey[0], __value)
            setattr(self, key, rtn_value)

    def update(self, override=True, **kwargs):
        for k,v in kwargs.items(): 
            if not override and k in self:
                continue
            self.set(k, v)
        
    def pop(self,__name, __default=None) -> Any:
        return self.__dict__.pop(__name, __default)
    
    def pops(self, *__names, input_mappings={}):
        return {input_mappings.get(n, n): self.pop(n) for n in __names}

    def copy(self):
        return deepcopy(self)

    def __add__(self, other):
        return Args(**self, **other)

    def __contains__(self, item): return hasattr(self, item)
    
    def __iter__(self): yield from self.__dict__

    def get(self, item, *default): 
        if default: return getattr(self, item, default[0])
        else: return getattr(self, item)
    
    def __getitem__(self, item): return getattr(self, item)
    
    def __setitem__(self, item, value): setattr(self, item, value)

    def __len__(self): return len(self.__dict__)

    def post_init(self):
        parser = argparse.ArgumentParser()
        def f(args, prefix=''):
            flag = False
            for k,v in args.items():
                prefix_k = prefix + '.' + k
                if isinstance(v, (Args, dict)): f(v, prefix_k)
                elif v is None or v == 'None': args[k] = None
                elif isinstance(v, str) and v.startswith('$'):
                    if v.startswith('$$'): args[k] = v[1:]
                    else: args[k] = attrgetter(v.lstrip('$'))(self)
                elif isinstance(v, str) and v.startswith('--'):
                    if (match := re.match('--(\w+):\s*(.*)', v)):
                        _type, _value = match.groups(); _type=eval(_type)
                        preargs = [f"--{prefix_k[1:]}", f"-{k}"]
                        if _type.__name__ == 'bool':
                            action = 'store_true' if _type(_value) else 'store_false'
                            parser.add_argument(*preargs, action=action, default=_type(_value))
                        elif _type.__name__ in ['str', 'int', 'float']:
                            parser.add_argument(*preargs, type=_type, default=_type(_value))
                        flag = True
                    else:
                        raise AttributeError("please make sure your argument follows --{type}:{default_value}")
            return flag
        if f(self):
            self.update(**vars(parser.parse_args()))

    def __repr__(self):
        return pformat(self.to_dict())

    def to_dict(self):
        return to_dict(self.copy())

    def __str__(self):
        choice = r"^(choice|interval|range|sort|shuffle|tag|glob)\(.*\)"
        def show(x):
            if x is None or x == 'null':
                return 'null'
            elif isinstance(x, str) and not re.match(choice, x): 
                return f'"{x}"'
            elif not isinstance(x, Mapping):
                return x
            return '{' + ', '.join(f"{k}: {show(v)}" for (k, v) in x.items()) + '}'
        return show(self)

    def hydra_prepare(self, sweep=False):
        """treat arg as sys.argv to be read by hydra"""
        if sweep: 
            sys.argv.extend(["--multirun", "hydra/sweeper=example"])
        for k,v in flatten_dict(self).items():  # type: ignore
            sys.argv.append("%s=%s"%(k, v))
    
    def parse_args(self, sep='', eql='=', ignore=[]):
        if sep != '':
            return sep.join([f'{k}{eql}{v}' for k,v in flatten_dict(self).items() if not k in ignore])
        from hydra.core.override_parser.overrides_parser import ( OverridesParser, create_functions,)
        rules = create_functions()
        parser = OverridesParser(rules)
        return parser.parse_rule(str(self), 'dictContainer')


class Registry:

    def __init__(self, name: str):
        self.name = name
        self.functions = []
        self._registry = []

    @property
    def registry(self):
        return self._registry
    
    def __add__(self, other):
        registries = self.registry + other.registry
        return ConcatRegistry(*registries)
    
    def __len__(self):
        return len(self.functions)
    
    def __contains__(self, key):
        return any(key == e["name"] for e in self.functions)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, functions={self.functions})"

    def get(self, key: str, return_first=True, **metadata):
        matches = [e for e in self.functions if key == e['name']]
        if not matches:
            raise KeyError(f"Key: {key} is not in {type(self).__name__}. Available keys: {self.available_keys()}")
        if metadata:
            matches = [m for m in matches if metadata.items() <= m["metadata"].items()]
            if not matches:
                raise KeyError("Found no matches that fit your metadata criteria. Try removing some metadata")
        matches = [e['fn'] for e in matches]
        return matches[0] if return_first else matches
        
    def remove(self, key: str):
        self.functions = [f for f in self.functions if f['name'] != key]

    def _register_function(self, fn: Callable, name=None, override=False, metadata=None):
        assert isinstance(fn, Callable), f"You can only register a callable, found: {fn}"
        name = name or fn.__name__
        item = {'fn': fn, 'name': name, 'metadata': metadata or {}}
        idx = self._find(item)
        if override and idx:
            self.functions[idx] = item
        assert not idx, f"Function with name: {name} and metadata: {metadata} is already present within {self}. \nHINT: Use `override=True`."
        self.functions.append(item)

    def _find(self, item):
        for i, fn in enumerate(self.functions):
            if all(fn[k] == item[k] for k in ('fn', 'name', 'metadata')):
                return i

    def available_keys(self):
        return sorted(e["name"] for e in self.functions)
    
    def __call__(self, fn: Callable, name=None, override=False, **metadata):
        if fn is not None:
            self._register_function(fn=fn, name=name, override=override, metadata=metadata)
            return fn
        if not (name is None or isinstance(name, str)):
            raise TypeError(f"`name` must be a str, found {name}")
        def _registry(cls):
            self._register_function(fn=cls, name=name, override=override, metadata=metadata)
        return _registry
        

class ConcatRegistry(Registry):
    
    def __init__(self, *registries: Registry):
        super().__init__( ",".join( {registry.name for registry in registries}))
        self._registry = registries

    def __len__(self):
        return sum(len(r) for r in self.registry)
    
    def __contains__(self, key):
        return any(key in r for r in self.registry)

    def __repr__(self):
        return f"{self.__class__.__name__}(registries={self.registries})"  # type: ignore

    def get(self, key: str, return_first=True, **metadata):
        matches = []
        for r in self.registry:
            if key in r:
                result = r.get(key, return_first=return_first, **metadata)
                if not isinstance(result, list):
                    result = [result]
                matches += result
            if matches and return_first:
                return matches[0]
        if not matches: raise KeyError("No matches found in registry")
        return matches
    
    def remove(self, key: str):
        for r in self.registry:
            if key in r and hasattr(r, 'remove'):
                r.remove(key)
    
    def _register_function(self, fn: Callable, name=None, override=False, metadata=None):
        for r in self.registry:
            if hasattr(r, '_register_function'):
                return r._register_function(fn, name=name, override=override, metadata=metadata)
    
    def available_keys(self):
        return list(itertools.chain.from_iterable(r.available_keys()) for r in self.registry)
