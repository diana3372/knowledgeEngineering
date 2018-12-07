#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Prune_classifier:
    def __init__(self, all_disorders):
        self.candidate_disorders = all_disorders.copy()

    def execute(self, symptom_id, severity, symptom_id_to_questions_left):        
        if len(self.candidate_disorders) > 1:
            for candidate_idx in reversed(range(len(self.candidate_disorders))):
                candidate = self.candidate_disorders[candidate_idx]
                expected_value = candidate.symptom_id_to_severity[symptom_id]
                
                if self.match(severity, expected_value) or symptom_id_to_questions_left[symptom_id] > 0:
                    continue
                
                # Discard this candidate disorder
                self.candidate_disorders.remove(candidate)
                
    def match(self, value, expected_value):
        # It is exact match
        if expected_value == value:
            return True
        
        # It is not an exact match but the symptom is not that severe, so cannot discard
        if abs(expected_value - value) <= 1:
            return True
        
        # Do not rule out because of extra symptoms
        if value > expected_value and expected_value - value <= 2:
            return True

        return False