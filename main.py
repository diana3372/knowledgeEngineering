# -*- coding: utf-8 -*-

import random
from functools import reduce

from knowledge_base_loader import KB_loader
from inference_engine import Prune_classifier

MAX_SEVERITY_VALUE = 4
MIN_SEVERITY_VALUE = 0

# Load knowledge base
loader = KB_loader()

# Initialize inference process
classifier = Prune_classifier(loader.disorders, loader)

# System run
print('Answer to each question with a Yes(Y) or No(N) according to whether the symptom is present in the patient.\n')

all_symptom_questions = loader.symptom_id_to_questions.items()
# Convert list of questions to single question per symptom
symptom_question_tuples = reduce(lambda x,y: x+y, map(lambda x: [(x[0], s) for s in x[1]], all_symptom_questions))

# Shuffle questions
random.shuffle(symptom_question_tuples)

n_questions = 1000
count_questions = 0

for symptom_id, question in symptom_question_tuples:
    print()
    print(question)
    while True:   
        answer = input('Yes/No >> ')
        answer = answer.lower()
        if answer not in ['yes', 'no', 'y', 'n']:
            print('Incorrect input. Please answer Yes or No')
        else:
            break
    
    if 'y' in answer:
        severity = MAX_SEVERITY_VALUE
    else:
        severity = MIN_SEVERITY_VALUE
        
    classifier.execute(symptom_id, severity)
    
    results = classifier.candidate_disorders
    if len(results) == 0:
        results = [loader.disorders[-1]]
        break
        
    count_questions += 1
    if count_questions == n_questions:
        break

print()
print('========================================================================')
print()
print()

if len(results) == 1:
    print('Anxiety disorder is classified as: {}'.format(results[0].name))    
else:
    print('Anxiety disorder type is narrowed down to one of the following:')
    for r in results:
        print(r.name)
    
