"""
Micromodels Factory
"""

from .micromodels.svm import SVM
from .micromodels.logic import LogicClassifier
from .micromodels.bert_query import BertQuery
from .micromodels.FastText import FastText

MICROMODEL_FACTORY = {
    "svm": SVM,
    "logic": LogicClassifier,
    "bert_query": BertQuery,
    "fasttext": FastText,
}
