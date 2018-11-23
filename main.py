# -*- coding: utf-8 -*-

import pandas as pd
import random

class Disorder:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def build_symptoms_dict(self, symptoms, symptoms_ids):
        self.symptoms_dict = {}
        for s_id, item in enumerate(symptoms.iteritems()):
            s, v = item
            assert s == symptoms_ids[s_id], 'Wrong mapping symptom to id'
            self.symptoms_dict[s_id] = v # dictionary symptom id to severity

kb_folder = 'knowledge_base'
symptoms_ids_file = '{}/symptoms_to_id.csv'.format(kb_folder)
disorders_symptoms_file = '{}/disorders_symptoms.csv'.format(kb_folder)
symptoms_questions_file = '{}/symptoms_to_questions.csv'.format(kb_folder)

# Load symptoms ids
symptoms_ids_df = pd.read_csv(symptoms_ids_file, header=None)
symptoms_ids = {} # dictionary id to symptom name
for row in symptoms_ids_df.iterrows():
    row_data = row[1]
    name = row_data[0]
    id = row_data[1]
    symptoms_ids[id] = name


# Read data
disorders_symptoms_df = pd.read_csv(disorders_symptoms_file)
# Filter out columns with unnamed headers
disorders_symptoms_df = disorders_symptoms_df.loc[:, ~disorders_symptoms_df.columns.str.contains('^Unnamed')]

disorders = []
for disorder_count, row in enumerate(disorders_symptoms_df.iterrows()):
    row_data = row[1]
    disorder_name = row_data[0]
    symptoms = row_data[1:]
    disorder = Disorder(disorder_name, disorder_count)
    disorder.build_symptoms_dict(symptoms, symptoms_ids)
    disorders.append(disorder)
    
# UT
#disorder_key = 2
#disorder = disorders[disorder_key]
#print(disorder.name)
#print(disorder.id)
#symptom_key = 1
#print(symptoms_ids[symptom_key])
#print(disorder.symptoms_dict[symptom_key])

symptoms_questions_df = pd.read_csv(symptoms_questions_file)
# Grab the first question for now
symptoms_questions_df = symptoms_questions_df.filter(['Symptom', 'Questions'])

symptoms_to_questions = {} #dictionary symptom id to question
for symptom_id, row in enumerate(symptoms_questions_df.iterrows()):
    row_data = row[1]
    question = row_data[1]
    symptoms_to_questions[symptom_id] = question
    

# System run
print('Answer to each question with a Yes(Y) or No(N) according to whether the symptom is present in the patient.\n')

# First shuffle questions
symptom_question_tuples = list(symptoms_to_questions.items())
random.shuffle(symptom_question_tuples)

n_questions = 5
count_questions = 0

present_symptoms = []
for symptom_id, question in symptom_question_tuples:
    print(question)
    while True:   
        answer = input('Yes/No >> ')
        answer = answer.lower()
        if answer not in ['yes', 'no', 'y', 'n']:
            print('Incorrect input. Please answer Yes or No')
        else:
            break
    
    if 'y' in answer:
        present_symptoms.append(symptom_id)
        
    count_questions += 1
    if count_questions == n_questions:
        break
    
print([symptoms_ids[x] for x in ypresent_symptoms])
