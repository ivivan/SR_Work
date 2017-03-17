import os
import pandas as pd
import multiprocessing


def results_dataframe_counts(odarray):
    """Table View Results, O, D, C"""
    title = ('Origin', 'Destination','Distance','PrimaryServiceProviderCode')
    df = pd.DataFrame(odarray, columns=list(title))
    group_df = df.groupby(['Origin', 'Destination']).size().reset_index(name='Count')
    sorted_df = group_df.sort_values(by='Count', ascending=0).reset_index(drop=True)
    return sorted_df

def results_dataframe_all(odarray):
    """Table View Results, O, D, D, I, T, P"""
    title = ('Origin', 'Destination','Distance','PrimaryServiceProviderCode')
    df = pd.DataFrame(odarray, columns=list(title))
    return df

def output_group(results,filepath):
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    outputfiledir = os.path.abspath(os.path.join(filedir, 'DataBase', name))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)
    csvfile = os.path.join(outputfiledir, name + '.csv')
    result = results_dataframe_counts(results)
    resultforDB = results_dataframe_all(results)
    print(result.to_string())
    print(resultforDB.to_string())
    resultforDB.to_csv(csvfile, sep=',', encoding='utf-8')

if __name__ == '__main__':
    multiprocessing.freeze_support()