import networkx as nx
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import pandas as pd
import numpy as np

plotly.tools.set_credentials_file(username='ivivan', api_key='BsmuQgUrCGvEa7P6VWOs')


def prepareData(resultsindataframe):
    resultwithnewcolumne = resultsindataframe.assign(OD=resultsindataframe['Origin']+ '_' + resultsindataframe['Destination'])
    resultwithnewcolumne.drop('Origin', axis=1, inplace=True)
    resultwithnewcolumne.drop('Destination', axis=1, inplace=True)
    return resultwithnewcolumne


def drawLineGraph(prepareddata):
    data = [
        go.Scatter(
            x=prepareddata['OD'], # assign x as the dataframe column 'x'
            y=prepareddata['Count'],
            name='2016-06-13'
        )
    ]
    layout = go.Layout(
        title='OD popularity',
        xaxis=dict(
            title='OD',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Count',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    url = py.plot(fig, filename='basic-line-plot')




