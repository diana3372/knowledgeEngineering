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
classifier = Prune_classifier(loader.disorders)

# System run
print('Answer to each question with a value according to whether the symptom is present in the patient. {} is not present at all, {} is the most severe.\n'.format(
    MIN_SEVERITY_VALUE, MAX_SEVERITY_VALUE))

all_symptom_questions = loader.symptom_id_to_questions.items()
# Convert list of questions to single question per symptom
symptom_question_tuples = reduce(lambda x,y: x+y, map(lambda x: [(x[0], s) for s in x[1]], all_symptom_questions))

# Shuffle questions
random.shuffle(symptom_question_tuples)

symptom_id_to_questions_left = {k:len(v) for (k, v) in loader.symptom_id_to_questions.items()}


for symptom_id, question in symptom_question_tuples:
    if symptom_id_to_questions_left[symptom_id] == 0:
        continue

    print()
    print(question)
    while True:   
        answer = input('Severity>> ')
        if not answer.isdigit() or int(answer) not in range(5):
            print('Incorrect input. Please input a number from 0 to 4')
        else:
            break

    answer = int(answer)
    
    if answer == MAX_SEVERITY_VALUE or answer == MAX_SEVERITY_VALUE - 1:
        # Do not ask repeated questions for the same symptom
        # if we already know it is strongly present
        symptom_id_to_questions_left[symptom_id] = 0
    else:
        symptom_id_to_questions_left[symptom_id] -= 1
        
    # Run inference
    classifier.execute(symptom_id, answer, symptom_id_to_questions_left)
    
    results = classifier.candidate_disorders

    # Break if we already ruled out enough
    if len(results) == 0:
        results = [loader.disorders[-1]]
        break
    elif len(results) == 1:
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
    
