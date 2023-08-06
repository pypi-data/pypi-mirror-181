from xxnlp import Registry
from xxnlp.utils import Logger, pickle_load
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression 
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from xgboost import XGBClassifier

log = Logger.get()

MODELS = Registry("model:sklearn")

for name, func in {
    "svc": SVC,
    "svr": SVR,
    "lda": LDA,
    "rforest":  RandomForestClassifier,
    "gboost":  GradientBoostingClassifier,
    "knn": KNeighborsClassifier,
    "adboost": AdaBoostClassifier,
    "logistic": LogisticRegression,
    "dtree": DecisionTreeClassifier,
    "xgboost": XGBClassifier,
}.items():
    MODELS(func, name)


def make_model(name, load_best, checkpoint):
    if load_best and checkpoint:
        try:
            log.info(f'Checkpoint set to {checkpoint}')
            return pickle_load(checkpoint)
        except OSError: pass # start training from scratch
    return MODELS.get(name)
    