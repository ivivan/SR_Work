from RankingOD.analyse_logs import read_logs as rl
import pandas as pd
import numpy as np

def top_n_rows(dataframe, rownumber):
    """return top N rows, dataframe is ordered by Count """
    df = dataframe.head(rownumber)
    return df

def top_n_rows_conditions(dataframe,number):
    dataframe['group'] = pd.qcut(dataframe.Count, number)
    return dataframe

def top_n_rows_lager(dataframe,number):
    df = dataframe[dataframe.Count > number]
    return df

def top_n_rows_smaller(dataframe,number):
    df = dataframe[dataframe.Count < number]
    return df

def top_n_rows_percentage(dataframe):
    df = dataframe.assign(Perc=dataframe['Count']/dataframe['Count'].sum())
    return df





if __name__  == '__main__':
    log_dataframe = rl.read_csv(r'C:\Logs\DataBase\20170310\TRY.csv')


    couted_df = rl.calculate_count(log_dataframe)
    print(couted_df.to_string)

    choosen_dataframe = top_n_rows_conditions(couted_df, 20)
    print(choosen_dataframe.to_string)

    # choosen_dataframe = top_n_rows_lager(couted_df,50)
    # print(choosen_dataframe.to_string)
    #
    # choosen_dataframe_smaller = top_n_rows_smaller(couted_df,50)
    #
    # percentage_dataframe = top_n_rows_percentage(couted_df)
    # print(percentage_dataframe.to_string )
