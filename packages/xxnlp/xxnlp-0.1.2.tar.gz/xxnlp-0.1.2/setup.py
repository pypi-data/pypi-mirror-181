# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xxnlp',
 'xxnlp.configs',
 'xxnlp.data',
 'xxnlp.keras',
 'xxnlp.model',
 'xxnlp.project.erisk',
 'xxnlp.project.exp',
 'xxnlp.project.micro',
 'xxnlp.project.micro.aggregators',
 'xxnlp.project.micro.micromodels',
 'xxnlp.project.toxic',
 'xxnlp.project.toxic.data',
 'xxnlp.project.toxic.data.augmentations',
 'xxnlp.project.toxic.modelling',
 'xxnlp.project.toxic.modelling.modules',
 'xxnlp.project.toxic.utils',
 'xxnlp.project.twitter',
 'xxnlp.project.twitter.pseudodata',
 'xxnlp.skorch',
 'xxnlp.spacy',
 'xxnlp.tests.twitter',
 'xxnlp.tools',
 'xxnlp.torch',
 'xxnlp.torch.ignite',
 'xxnlp.torch.nlp',
 'xxnlp.torch.trainer',
 'xxnlp.types',
 'xxnlp.utils']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.1.0,<3.0.0',
 'deepspeed>=0.7.4,<0.8.0',
 'evaluate>=0.3.0,<0.4.0',
 'fastnlp>=1.0.1,<2.0.0',
 'fitlog>=0.9.13,<0.10.0',
 'hydra-core>=1.2.0,<2.0.0',
 'ipython>=8.6.0,<9.0.0',
 'jieba>=0.42.1,<0.43.0',
 'jsonlines>=3.1.0,<4.0.0',
 'networkx>=2.8.8,<3.0.0',
 'pyhocon>=0.3.59,<0.4.0',
 'pytest>=7.2.0,<8.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'pytorch-lightning>=1.7.7,<2.0.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'textdistance>=4.5.0,<5.0.0',
 'torchmetrics>=0.10.2,<0.11.0',
 'transformers>=4.25.1,<5.0.0']

setup_kwargs = {
    'name': 'xxnlp',
    'version': '0.1.2',
    'description': '',
    'long_description': '# XNLP\n\n首先是document embedding: 怎么把原始的一个段落/推文给转换成一个embedding, 这里有很多的Embedding模型(bert,xlnet,)和sentence-embedding模型\n\n在得到了段落的embedding基础上, 下一步是怎么把信息给整合起来, 这里可以用attn+lstm或者transformer\n',
    'author': 'dennislblog',
    'author_email': 'dennisl@udel.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
