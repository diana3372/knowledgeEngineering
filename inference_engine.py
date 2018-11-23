#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Prune_classifier:
    def __init__(self, disorders):
        self.all_disorders = disorders
        self.symptoms_so_far = []
        
    def execute(self, symptom_id, severity):
        self.symptoms_so_far.append((symptom_id, severity))
        
        candidate_disorders = self.all_disorders        
        symptom_idx = 0
        while symptom_idx < len(self.symptoms_so_far) and len(candidate_disorders) > 0:
            for candidate_idx in reversed(range(len(candidate_disorders))):
                candidate = candidate_disorders[candidate_idx]
                current_symptom_id, value = self.symptoms_so_far[symptom_idx]
                # Is exact match
                if candidate.symptom_id_to_severity[current_symptom_id] == value:
                    continue
                
                # Is not an exact match but the symptom is not that severe, so cannot discard
                if candidate.symptom_id_to_severity[current_symptom_id] == 2:
                    continue
                
                # Discard this candidate disorder
                candidate_disorders.pop()
                print('Rulin out {}'.format(candidate.name))
            
            symptom_idx += 1
                