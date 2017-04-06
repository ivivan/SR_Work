import pandas as pd
import os


def read_csv(filepath):
    df = pd.read_csv(filepath)
    return df


def results_dataframe_counts(odarray,filename):
    """Log info in dataframe, O, D, Count"""
    title = ('Origin', 'Destination', 'Time', 'Distance', 'PrimaryServiceProviderCode', 'Date')
    df = pd.DataFrame(odarray, columns=list(title))
    group_df = df.groupby(['Origin', 'Destination']).size().reset_index(name='Count')
    sorted_df = group_df.sort_values(by='Count', ascending=0).reset_index(drop=True)
    return sorted_df


def all_results_with_count(origin_df,filename):
    origin_df.drop('Time', axis=1, inplace=True)
    count_df = results_dataframe_counts(origin_df, filename)
    all_df = pd.merge(origin_df, count_df,
              left_on=['Origin', 'Destination'],
              right_on=['Origin', 'Destination'],
              how='inner')
    result = all_df.groupby(['Origin', 'Destination']).first().reset_index()  # remove the duplicate rows and only keep the first value
    result.sort_values(['Date', 'Count'], ascending=[True, False], inplace=True)
    return result


def results_dataframe_all(odarray):
    """Log info in dataframe, O, D, D P"""
    title = ('Origin', 'Destination', 'Distance', 'PrimaryServiceProviderCode', 'Date')
    df = pd.DataFrame(odarray, columns=list(title))
    return df


def output_df_all(filepath):
    """save all info together"""
    result = pd.read_csv(filepath)
    filedir,name = os.path.split(filepath)
    name, ext = os.path.splitext(name)
    csvfile = os.path.join(filedir, name+'_all' + '.csv')
    log_count = all_results_with_count(result,name)
    log_count.to_csv(csvfile, sep=',', encoding='utf-8', index=False)  # csv for OD pairs, distance and servic eprovider code


def output_df(filepath):
    """save new csv with count"""
    result = pd.read_csv(filepath)
    filedir,name = os.path.split(filepath)
    name, ext = os.path.splitext(name)
    log_count = results_dataframe_counts(result,name)
    csvfile = os.path.join(filedir, name+'_count' + '.csv')
    log_count.to_csv(csvfile, sep=',', encoding='utf-8', index=False)  # csv for OD pairs, distance and servic eprovider code


if __name__ == '__main__':
    #output_df(r'C:\work\project\logprocess\join_logs\20170307\20170307.csv')
    output_df_all(r'C:\work\project\logprocess\join_logs\20170306\20170306.csv')