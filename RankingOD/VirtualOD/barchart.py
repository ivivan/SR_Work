import networkx as nx
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import plotly.offline as offline
import numpy as np
import collections
import pandas as pd

plotly.tools.set_credentials_file(username='ivivan', api_key='BsmuQgUrCGvEa7P6VWOs')

def prepare_data(dict, dataframe):
    """k:date,v: same od counts, common:different od counts, total: total od perday """
    ordered = collections.OrderedDict(sorted(dict.items()))
    dict_k = []
    dict_v = []
    dict_common = []
    dict_total = []
    for k, v in ordered.items():
        dict_k.append(k[:8])
        dict_v.append(len(dataframe.index))
        dict_common.append(len(v.index)-len(dataframe.index))
        dict_total.append(len(v.index))
    return (dict_k,dict_v,dict_common,dict_total)


def prepare_data_two(arr):
    """2D array to dataframe, total actually total minus same"""
    df = pd.DataFrame(arr, columns=['Total', 'Same', 'Coverage'])
    df['Total'] = df['Total'] - df['Same']
    return df


def common_od_histogram(tuple_od,filename):

    trace_0 = go.Bar(
        x = tuple_od[0],
        y = tuple_od[1],
        name='Same OD Pairs'
    )
    trace_1 = go.Bar(
        x = tuple_od[0],
        y = tuple_od[2],
        name='Different OD Pairs'
    )
    data = [trace_0, trace_1]
    layout = go.Layout(
        barmode='stack',
        title='Same OD Pairs Among Different Days',
        xaxis=dict(
            title='Date',
            type='category',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            ),
        ),
        yaxis=dict(
            type='linear',
            title='Number of OD Pairs',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data,layout=layout)
    py.plot(fig, filename=filename)


def same_od_changing(df,filename):
    """Same OD Pairs Under Different Query Coverage Rate, mixed with line graph and bar chart, two y axis"""
    trace_0 = go.Bar(
        x = df['Coverage'],
        y = df['Same'],
        name='Same OD Pairs'
    )
    trace_1 = go.Bar(
        x = df['Coverage'],
        y = df['Total'],
        name='Different OD Pairs'
    )

    trace_2 = go.Scatter(
        x = df['Coverage'],
        y = df['Same'] / (df['Total'] + df['Same']),
        name='Percentage of Same OD Pairs',
        yaxis='y2'
    )

    data = [trace_0, trace_1, trace_2]
    layout = go.Layout(
        barmode='stack',
        title='Same OD Pairs Under Different Query Coverage Rate',
        xaxis=dict(
            title='Query Coverage Rate (Percentage)',
            type='category',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            ),
        ),
        yaxis=dict(
            type='linear',
            title='Number of OD Pairs',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis2=dict(
            title='Percentage',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        )
    )

    fig = go.Figure(data=data,layout=layout)
    py.plot(fig, filename=filename)

if __name__  == '__main__':
    prepare_data(dict)