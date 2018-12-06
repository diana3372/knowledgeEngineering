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
print('Answer to each question with True(T) or False(F) according to whether the symptom is present in the patient.\n')

all_symptom_questions = loader.symptom_id_to_questions.items()
# Convert list of questions to single question per symptom
symptom_question_tuples = reduce(lambda x,y: x+y, map(lambda x: [(x[0], s) for s in x[1]], all_symptom_questions))

# Shuffle questions
random.shuffle(symptom_question_tuples)

symptom_id_to_questions_left = {k:len(v) for (k, v) in loader.symptom_id_to_questions.items()}

n_questions = 150 #163
count_questions = 0

for symptom_id, question in symptom_question_tuples:
    if symptom_id_to_questions_left[symptom_id] == 0:
        continue

    print()
    print(question)
    while True:   
        answer = input('True/False >> ')
        answer = answer.lower()
        if answer not in ['true', 'false', 't', 'f', 'yes', 'no', 'y', 'n']:
            print('Incorrect input. Please answer True or False')
        else:
            break
    
    if 't' in answer or 'y' in answer:
        severity = MAX_SEVERITY_VALUE
        # Do not ask repeated questions for the same symptom
        symptom_id_to_questions_left[symptom_id] = 0
    else:
        severity = MIN_SEVERITY_VALUE
        symptom_id_to_questions_left[symptom_id] -= 1
        
    classifier.execute(symptom_id, severity, symptom_id_to_questions_left)
    
    results = classifier.candidate_disorders
    if len(results) == 0:
        results = [loader.disorders[-1]]
        break
    elif len(results) == 1:
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
    
