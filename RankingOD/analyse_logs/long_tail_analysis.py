from RankingOD.analyse_logs import prepare_df as rl
from RankingOD.VirtualOD import LineGraphOD as linedrawer
from RankingOD.VirtualOD import line_graph as lg
import pandas as pd
import numpy as np
import os
import scipy.optimize as optimize


def top_n_rows(dataframe, rownumber):
    """return top N rows, dataframe is ordered by Count """
    df = dataframe.head(rownumber)
    return df


# def top_n_rows_conditions(dataframe):
#     bins = [20,1000,2000,3000,4000,5000,9000]
#     group_names = ['Rarely ', 'Few', 'Normal', 'Hot']
#     # categories = pd.cut(dataframe['Count'], bins, labels=group_names)
#     dataframe['categories'] = pd.cut(dataframe['Count'], bins, labels=group_names)
#     return dataframe


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
        #print('%s %% covers %s od pairs' % (percentage_level * 100, od_num))
    else:
        for i in percentage_od:
            if total < percentage_level:
                total += i
            else:
                od_num = percentage_od.index(i)
                #print('%s %% covers %s od pairs' % (percentage_level*100, percentage_od.index(i)))
                #print('Last od pair has %s counts' % counted_od[percentage_od.index(i)])
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
            #print('%s od pairs can cover %s %% counts' % (od_num, total*100/np.sum(counted_od)))
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


def curve_fitting_function(df,degree):
    numpyMatrix = df.as_matrix()
    y = numpyMatrix[:, 0]
    x = numpyMatrix[:, 1]
    print(x)
    print(y)

    # calculate polynomial
    z = np.polyfit(x, y, degree)
    f = np.poly1d(z)
    return f



if __name__  == '__main__':
    filepath = r'C:\work\project\logprocess\join_logs\20170306_count.csv'
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)


    log_dataframe = rl.read_csv(filepath)
    count = log_dataframe['Count'].tolist()

    median = np.median(count)  # output median number
    print(median)

    summary = np.sum(count)  # output total counts
    print(summary)

    print(log_dataframe.describe())  # output describeof the dataframe

    percentage = [e/summary for e in count]

    # po_df = percentage_od_xy(np.linspace(0.5, 1.0, num=11), count)
    # numpyMatrix = po_df.as_matrix()
    # x = numpyMatrix[:, 0]
    # y = numpyMatrix[:, 1]
    # z = np.polyfit(x, y, 3)
    # f = np.poly1d(z)
    # print(f)


    # top_df = top_n_rows(log_dataframe, 100000)

    # # draw line graph ,x: perc y: od
    # po_df = linedrawer.prepareData(log_dataframe)
    # linedrawer.drawLineGraph(po_df, "OD_pairs_count")


    # draw line graph ,x: perc y: od
    # po_df = percentage_od_xy(np.linspace(0.5, 1.0, num=11), count)
    # linedrawer.line_per_od(po_df,"OD_pairs_needed")
    # #
    # # draw line graph, x: od y: perc
    # po_df = od_percentage_xy(range(5000,len(count),1000), count)
    # linedrawer.line_od_per(po_df,"OD_pairs_coverage")
    #
    # # draw line graph, x: od perc y: perc
    # po_df = od_percentage_xy(range(5000, len(count), 1000), count)
    # po_df_perc = perc_perc_xy(po_df,count)
    # linedrawer.line_odper_per(po_df_perc,"OD_Coverage_Relationship")
    #
    # # draw line graph, x: perc y: od perc
    # po_df = percentage_od_xy(np.linspace(0.5, 1.0, num=11), count)
    # po_df_perc = perc_perc_xy(po_df,count)
    # linedrawer.line_per_odper(po_df_perc,"Coverage_OD_Relationship")

    # draw line graph with fitting function, x: perc y: od perc
    po_df = percentage_od_xy(np.linspace(0.5, 1.0, num=11), count)
    po_df_perc = perc_perc_xy(po_df,count)
    f = curve_fitting_function(po_df_perc,4)
    print(f)
    linedrawer.line_per_odper_fitting_fuction(po_df_perc, f, "Coverage_OD_Relationship_with_fitting")


    # choose top 25k od pairs for analysing
    # top_df = top_n_rows(log_dataframe,25000)















