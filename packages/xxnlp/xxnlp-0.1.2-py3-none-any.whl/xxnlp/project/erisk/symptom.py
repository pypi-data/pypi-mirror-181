#%% ----- first we need to obtain data?
import os, re, json, rdflib as R
import numpy as np 
import pandas as pd 
from tqdm import tqdm
from collections import defaultdict
from xxnlp.utils import ojoin, set_directory

with set_directory():
    from constant import DATA_PATH
# %% --- obtain graph?

g = R.Graph()
g.parse(ojoin(DATA_PATH, "assets/symptom_kg.owl"), format="turtle")
ns = R.Namespace("http://www.semanticweb.org/admin/ontologies/2021/10/untitled-ontology-8#")
ns2 = R.Namespace("http://www.w3.org/2002/07/owl#")
ns3 = R.Namespace("http://www.w3.org/2000/01/rdf-schema#")

diseases = list(g.subjects(R.RDF.type, ns["Mental_Disease"]))

# %% --- disease ID --> symptom?
# 焦虑、双相情感障碍、抑郁、饮食失调..
def get_uri_name(x):
    return x[len("http://www.semanticweb.org/admin/ontologies/2021/10/untitled-ontology-8#"):]
def get_desc_symp(x):
    descs = sorted(list(g.objects(ns[x], ns["Subsymptoms"])))
    return map(str, descs)
def get_desc_range():
    desc_from_post, id2desc, left = {}, [], 0
    id2desc_range = [[0, 0] for symp in id2symptoms]
    for i, symp in enumerate(id2symptoms):
        descs = desc_from_post.get(symp, get_desc_symp(symp))
        id2desc.extend(descs)
        id2desc_range[i] = [left, len(id2desc)]
        left = len(id2desc)
    return id2desc_range, id2desc

id2disease = [ 'adhd', 'anxiety', 'bipolar_disorder', 'depression', 'eating_disorder', 'ocd', 'ptsd', ]
disease2id = {x:i for i, x in enumerate(id2disease)}
symptoms = sorted(list(g.subjects(R.RDF.type, ns["Symptom"])))
id2symptoms = [get_uri_name(x) for x in symptoms]
symptom2id = {x:i for i, x in enumerate(id2symptoms)}
symptoms2range, id2desc = get_desc_range()

# %% --- example disease? depression?
# 抑郁: 心动过速、心悸、胸痛、血管搏动、昏厥感、心跳丢失
symp = 'depression'
symp_id = disease2id[symp]
st, ed = symptoms2range[symp_id]
desc = f"Symptoms to describe {symp}: \n" + '\n'.join(['{}. {}'.format(i, x) for i,x in enumerate(id2desc[st: ed], start=1)])
print(desc)

# %% --- symptom -> disease?
def get_symp2disease():
    symp_id2disease_ids = [[] for i in range(len(id2symptoms))]
    for symptom in symptoms:
        diseases = list(get_uri_name(x).lower() for x in g.objects(symptom, ns['IsSymptomOf']))
        symp = get_uri_name(symptom)
        print(f"Symptom [{symp}]: {diseases}")
        symp_id2disease_ids[symptom2id[symp]] = [disease2id[d] for d in diseases]
    return symp_id2disease_ids

symp_id2disease_ids = get_symp2disease()
# %%
