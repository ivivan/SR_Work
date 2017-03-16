from RankingOD.analyse_logs import read_logs as rl
import pandas as pd
import numpy as np

def top_n_rows(dataframe, rownumber):
    """return top N rows, dataframe is ordered by Count """
    df = dataframe.head(rownumber)
    return df

def top_n_rows_conditions(dataframe):
    bins = [0,20,200,2000,20000]
    group_names = ['Rarely ', 'Few', 'Normal', 'Hot']
    # categories = pd.cut(dataframe['Count'], bins, labels=group_names)
    dataframe['categories'] = pd.cut(dataframe['Count'], bins, labels=group_names)
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
        print('%s %% covers %s od pairs' % (percentage_level * 100, od_num))
    else:
        for i in percentage_od:
            if total < percentage_level:
                total += i
            else:
                print(total)
                od_num = percentage_od.index(i)
                print(counted_od[percentage_od.index(i)])
                print('%s %% covers %s od pairs' % (percentage_level*100, percentage_od.index(i)))
                print('Last od pair has %s counts' % counted_od[percentage_od.index(i)])
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
            print('%s od pairs can cover %s %% counts' % (od_num, total*100/np.sum(counted_od)))
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

    print(percentile_list)
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

    print(percentile_list)
    return percentile_list









if __name__  == '__main__':
    log_dataframe = rl.read_csv(r'C:\Logs\DataBase\20160613_copy\ZIP.csv')

    print(log_dataframe.describe())


    # couted_df = rl.calculate_count(log_dataframe)
    # print(couted_df.to_string)
    #
    # choosen_dataframe = top_n_rows_conditions(couted_df)
    # print(choosen_dataframe.to_string)

    # choosen_dataframe = top_n_rows_lager(couted_df,50)
    # print(choosen_dataframe.to_string)
    #
    # choosen_dataframe_smaller = top_n_rows_smaller(couted_df,50)
    #
    # percentage_dataframe = top_n_rows_percentage(couted_df)
    # print(percentage_dataframe.to_string )

    # print(log_dataframe)

    count = log_dataframe['Count'].tolist()
    print(count)

    median = np.median(count)
    print(median)

    summary = np.sum(count)
    print(summary)

    percentage = [e/summary for e in count]
    # print(percentage[0])
    # print(count[0]/summary)


    n_percentage_part(1.0, count)

    n_odpairs_percentage(10000,count)



    po_df = percentage_od_xy(np.linspace(0.5, 1.0, num=11),count)




    po_df_perc = po_df.assign(od_needed=lambda x: x/len(count))



    print(po_df_perc)

    # od_percentage_xy(range(5000,len(count),1000),count)











