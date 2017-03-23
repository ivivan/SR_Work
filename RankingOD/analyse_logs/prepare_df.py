import pandas as pd
import os


def read_csv(filepath):
    df = pd.read_csv(filepath)
    return df


def results_dataframe_counts(odarray):
    """Log info in dataframe, O, D, Count"""
    title = ('Origin', 'Destination', 'Distance', 'PrimaryServiceProviderCode')
    df = pd.DataFrame(odarray, columns=list(title))
    group_df = df.groupby(['Origin', 'Destination']).size().reset_index(name='Count')
    sorted_df = group_df.sort_values(by='Count', ascending=0).reset_index(drop=True)
    return sorted_df


def results_dataframe_all(odarray):
    """Log info in dataframe, O, D, D P"""
    title = ('Origin', 'Destination', 'Distance', 'PrimaryServiceProviderCode')
    df = pd.DataFrame(odarray, columns=list(title))
    return df


def output_df(filepath):
    """save new csv with count"""
    result = pd.read_csv(filepath)
    log_count = results_dataframe_counts(result)
    filedir,name = os.path.split(filepath)
    name, ext = os.path.splitext(name)
    csvfile = os.path.join(filedir, name+'_count' + '.csv')
    log_count.to_csv(csvfile, sep=',', encoding='utf-8', index=False)  # csv for OD pairs, distance and servic eprovider code


if __name__ == '__main__':
    output_df(r'C:\work\project\logprocess\join_logs\20170310\20170310.csv')



