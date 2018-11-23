# -*- coding: utf-8 -*-

import random
from knowledge_base_loader import KB_loader

# Load knowledge base
loader = KB_loader()

# System run
print('Answer to each question with a Yes(Y) or No(N) according to whether the symptom is present in the patient.\n')

# First shuffle questions
symptom_question_tuples = list(loader.symptom_id_to_question.items())
random.shuffle(symptom_question_tuples)

n_questions = 5
count_questions = 0

present_symptoms = []
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
        present_symptoms.append(symptom_id)
        
    count_questions += 1
    if count_questions == n_questions:
        break
    
print([loader.id_to_symptom_name[x] for x in present_symptoms])
