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
import re
import time
from datetime import datetime


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
    """find subset of od based on percentage coverage"""
    files = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".csv"):
                files.append(entry.path)
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


def weekly_head_df_above(count_level, filepath):
    """find subset of od based on count above some value"""
    files = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".csv"):
                files.append(entry.path)
    week_data = {}
    for f in files:
        filedir, name = os.path.split(f)
        name, ext = os.path.splitext(name)
        full_df = rl.read_csv(f)
        count = full_df['Count'].tolist()
        popular_df = top_n_rows_lager(full_df, count_level)
        week_data[name] = popular_df

    return week_data


def head_common_df(percentage,filepath):
    """one week logs analysis, showing common popular od pairs in N days.  Count columns in order by date. Use percentage to choose data"""
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


def head_common_df_above(count_level,filepath):
    """one week logs analysis, showing common popular od pairs in N days.  Count columns in order by date. Use value to choose data"""
    week_log = weekly_head_df_above(count_level,filepath)

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
    csvfile = os.path.join(filedir, 'same_odpairs' + '.csv')
    df.to_csv(csvfile, sep=',', encoding='utf-8',
                     index=False)  # csv for OD pairs, distance and servic eprovider code


def same_od_changing(range, filepath):
    """return same od pairs under different percentage coverage. [[average_total_number, same_od_number, percentage],...]"""
    results = []
    for p in range:
        total_od = 0
        result = []
        each_day_info = weekly_head_df(p, filepath)
        same_df = head_common_df(p, filepath)
        for k,v in each_day_info.items():
            total_od += len(v.index)
        average_od = total_od//len(each_day_info)
        result.append(average_od)
        result.append(len(same_df))
        result.append(str(p))
        results.append(result)

    return results



def common_od_log(dic,df, filepath):
    print('Generate Report for same op pairs')
    filedir,name = os.path.split(filepath)
    outputfile = os.path.join(filedir, 'same_odpairs' + '.txt')

    with open(outputfile, 'w') as f:
        for k,v in dic.items():
            f.write('Day: %s \n' % k)
            f.write('\n')
            f.write('Total number of od paris are: %s \n' % len(v.index))
            f.write('\n')
            f.write('Total number of same od paris are: %s \n' % len(df.index))
            f.write('\n')
            perc = len(df.index)*100/len(v.index)
            f.write('%s %% of od pairs are the same \n' % perc )
            f.write('\n')
    f.close()


def journey_start_date(df):
    df['Time'] = df['Time'].str[0:10]
    return df


def split_it(timestamp):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
    return re.findall(date_pattern, timestamp)


def compare_date(date_one, date_two):
    date1 = datetime.strptime(date_one, '%Y-%m-%d')
    date2 = datetime.strptime(date_two, '%Y-%m-%d')
    return (date1 - date2)


if __name__  == '__main__':
    filepath_folder = r'C:\work\project\logprocess\join_logs\20170312\20170312.csv'
    result = pd.read_csv(filepath_folder)
    new_date_df = journey_start_date(result)

    date1 = datetime.strptime('2017-03-01', '%Y-%m-%d')
    date2 = datetime.strptime('2017-03-03', '%Y-%m-%d')

    print(date1 > date2)


    #print(new_date_df)









