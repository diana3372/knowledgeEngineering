# -*- coding: utf-8 -*-

import pandas as pd


class Disorder():
    def __init__(self, name):
        self.name = name
        
    def build_symptoms_dict(self, pd):
        pass


disorders_symptoms_file = 'disorders_symptoms.csv'

# Read data
disorders_symptoms_df = pd.read_csv(disorders_symptoms_file)
# Filter out columns with unnamed headers
disorders_symptoms_df = disorders_symptoms_df.loc[:, ~disorders_symptoms_df.columns.str.contains('^Unnamed')]

print(disorders_symptoms_df)


