from sklearn.model_selection import PredefinedSplit, GridSearchCV
from sklearn.metrics._scorer import _MultimetricScorer
import numpy as np
import pandas as pd

from xxnlp.data import Datasets
from xxnlp.utils import Logger, pickle_dump

log = Logger.get()

def get_predefined_split(x_train, y_train, x_val, y_val):
    test_fold = np.concatenate([-np.ones_like(y_train), np.zeros_like(y_val)])
    ps = PredefinedSplit(test_fold)
    x = np.concatenate([x_train, x_val], axis=0)
    y = np.concatenate([y_train, y_val], axis=0)
    return ps, (x,y)

metrics = {
    'mae': 'neg_mean_absolute_error',
    "auc": "roc_auc", 
    "f1": "f1", 
    'prec': 'precision', 
    'rec': 'recall'
}

class Engine:

    scoring = {"auc": "roc_auc", "f1": "f1", 'prec': 'precision', 'rec': 'recall'}

    def __init__(self, hypopt, params, base_estimator, save_best, optim_metrics='f1', n_jobs=1, scoring=None):
        params = {} if not hypopt else dict(params) #disable hyperparameter search
        self.gs = Search(base_estimator, param_grid=params, scoring=scoring or self.scoring, refit=optim_metrics, n_jobs=n_jobs, return_train_score=True, error_score='raise')
        self.estimator = base_estimator
        self.params = params
        self.save_best = save_best
        
    @property
    def estname(self):
        return self.gs.estimator.__class__.__name__
    
    def run( self, datasets: Datasets, checkpoint: str = ''):
        ps, [x_train, y_train] = get_predefined_split(*datasets.train, *(datasets.val or datasets.test))
        self.gs.cv = ps
        self.gs.fit(x_train, y_train)
        perf = self.gs.evaluate(*datasets.test)
        log.info('Model Performance: \n' + perf.to_string() + '\n')
        if self.save_best and checkpoint:
            try:
                log.info(f'Save best model {self.estname}{self.gs.best_params_} to {checkpoint}')
                pickle_dump(self.gs.best_estimator_, checkpoint)
            except OSError: pass # start training from scratch
    
    def run(self, x_train, y_train, x_test, y_test):
        self.gs.fit(x_train, y_train)
        perf = self.gs.evaluate(x_test, y_test)
        log.info('Model Performance: \n' + perf.to_string() + '\n')

        
class Search(GridSearchCV):

    # def _run_search(self, evaluate_candidates): pass
    def _format_results(self, candidate_params, n_splits, out, more_results=None):
        self.results = [{"params": p, **d} for p,d in zip(candidate_params, out)]
        return super()._format_results(candidate_params, n_splits, out, more_results)

    def evaluate(self, X_test, y_test):
        score = _MultimetricScorer(**self.scorer_)
        for record in self.results:
            record['val_scores'] = record.pop('test_scores')
            record['test_scores'] = score(record.pop('estimator'), X_test, y_test)
        df = pd.DataFrame(
            [{(k.rstrip('_scores'),k1): v1 for k, v in x.items() if k.endswith('_scores') for k1, v1 in v.items()} for x in self.results]
        )
        params = pd.DataFrame.from_records([x['params'] for x in self.results])
        if params.size > 0:
            df = df.join(params).set_index(list(params.columns))
        return df.sort_values(by=[('test', self.refit), ('val', self.refit)], ascending=False)


class Repeat:

    def __init__(self, cv, n_repeats=10, random_state=None):
        self.cv = cv
        self.n_repeats = n_repeats
        
    def split(self, X, y=None, groups=None):
        n_repeats = self.n_repeats
        cv = self.cv
        for idx in range(n_repeats):
            for train_index, test_index in cv.split(X, y, groups):
                yield train_index, test_index
                
    def get_n_splits(self, X=None, y=None, groups=None):
        cv = self.cv
        return cv.get_n_splits(X, y, groups) * self.n_repeats
