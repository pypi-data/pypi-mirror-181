
RAW_PATH = '/home/dennisl/project/nlp-cls/data/ERISK-2/2018-t1'
DATA_PATH = '/home/dennisl/project/nlp-cls/data/ERISK'
ERISK_PATH = '/home/dennisl/project/nlp-cls/data/ERISK-2'
NER_PATH = '/home/dennisl/nlp/pretrained/ner'

SINGLE = [
    "I feel sad.",
    "I am discouraged about my future.",
    "I always fail.",
    "I don't get pleasure from things.",
    "I feel quite guilty.",
    "I expected to be punished.",
    "I am disappointed in myself.",
    "I always criticize myself for my faults.",
    "I have thoughts of killing myself.",
    "I always cry.",
    "I am hard to stay still.",
    "It's hard to get interested in things.",
    "I have trouble making decisions.",
    "I feel worthless.",
    "I don't have energy to do things.",
    "I have changes in my sleeping pattern.",
    "I am always irritable.",
    "I have changes in my appetite.",
    "I feel hard to concentrate on things.",
    "I am too tired to do things.",
    "I have lost my interest in sex."
]

ALERT = [
    "I feel depressed.",
    "I am diagnosed with depression.",
    "I am treating my depression."
]

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-roberta-large-v1')

# Two lists of sentences
sentences1 = ['The cat sits outside',
             'A man is playing guitar',
             'The new movie is awesome']

sentences2 = ['The dog plays in the garden',
              'A woman watches TV',
              'The new movie is so great']

#Compute embedding for both lists
embeddings1 = model.encode(sentences1, convert_to_tensor=True)
embeddings2 = model.encode(sentences2, convert_to_tensor=True)

#Compute cosine-similarities
cosine_scores = util.cos_sim(embeddings1, embeddings2)
print(cosine_scores)

#Output the pairs with their score
for i in range(len(sentences1)):
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))