from RankingOD.analyse_logs import prepare_df as rl
from RankingOD.VirtualOD import LineGraphOD as linedrawer
from RankingOD.VirtualOD import line_graph as lg
from RankingOD.VirtualOD import barchart as bc
import pandas as pd
import numpy as np
import os
import scipy.optimize as optimize
import matplotlib.pyplot as plt
import collections


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


def weekly_head_df(percentage, filepath):
    files = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".csv"):
                files.append(entry.path)

    # filedir,name = os.path.split(filepath)
    # outputfiledir = os.path.abspath(os.path.join(filedir, os.path.pardir,'join_logs',name))
    week_data = {}
    for f in files:
        filedir, name = os.path.split(f)
        name, ext = os.path.splitext(name)
        full_df = rl.read_csv(f)
        count = full_df['Count'].tolist()
        percentage_point = n_percentage_part(percentage, count)
        popular_df = top_n_rows(full_df, percentage_point)
        week_data[name] = popular_df

    return week_data


def head_common_df(percentage,filepath):
    """one week logs analysis, showing common popular od pairs in N days.  Count columns in order by date"""
    week_log = weekly_head_df(percentage,filepath)

    key_list = []
    for k in week_log.keys():
        key_list.append(k)
    key_list.sort()  # order by date

    temp_df = week_log.get(key_list[0])
    for item in key_list[1:len(key_list)]:
        temp_df = pd.merge(temp_df, week_log.get(item), on=['Origin', 'Destination'], how='inner')

    head_list = list(temp_df)
    head_list[2:] = key_list
    temp_df.columns = head_list

    return temp_df


def save_common_df_as_csv(df,outputfolder):
    """save new csv with common od pairs within one week"""
    filedir,name = os.path.split(outputfolder)
    csvfile = os.path.join(filedir, 'common_odpairs' + '.csv')
    df.to_csv(csvfile, sep=',', encoding='utf-8',
                     index=False)  # csv for OD pairs, distance and servic eprovider code


def common_od_log(dic,df, filepath):
    print('Generate Report for common op pairs')
    filedir,name = os.path.split(filepath)
    outputfile = os.path.join(filedir, 'common_odpairs' + '.txt')

    with open(outputfile, 'w') as f:
        for k,v in dic.items():
            f.write('Day: %s \n' % k)
            f.write('\n')
            f.write('Total number of od paris are: %s \n' % len(v.index))
            f.write('\n')
            f.write('Total number of common od paris are: %s \n' % len(df.index))
            f.write('\n')
            perc = len(df.index)*100/len(v.index)
            f.write('%s %% of od pairs are the same \n' % perc )
            f.write('\n')
    f.close()


if __name__  == '__main__':

    filepath_folder = r'C:\work\project\logprocess\processed_result\weekly'

    # one week logs analysis
    temp_df = head_common_df(1.0, filepath_folder)
    # save_common_df_as_csv(temp_df, filepath_folder)

    # common od pairs percentage
    weekly_popular_od = weekly_head_df(1.0, filepath_folder)
    common_od_log(weekly_popular_od,temp_df,filepath_folder)

    # bar chart for the same od pairs
    tuple_data = bc.prepare_data(weekly_popular_od, temp_df)
    bc.common_od_histogram(tuple_data,'barchart')