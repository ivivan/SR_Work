from RankingOD.analyse_logs import prepare_df as rl
from RankingOD.VirtualOD import LineGraphOD as linedrawer
from RankingOD.VirtualOD import line_graph as lg
import pandas as pd
import numpy as np
import os
import scipy.optimize as optimize
import matplotlib.pyplot as plt


def top_n_rows(dataframe, rownumber):
    """return top N rows, dataframe is ordered by Count """
    df = dataframe.head(rownumber)
    return df


def top_n_rows_lager(dataframe,number):
    df = dataframe[dataframe.Count > number]
    return df


def top_n_rows_smaller(dataframe,number):
    df = dataframe[dataframe.Count < number]
    return df


def top_n_rows_percentage(dataframe):
    df = dataframe.assign(Perc=dataframe['Count']/dataframe['Count'].sum())
    return df


def count_to_percentage(count_od):
    summary = np.sum(count_od)
    percentage = [e / summary for e in count_od]
    return percentage


def n_percentage_part(percentage_level, counted_od):
    """Calculate to cover N percentage counts, how many od pairs we need"""
    total = 0.0
    od_num = 0
    percentage_od = count_to_percentage(counted_od)
    if percentage_level == 1.0:
        od_num = len(counted_od)
    else:
        for i in percentage_od:
            if total < percentage_level:
                total += i
            else:
                od_num = percentage_od.index(i)
                break
    return od_num


def n_odpairs_percentage(od_num, counted_od):
    """calculate if we have N od pairs, how many percentages we can cover"""
    start = 0
    total = 0
    for i in counted_od:
        if start < od_num:
            total += i
            start += 1
        else:
            break
    return total/np.sum(counted_od)


def percentage_od_xy(range,count):
    """generate dataframe, x percentage, y counts"""
    percentages = []
    for i in range:
        percentages.append(n_percentage_part(i, count))

    percentile_list = pd.DataFrame(
        {'percentage': range,
         'od_needed': percentages
         })
    return percentile_list


def od_percentage_xy(range, count):
    """generate dataframe, x counts, y percentage"""
    percentages = []
    for i in range:
        percentages.append(n_odpairs_percentage(i, count))

    percentile_list = pd.DataFrame(
        {'od_needed': range,
         'percentage': percentages
         })
    return percentile_list


def perc_perc_xy(po_df,count):
    po_df_perc = po_df.assign(od_needed=lambda x: x/len(count))
    return po_df_perc


if __name__  == '__main__':
    filepath = r'C:\work\project\logprocess\join_logs\20170308\20170308_count.csv'
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    log_dataframe = rl.read_csv(filepath)
