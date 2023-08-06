import requests, itertools
from functools import partial
from tokenizers import Encoding
from typing import List

class LDTSession(requests.Session):
    def __init__(self, domain:str,user:str,pwd:str,host:str=None):
        """[summary]
        Initializes a LightTag API session object
        Arguments:
            domain {str} -- [The name of your workspace]
            user {str} -- [Your LightTag Username]
            pwd {str} -- [Your LightTag password]
        Keyword Arguments:
            host {str} -- [Optional, use this when self hosting LightTag ] (default: {None})
        """
        super().__init__()
        if host is None:
            host = 'https://{domain}.lighttag.io/api/'.format(domain=domain)
        token =self._authenticate(host,user,pwd)
        self.headers.update({"Authorization":"Token {token}".format(token=token)})
        def new_request(f, method, url, *args, **kwargs):
            if '://' not in url:  
                return f(method,host + url, *args, **kwargs)  
            else:
                return f(method,url,*args,**kwargs)
        self.request = partial(new_request, self.request)
        def check_for_errors(resp,*args,**kwargs):
            resp.raise_for_status()
        self.hooks['response'] = [check_for_errors]
        # self.report()

    @property
    def annotators(self):
        "id,username,email,is_active,is_manager,is_reviewer,teams,name"
        annotators = self.get('v1/projects/default/annotators/').json()
        return {x['name']: x for x in annotators}
    
    @property
    def team(self):
        "name, slug, description, id, url, memebers"
        teams = self.get('v1/projects/default/teams/').json()
        return {x['name']: x for x in teams}

    @property
    def schema(self):
        "id, slug, url, name, editable"
        schemas = self.get('v1/projects/default/schemas/').json()
        return {x['name']: x for x in schemas}

    @property
    def dataset(self):
        "id, url, name, id_field, content_field, aggregation_field, order_field, project_id, upload_status, archived, editable"
        datasets = self.get('v1/projects/default/datasets/').json()
        return {x['name']: x for x in datasets}

    @property
    def task(self):
        tasks = self.get('v1/projects/default/task_definitions/').json()
        return {x['name']: x for x in tasks}

    def set_team(self, name):
        if name in self.team: return
        team = {"name":name, "description": name, "members":[self.annotators['cate.wl.zhang@gmail.com']]}
        self.post('v1/projects/default/teams/', json=team)

    def set_task(self, task_name, data_name, is_classification=True):
        if task_name in self.task: return task_name
        if is_classification:
            schema = 'depression-classification-only'
        else:
            schema = 'depress-annotation-tag-only'
        task = {
            "name": task_name,
            "dataset_slug": self.dataset[data_name]['slug'],
            "annotators_per_example":1,
            "schema_slug": schema,
            "allow_suggestions":False,
            "guidelines": guideline_templates,
            "teams": [self.team['Manager']['id']],
            "models":[]
        }
        self.post('v1/projects/default/task_definitions/',json=task)
        return task_name

    def set_data(self, data, name, field='text', group=None):
        if name in self.dataset: return name
        data =  {
            "name": name,
            "content_field": field, # text is the field in the JSON we will be annotating
            "examples": data,# Set the list of examples that are part of this dataset
        }
        if group: data.update({'aggregation_field': group})
        self.post('v1/projects/default/datasets/bulk/',json=data)
        return name

    @staticmethod
    def _authenticate(host:str,user:str,pwd:str):
        """Fetches authentication token based on username password
        Arguments:
            host {str} -- [Fully qualified host name]
            user {str} -- [LightTag Username]
            pwd {str} -- [LightTag Password]
        """
        response = requests.post(host+'auth/token/login/',json={"username":user,"password":pwd})
        response.raise_for_status()
        auth_details = response.json()
        token = auth_details['key']
        assert auth_details['is_manager'] ==1, "not a manager" # Check you are a manager
        return token

    def report(self):
        metrics = self.get('v1/projects/default/task_definitions/metrics/').json()
        for metric in metrics:
            if not metric['definition']['archived']:
                name, finish, total = metric['definition']['slug'], metric['complete_tasks'], metric['total_tasks']        
                print(f'{name:>10} {finish:>3}/{total} finish')

def align_tokens_and_annotations_bilou(tokenized: Encoding, annotations):
    tokens = tokenized.tokens
    aligned_labels = ["O"] * len(
        tokens
    )  # Make a list to store our labels the same length as our tokens
    for anno in annotations:
        annotation_token_ix_set = ( set() )  # A set that stores the token indices of the annotation
        for char_ix in range(anno["start"], anno["end"]):
            token_ix = tokenized.char_to_token(char_ix)
            if token_ix is not None:
                annotation_token_ix_set.add(token_ix)
        if len(annotation_token_ix_set) == 1: # If there is only one token
            token_ix = annotation_token_ix_set.pop()
            prefix = ( "U"  ) # This annotation spans one token so is prefixed with U for unique
            aligned_labels[token_ix] = f"{prefix}-{anno['tag']}"

        else:
            last_token_in_anno_ix = len(annotation_token_ix_set) - 1
            for num, token_ix in enumerate(sorted(annotation_token_ix_set)):
                if num == 0:
                    prefix = "B"
                elif num == last_token_in_anno_ix:
                    prefix = "L"  # Its the last token
                else:
                    prefix = "I"  # We're inside of a multi token annotation
                aligned_labels[token_ix] = f"{prefix}-{anno['tag']}"
    return aligned_labels

class LabelSet:
    def __init__(self, labels: List[str]):
        self.labels_to_id = {}
        self.ids_to_label = {}
        self.labels_to_id["O"] = 0
        self.ids_to_label[0] = "O"
        num = 0  # in case there are no labels
        # Writing BILU will give us incremntal ids for the labels
        for _num, (label, s) in enumerate(itertools.product(labels, "BILU")):
            num = _num + 1  # skip 0
            l = f"{s}-{label}"
            self.labels_to_id[l] = num
            self.ids_to_label[num] = l

    def get_aligned_label_ids_from_annotations(self, tokenized_text, annotations):
        raw_labels = align_tokens_and_annotations_bilou(tokenized_text, annotations)    
        return list(map(self.labels_to_id.get, raw_labels))


guideline_templates = """
## Task Guidelines

## Overview

> Welcome! In this task, we request you to tag labels on social media posts. We will use the labeled dataset to build a learning model to help identify depressed users on social media platforms and give them early guidance.

## Concepts

> Depression is a common mental illness that involves sadness and lack of interest in all day-to-day activities [1,2]. Detecting depression is important because severe consequences may be avoided if depression can be identified and treated early [3]. 

> The life events/symptoms/treatments reported are usually phrases (e.g., hit myself, back in therapy). The labels should be **the most concise phrase. Please do not include meaningless words (e.g., it’s)**. 

## Your Contribution

> We'd like you to tag specific words and phrases in a social media post, such as **Life Events** that may cause or exacerbate depression, **Symptoms** that signal depression, and **Treatments** for depression. If there are multiple Life Events/Symptoms/Treatments reported or if there are multiple phrases about similar Life events/Symptoms/Treatments, **please annotate all of them**.  

> Please click a tag and highlight any text in the social media post. One social media post may have multiple tags. You can press **l/s/t** on your keyboard to quickly switch the choice of tags.
> 
> ![](https://i.imgur.com/bOQ6BkP.png)

> You can always go back to change your annotations. However, you **may not** go back to make changes once you have submitted your work and logged out.  
> 
> ![](https://i.imgur.com/uu9cM0Z.png)

> You can delete your annotation by clicking on the text and deleting it.
>
> ![](https://i.imgur.com/UGTywAF.png)

> Feel free to log out and come back to continue your work. But please don't forget to **Submit** your work for each task before jumping to the next. **Otherwise, your annotations won't be saved and uploaded**.
>
> ![](https://i.imgur.com/qkojznl.png)

> Click **GUIDELINES** to see this page. The number (e.g., **2493 Assigned**) to its left shows how many social media posts are left to be annotated and submitted. 
>
> ![](https://i.imgur.com/NbB60KC.png)

## Background knowledge 
### life events  
> life events that may cause or exacerbate depression, for example,  
- dealing with crisis  
- divorce  
- person safe  
- loss of job  
- alcohol use disorder  
- drug use disorder  
- body weight  
- body shape  
- medication  
- domestic violence  
- emotional abuse  
- family violence  
- food  
- history of self-harm  
- history of violence  
- insomnia  
- life management  
- presence of abuse  
- presence of emotional support  
- psychiatric admission  
- sexual abuse  
- neglect  

### symptoms  
> depression symptoms, for example,   
- anxiety   
- psychotic behavior   
- mood: worry  
- mood: low mood  
- mood: anhedonia  
- mood: guilt  
- mood: concentration problems  
- mood: reduced self-esteem  
- mood: pessimistic thoughts  
- physical symptoms: change in appetite  
- physical symptoms: weight loss  
- physical symptoms: change in sleep  
- physical symptoms: change in activities  
- physical symptoms: change in fatigue  
- suicidality: suicide attempt  
- suicidality: thoughts of suicide  
- suicidality: suicide plan  
- suicidality: self-harm  
- suicidality: completed suicide  
- response to medication: remission  
- response to medication: good response  
- response to medication: minimal response  
- response to medication: non-response  
- adverse side-effects of medication: nausea  
- adverse side-effects of medication: headache  
- adverse side-effects of medication: dry mouth  
- adverse side-effects of medication: insomnia  
- adverse side-effects of medication: dizziness  
- adverse side-effects of medication: sedation/somnolence  
- adverse side-effects of medication: diarrhea  
- adverse side-effects of medication: constipation  
- adverse side-effects of medication: sexual dysfunction  
- adverse side-effects of medication: fatigue  

## treatments
> depression treatmens: medication (dosage / frequency / duration (start / ongoing / stop / dose up / dose down))  
- Abilify (aripiprazole) – an antipsychotic medication used in combination with an antidepressant  
- Adapin (doxepin)  
- Anafranil (clomipramine)  
- Aplenzin (bupropion)  
- Asendin (amoxapine)  
- Aventyl HCI (nortriptyline)  
- Brexipipzole (Rexulti) - an antipsychotic medication used in combination with an antidepressant”  
- Celexa (citalopram)  
- Cymbalta (duloxetine)  
- Desyrel (trazodone)  
- Effexor XR (venlafaxine)  
- Emsam (selegiline)  
- Esketamine (Spravato)  
- Etrafon (perphenazine and amitriptyline)  
- Elavil (amitriptyline)  
- Endep (amitriptyline)  
- Fetzima (levomilnacipran)  
- Khedezla (desvenlafaxine)  
- Latuda (lurasidone) -- an atypical antipsychotic drug used to treat bipolar depression  
- Lamictal (lamotrigine) -- an anticonvulsant drug sometimes used to treat or prevent bipolar depression  
- Lexapro (escitalopram)  
- Limbitrol (amitriptyline and chlordiazepoxide)  
- Marplan (isocarboxazid)  
- Nardil (phenelzine)  
- Norpramin (desipramine)  
- Oleptro (trazodone)  
- Pamelor (nortriptyline)  
- Parnate (tranylcypromine)  
- Paxil (paroxetine)  
- Pexeva (paroxetine)  
- Prozac (fluoxetine)  
- Pristiq (desvenlafaxine)  
- Remeron (mirtazapine)  
- Sarafem (fluoxetine)  
- Seroquel XR (quetiapine) -- an antipsychotic medication used in combination with antidepressants for treating bipolar depression  
- Serzone (nefazodone)  
- Sinequan (doxepin)  
- Surmontil (trimipramine)  
- Symbyax (fluoxetine and the atypical antipsychotic drug olanzapine)  
- Tofranil (imipramine)  
- Triavil (perphenazine and amitriptyline)  
- Trintelllix (vortioxetine)  
- Viibryd (vilazodone)  
- Vivactil (protriptyline)  
- Wellbutrin (bupropion)  
- Zoloft (sertraline)  
- Zyprexa (olanzapine) -- an antipsychotic medication used in combination with an antidepressant

## Thank You Again for Participating in this Meaningful Research Project! 😃

## Reference

[1] [Institute of Health Metrics and Evaluation. Global Health Data Exchange (GHDx)](http://ghdx.healthdata.org/gbd-results-tool?params=gbd-api-2019-permalink/d780dffbe8a381b25e1416884959e88b)

[2] Evans-Lacko S, Aguilar-Gaxiola S, Al-Hamzawi A, et al. Socio-economic variations in the mental health treatment gap for people with anxiety, mood, and substance use disorders: results from the WHO World Mental Health (WMH) surveys. Psychol Med. 2018;48(9):1560-1571.

[3] Losada, D. E., Crestani, F., & Parapar, J. (2017, September). eRISK 2017: CLEF lab on early risk prediction on the internet: experimental foundations. In the International Conference of the Cross-Language Evaluation Forum for European Languages (pp. 346-360). Springer, Cham.
"""