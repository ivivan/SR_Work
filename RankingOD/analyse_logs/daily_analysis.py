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


def curve_fitting_function(df,degree):
    numpymatrix = df.as_matrix()
    y = numpymatrix[:, 0]
    x = numpymatrix[:, 1]
    print(x)
    print(y)

    # calculate polynomial
    z = np.polyfit(x, y, degree)
    f = np.poly1d(z)
    return f


def custom_fitting_function(df):
    numpymatrix = df.as_matrix()
    y = numpymatrix[:, 0]
    x = numpymatrix[:, 1]

    def func(x, a, b,c):
        return a * np.exp(b * x)-c

    popt, pcov = optimize.curve_fit(func, x, y)
    yvals = func(x, *popt)
    print(popt)
    plot1 = plt.plot(x, y, '*', label='original values')
    plot2 = plt.plot(x, yvals, 'r', label='curve_fit values')
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.legend(loc=4)  # location of legend
    plt.title('curve_fit')
    plt.show()
    plt.savefig('p2.png')


def statistic_daily_log(df,filepath):
    count = df['Count'].tolist()
    median = np.median(count)  # output median number
    summary = np.sum(count)  # output total counts

    # output statistical results
    print('Generate Report')
    filedir,name = os.path.split(filepath)
    outputfile = os.path.join(filedir, name + '.txt')

    statistical_report = open(outputfile, 'w', encoding='utf-8')
    statistical_report.write('Statistic Information: \n')
    statistical_report.write('Median value is: %s \n' % median)
    statistical_report.write('Total number of queries are: %s \n' % summary)
    statistical_report.write('More Details \n')
    statistical_report.write(df.describe().to_string())
    statistical_report.close()


def draw_all_chars(df):
    count = df['Count'].tolist()

    # draw line graph ,x: perc y: od
    po_df = linedrawer.prepareData(df)
    linedrawer.drawLineGraph(po_df, "OD_Pairs_Popularity")

    #draw line graph ,x: perc y: od
    po_df = percentage_od_xy(np.linspace(0.5, 1.0, num=11), count)
    linedrawer.line_per_od(po_df,"OD_pairs_needed")

    # draw line graph, x: od y: perc
    po_df = od_percentage_xy(range(5000,len(count),1000), count)
    linedrawer.line_od_per(po_df,"OD_pairs_coverage")

    # draw line graph, x: od perc y: perc
    po_df = od_percentage_xy(range(5000, len(count), 1000), count)
    po_df_perc = perc_perc_xy(po_df,count)
    linedrawer.line_odper_per(po_df_perc,"OD_Coverage_Relationship")

    # draw line graph, x: perc y: od perc
    po_df = percentage_od_xy(np.linspace(0.5, 1.0, num=11), count)
    po_df_perc = perc_perc_xy(po_df,count)
    linedrawer.line_per_odper(po_df_perc,"Coverage_OD_Relationship")


if __name__  == '__main__':
    filepath = r'C:\work\project\logprocess\join_logs\20170312\20170312_count.csv'
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    log_dataframe = rl.read_csv(filepath)

    # output statistical info:
    statistic_daily_log(log_dataframe,filepath)

    # draw all chars
    draw_all_chars(log_dataframe)