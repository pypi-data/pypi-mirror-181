from shutil import rmtree, move, copyfile
from pathlib import Path
import inspect, optuna, os
from typing import Callable, Dict, Mapping, Sequence
from optuna.pruners import MedianPruner, HyperbandPruner, NopPruner
from optuna.samplers import PartialFixedSampler, RandomSampler
from optuna._transform import _SearchSpaceTransform
import multiprocessing as mp
from tqdm import tqdm
import numpy as np
import pandas as pd

import torch
import torch.distributed as dist
from xxnlp.utils import (
    timeit, color_str, oexists, ojoin, omake
)
from xxnlp import Args
from hydra.core.override_parser.types import (
    Sweep, RangeSweep, ChoiceSweep, IntervalSweep, Transformer, QuotedString
)
from optuna.distributions import (
    CategoricalDistribution, IntLogUniformDistribution, IntUniformDistribution, LogUniformDistribution, UniformDistribution, BaseDistribution, DiscreteUniformDistribution
)
from fastNLP.envs import get_global_rank, is_cur_env_distributed, rank_zero_call, FASTNLP_DISTRIBUTED_CHECK, FASTNLP_GLOBAL_RANK, FASTNLP_GLOBAL_SEED, FASTNLP_NO_SYNC
from copy import copy
from random import random, shuffle
from itertools import product
from functools import reduce

@timeit(color='green', bold=True)
def run_single(run, config, seeds, use_gpu=False, gpu_ids=None, copy_file=False, prune_exp=True, level=2):
    r"""A convenient function to parallelize the experiment (master-worker pipeline). 
    
    It is implemented by using `concurrent.futures.ProcessPoolExecutor`
                
    Args:
        run (function): a function that defines an algorithm, it must take the 
            arguments `(config, seed, device, logdir)`
        config (args): a :class:`Args` object defining all configuration settings parsed via Hydra
        seeds (list): a list of random seeds
        use_gpu (bool): if `True`, then use CUDA. Otherwise, use CPU.
        gpu_ids (list): if `None`, then use all available GPUs. Otherwise, only use the
            GPU device defined in the list. 
        level (int): argparse level, default to be able to parse A.B.C
    """
    if is_cur_env_distributed() and get_global_rank() != 0:
        objective(None)

    check_valid_config(config)
    checkpoint = config.checkpoint
    print(color_str(f'\nExperiment starts. Loggings are stored in {checkpoint}. ', 'cyan', bold=True))

    # recognize distributions in configurations
    parsed = config.parse_args()
    sweep_config = SweepConfig(parsed)
    configs: list = sweep_config.make_config(log_dir=checkpoint)
    KEYS: dict = sweep_config.search_space
    
    # create logging and model checkpoint dir
    log_path = prepare_path(checkpoint)
    # save .py files from source folder
    prepare_copy(copy_file, run, log_path)
    write_analysis(ojoin(log_path, f'{config.exp_name}.py'), log_path, config.exp_name, config.optim_metric)
    
    # Create unique id for each job
    jobs = list(enumerate(product(configs, seeds), start=1))
    KEYS['seed'] = seeds
    storage = f"sqlite:///{str(log_path)}/{config.exp_name}.db"
    pruner = HyperbandPruner() if prune_exp else NopPruner()
    study = optuna.create_study(
        study_name=config.exp_name,
        pruner=pruner,
        direction=config.optim_direction,
        storage=storage,
        load_if_exists = True
    )
    for param, space in KEYS.items(): # save config in database
        study._storage.set_study_user_attr(study._study_id, param, space)
    
    # define how each job should be done, call (run) with parameter grid
    def _run(job, lock=None):
        job_id, (config, seed) = job
        # VERY IMPORTANT TO AVOID GETTING STUCK, oversubscription
        # see following links
        # https://github.com/pytorch/pytorch/issues/19163
        # https://software.intel.com/en-us/intel-threading-building-blocks-openmp-or-native-threads
        # torch.set_num_threads(1)
        num_gpu = torch.cuda.device_count()
        if not use_gpu:
            device = 'cpu'
        elif gpu_ids is None:  # use all GPUs
            device = job_id % num_gpu
        # elif isinstance(gpu_ids, Sequence):
        #     assert all([i >= 0 and i < num_gpu for i in gpu_ids])
        #     device = gpu_ids[job_id % len(gpu_ids)]
        elif isinstance(gpu_ids, (int, Sequence)):
            device = gpu_ids
            
        print('\n\n')
        print(f'@ Experiment: ID: {config["exp_id"]} ({len(configs)}), Seed: {seed}, Device: {device}, Job: {job_id} ({len(jobs)}), PID: {os.getpid()}')
        print('#'*80)
        _args = Args(**config, device=device, seed=seed, level=level)
        _args.set('task_name', ' | '.join(f'{k}={_args.search(k)}' for k in ('exp_name', 'seed', *KEYS)))
        pruner = HyperbandPruner() if prune_exp else NopPruner()
        study = optuna.load_study(study_name=_args.exp_name, storage=storage, pruner=pruner)

        def get_value(trial_id):
            STATE = optuna.trial.TrialState
            trial = study._storage.get_trial(trial_id)
            if trial.state == STATE.COMPLETE:
                return {'metric': trial.values[0]} #in case it's multi-objective
            else:
                return {'metric': 0} #issue: NA might be more appropriate

        global objective
        def objective(trial):
            if is_cur_env_distributed():
                trial = optuna.integration.TorchDistributedTrial(trial)
            for k, vs in KEYS.items():
                trial._suggest(k, sweep_config.dist.get(k, CategoricalDistribution(vs)))
            _args.update(trial = trial, trial_id = trial._trial_id)
            result = run(_args)
            if use_gpu: torch.cuda.empty_cache()
            return result

        fixed_params = {k: _args.search(k) for k in KEYS}
        study.sampler = PartialFixedSampler(fixed_params, study.sampler)
        study.optimize(objective, n_trials=1, gc_after_trial=True)
        # since we have only 1 trial to run, we can index it with -1
        return {'exp_id': _args.exp_id, 'trial_id': _args.trial_id, **fixed_params, **get_value(_args.trial_id)}
    
    results = [_run(job, None) for job in jobs]
    print(color_str(f'\nExperiment finished. Loggings are stored in {log_path.absolute()}. ', 'cyan', bold=True))
    result_d = pd.DataFrame(results)
    with open(log_path/'result.tsv', 'w') as fw:
        fw.write(repr(result_d))

class SweepConfig:

    def __init__(self, config_d: Dict, n_repeat: int = 1):
        self.config_d = config_d
        self.dist, self.search_space = {}, {}
        self.n_repeat = n_repeat
        self.sampler = self.prepare_sampler()

    def prepare_sampler(self):
        _rng = np.random.RandomState(seed=1000)
        def sample_independent(key, dist):
            trans = _SearchSpaceTransform({key: dist})
            trans_params = _rng.uniform(trans.bounds[:, 0], trans.bounds[:, 1])
            return trans.untransform(trans_params)[key]
        return sample_independent

    @property
    def n_trials(self):
        return reduce(lambda x, y: x*y, map(len, self.search_space.values()))

    def make_config(self, **fixed_dict):
        lst = self.make_config_helper(**fixed_dict, **self.config_d)
        lst *= self.n_repeat
        return [{'exp_id': i, **d} for i,d in enumerate(lst)]
    
    def make_config_helper(self, **d):
        sdist, sspace, fix = {}, {}, {}
        for k, v in d.items():
            if isinstance(v, Sweep):
                self.dist[k] = sdist[k] = self.parse_sweep(v)
                self.search_space[k] = sspace[k] = self.parse_dist(k, sdist[k])
            elif isinstance(v, QuotedString):
                fix[k] = v.text
            elif isinstance(v, (Dict, Args)):
                sspace[k] = self.make_config_helper(**v)
            else:
                fix[k] = v
        keys, values = sspace.keys(), sspace.values()
        grid_product = list(dict(zip(keys, vs)) for vs in product(*values))
        for config in grid_product:
            for k,v in config.items():
                if isinstance(v, str) and v.startswith('sample@'):
                    param = v.lstrip('sample@')
                    config[k] = self.sampler(k, sdist[param])
        # n_trials = reduce(lambda x, y: x*y, map(len, sspace.values()))
        if sspace:
            return [{**fix, **g} for g in grid_product]
        else:
            return [{**fix}]
                
    
    @staticmethod
    def parse_dist(key, X):
        if isinstance(X, CategoricalDistribution):
            return X.choices
        elif isinstance(X, IntUniformDistribution):
            return [X.low + i*X.step for i in range((X.high - X.low) // X.step)]
        elif isinstance(X, DiscreteUniformDistribution):
            return [X.low + i * X.q for i in range(int((X.high - X.low) // X.q))]
        else:
            return [f'sample@{key}']    # all other distribution is 

    @staticmethod
    def parse_sweep(X):
        transform = Transformer.encode
        def sort_X(start, end, step=None):
            if start > end:
                return end, start, -step
            return start, end, step

        if isinstance(X, ChoiceSweep):
            lst = copy(X.list)
            X.shuffle and shuffle(lst)
            return CategoricalDistribution([x for x in map(transform, lst)])

        elif isinstance(X, RangeSweep):
            if X.shuffle:
                lst = list(X.range()); shuffle(lst)
                return CategoricalDistribution([x for x in map(transform, lst)])
            start, stop, step = sort_X(X.start, X.stop, X.step)
            if (isinstance(start, float) or isinstance(stop, float) or isinstance(step, float)):
                return DiscreteUniformDistribution(start, stop, step)
            start, stop, step = map(int, (start, stop, step))
            return IntUniformDistribution(start, stop, step)

        elif isinstance(X, IntervalSweep):
            tags, start, end, _ = X.tags, *sort_X(X.start, X.end)
            if "log" in tags:
                if isinstance(start, int) and isinstance(end, int):
                    return IntLogUniformDistribution(int(start), int(end))
                return LogUniformDistribution(start, end)
            else:
                if isinstance(start, int) and isinstance(end, int):
                    return IntUniformDistribution(start, end)
                return UniformDistribution(start, end)

          
def clear_path(path):
    (sp := path/'source_files').exists() and rmtree(sp)
    (sp := path/'experiment.db').exists() and sp.unlink()
    (sp := path/'analysis.py').exists() and sp.unlink()
    (sp := path/'logs').exists() and rmtree(sp)
    (sp := path/'checkpoint').exists() and rmtree(sp)

    
def prepare_path(path):
    def pmove(source, target):
        if oexists(target): rmtree(target)
        move(source, target)
    import tempfile
    NAME = os.path.basename(path)
    temp_dir = ojoin(tempfile.gettempdir(), NAME)
    oexists(path) and pmove(path, temp_dir)
    print(color_str(f'\nSame exp_name={NAME} detected, directory is moved to {temp_dir}. ', 'cyan', bold=True))
    omake(
        ojoin(path, 'logs'), ojoin(path, 'ckpts')
    )
    return path
    
def prepare_copy(run_copy: bool, program: Callable, log_path: Path):
    if run_copy and not check_in_ipython():
        source_path = Path(inspect.getsourcefile(program)).parent
        target_path = Path(log_path)/'source_files'
        copy_recursive(source_path, target_path)

class Grader:
    def __init__(self, metric_name, best_value=0, best_param = {}):
        self.name = metric_name
        self.best_value = best_value
        self.best_param = best_param
    def update(self, value, param):
        self.best_value = value
        self.best_param = param

def copy_recursive(source: Path, target: Path): 
    target.mkdir(exist_ok=True, parents=True)
    for item in source.iterdir():
        if item.is_dir() and not item.name.startswith('__'):
            new_target = target/item.name
            new_target.mkdir(exist_ok=True)
            copy_recursive(item, new_target)
        else:
            for file in source.glob('*.py'):
                copyfile(file, target/file.name)

def check_in_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def check_valid_config(config):
    assert isinstance(config, Args), "you have to instantiate config with dpvs.config.Args class"
    assert 'exp_name' in config, "you have to specify an experiment name"
    assert 'optim_metric' in config, "you have to specify metric key used for model comparisons"
    assert 'optim_direction' in config, "you have to specify direction to which better result is defined"
    assert 'checkpoint' in config, "you have to specify where output/logging is saved"


def write_analysis(path, logpath, name, metric_key):
    from inspect import cleandoc
    py_str = f"""
from dpvs.utils import OptunaAnalysis
study = OptunaAnalysis('{name}', 'sqlite:///{logpath}/{name}.db')
study.df
study.make_plot(category='seed', column='', y='{metric_key}')
study.make_coordinate()
    """
    with open(path, 'w') as f:
        f.write(cleandoc(py_str))