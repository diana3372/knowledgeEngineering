#!/usr/bin/env python3
# -*- coding: utf-8 -*-

DEFAULT_DISORDER_ID = 11

class Prune_classifier:
    def __init__(self, all_disorders, loader):
        self.candidate_disorders = all_disorders.copy()
        self.symptoms_so_far = []
        
        self.loader = loader
        
    def execute(self, symptom_id, severity):
        self.symptoms_so_far.append((symptom_id, severity))
                
        symptom_idx = 0
        while symptom_idx < len(self.symptoms_so_far) and len(self.candidate_disorders) > 1:
            for candidate_idx in reversed(range(len(self.candidate_disorders))):
                candidate = self.candidate_disorders[candidate_idx]
                current_symptom_id, value = self.symptoms_so_far[symptom_idx]
                expected_value = candidate.symptom_id_to_severity[current_symptom_id]
                
                if self.match(value, expected_value):
                    continue
                
                # Discard this candidate disorder
                self.candidate_disorders.remove(candidate)
                print('(Ruling out {} because symptom [{}]{} was {} and not {})'.format(
                        candidate.name, 
                        current_symptom_id,
                        self.loader.id_to_symptom_name[current_symptom_id],
                        value,
                        expected_value))
                print('{} disorders left'.format(len(self.candidate_disorders)))
            
                if len(self.candidate_disorders) == 2 and DEFAULT_DISORDER_ID in [dis.id for dis in self.candidate_disorders]:
                    if self.candidate_disorders[0].id == DEFAULT_DISORDER_ID:
                        candidate = self.candidate_disorders[0]
                    else:
                        candidate = self.candidate_disorders[1]
                    self.candidate_disorders.remove(candidate)

            symptom_idx += 1

                
    def match(self, value, expected_value):
        # It is exact match
        if expected_value == value:
            return True
        
        # It is not an exact match but the symptom is not that severe, so cannot discard
        if abs(expected_value - value) < 4:
            return True
        
        # Do not rule out because of extra symptoms
        if value > expected_value:
            return True

        return False