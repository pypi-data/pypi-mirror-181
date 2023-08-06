from tqdm import tqdm
from scipy.sparse import csr_matrix
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
from sklearn.ensemble import StackingRegressor, StackingClassifier

from xxnlp.skorch import MODELS, Engine
from xxnlp.utils import pickle_load, ojoin, set_directory
from xxnlp.data import Datasets
from xxnlp import Args
with set_directory():
    from constant import RAW_PATH, DATA_PATH, NER_PATH

args = Args(
    task = 'classification',
)

# ------------------------ 1. prepare data, model, engine
def load_data():
    data = pickle_load(ojoin(DATA_PATH, 'tfidf_token_data.pkl'))
    def csr_data(X):
        return csr_matrix((X.data, X.indices, X.indptr), shape=X.shape)
    return data['trainX'], data['trainY'], data['testX'], data['testY']

def load_model():
    if args.task == 'classification':
        model = StackingClassifier(
            estimators=[
                ('svc', MODELS.get('svc')(kernel='linear')),
            ], final_estimator=MODELS.get('dtree')(max_depth=1)
        )  
    elif args.task == 'regression':
        model = MODELS.get('svr')(kernel='linear')
    return model

def run_engine():
    if args.task == 'classification':
        args.update(metric='f1'); metric = {'f1': 'f1_weighted'}
        params = {
            "svc__kernel": ['rbf'], "svc__C": [1e-3,1,10], "svc__gamma": [10e-4, 10e-3, 10e-2] 
        }
    else:
        args.update(metric='mae'); metric = {'mae': 'neg_mean_absolute_error'}
        params = {
            "svr__kernel": ['rbf'], "svr__C": [1e-3,1,10], "svr__gamma": [10e-4, 10e-3, 10e-2] 
        }
    x_train, y_train, x_test, y_test = load_data()
    model = load_model()
    engine = Engine(hypopt=True, base_estimator=model, params=params, save_best=False, scoring=metric)
    engine.run(x_train, y_train, x_test, y_test)



if __name__ == '__main__':
    run_engine()