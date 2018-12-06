#!/usr/bin/env python3
# -*- coding: utf-8 -*-

DEFAULT_DISORDER_ID = 11

class Prune_classifier:
    def __init__(self, all_disorders, loader):
        self.candidate_disorders = all_disorders.copy()
        self.symptoms_so_far = []
        
        self.loader = loader

    def execute(self, symptom_id, severity, symptom_id_to_questions_left):
        self.symptoms_so_far.append((symptom_id, severity))
        
        if len(self.candidate_disorders) > 1:
            for candidate_idx in reversed(range(len(self.candidate_disorders))):
                candidate = self.candidate_disorders[candidate_idx]
                expected_value = candidate.symptom_id_to_severity[symptom_id]
                
                if self.match(severity, expected_value) or symptom_id_to_questions_left[symptom_id] > 0:
                    if not self.match(severity, expected_value):
                        print('Not ruling out {} for symptom {}'.format(candidate.name, symptom_id))
                    continue
                
                # Discard this candidate disorder
                self.candidate_disorders.remove(candidate)
                print('(Ruling out {} because symptom [{}]{} was {} and not {})'.format(
                        candidate.name, 
                        symptom_id,
                        self.loader.id_to_symptom_name[symptom_id],
                        severity,
                        expected_value))
                print('{} disorders left'.format(len(self.candidate_disorders)))
            
                if len(self.candidate_disorders) == 2 and DEFAULT_DISORDER_ID in [dis.id for dis in self.candidate_disorders]:
                    if self.candidate_disorders[0].id == DEFAULT_DISORDER_ID:
                        candidate = self.candidate_disorders[0]
                    else:
                        candidate = self.candidate_disorders[1]
                    self.candidate_disorders.remove(candidate)

                
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