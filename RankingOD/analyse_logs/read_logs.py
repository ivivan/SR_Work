import pandas as pd
from RankingOD.prepare_logs import output_logs as ol

def read_csv(filepath):
    df = pd.read_csv(filepath)
    return df

def calculate_count(dataframe):
    df = ol.results_dataframe_counts(dataframe)
    return df

if __name__  == '__main__':
    read_csv(r'C:\Logs\DataBase\20170310\ZIP.csv')


