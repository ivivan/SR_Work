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


def journey_start_date(df,filename):
    df['Time'] = df['Time'].str[0:10]
    df['Time'] = pd.to_datetime(df.Time, format='%Y-%m-%d')
    filedir,name = os.path.split(filename)
    name, ext = os.path.splitext(name)
    df = df[df.Time >= datetime.strptime(name, '%Y%m%d')]
    return df


def split_it(timestamp):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
    return re.findall(date_pattern, timestamp)


def compare_date(date_one, date_two):
    date1 = datetime.strptime(date_one, '%Y-%m-%d')
    date2 = datetime.strptime(date_two, '%Y-%m-%d')
    return (date1 > date2)


def group_journeys(filepath):
    filedir,name = os.path.split(filepath)
    name, ext = os.path.splitext(name)
    today = datetime.strptime(name, '%Y%m%d').date()


def starttime_count(df):
    """Log info in dataframe, O, D, Count"""
    group_df = df.groupby(['Time']).size().reset_index(name='Count')
    sorted_df = group_df.sort_values(by='Time', ascending=1).reset_index(drop=True)
    return sorted_df


def group_starttime(df,range):
    """Log info in dataframe, O, D, Count"""
    df.index = pd.to_datetime(df.Time, format='%Y-%m-%d')
    df.drop('Time', axis=1, inplace=True)
    result = df.resample(range).sum()
    return result



if __name__  == '__main__':
    filepath_folder = r'C:\work\project\logprocess\join_logs\20170312\20170312.csv'
    result = pd.read_csv(filepath_folder)
    new_date_df = journey_start_date(result,filepath_folder)

    time_count_df = starttime_count(new_date_df)
    print(time_count_df[time_count_df.Count > 1000])

    bc.journey_start_bar(time_count_df[time_count_df.Count > 1000],'JourneyStartTime')



    # grouped_df = group_starttime(time_count_df,'3D')
    # print(grouped_df)
    #
    #
    # head_df = time_count_df[time_count_df.Count > 1000]
    # print(head_df)
















