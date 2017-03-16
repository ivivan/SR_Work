import networkx as nx
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

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

def line_per_od(dataframe,filename):
    """line graph for long tail analysis. X: percentage Y: od pairs"""
    data = [
        go.Scatter(
            x=dataframe['percentage'], # assign x as the dataframe column 'x'
            y=dataframe['od_needed'],
            name='2016-06-13'
        )
    ]
    layout = go.Layout(
        title='OD pairs required by coverage',
        xaxis=dict(
            title='Percentage',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Number of OD pairs',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    url = py.plot(fig, filename=filename)


def line_od_per(dataframe,filename):
    """line graph for long tail analysis. X: od pairs Y: percentage"""
    data = [
        go.Scatter(
            x=dataframe['od_needed'], # assign x as the dataframe column 'x'
            y=dataframe['percentage'],
            name='2016-06-13'
        )
    ]
    layout = go.Layout(
        title='OD pairs coverage',
        xaxis=dict(
            title='Number of OD pairs',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Percentage',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    url = py.plot(fig, filename=filename)


def line_odper_per(dataframe,filename):
    """line graph for long tail analysis. X: od percentage Y: percentage"""
    data = [
        go.Scatter(
            x=dataframe['od_needed'], # assign x as the dataframe column 'x'
            y=dataframe['percentage'],
            name='2016-06-13'
        )
    ]
    layout = go.Layout(
        title='OD and Coverage Relationship',
        xaxis=dict(
            title='Percentage of OD pairs',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Percentage of Coverage',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    url = py.plot(fig, filename=filename)


def line_per_odper(dataframe,filename):
    """line graph for long tail analysis. X: percentage Y: od percentage"""
    data = [
        go.Scatter(
            x=dataframe['percentage'], # assign x as the dataframe column 'x'
            y=dataframe['od_needed'],
            name='2016-06-13'
        )
    ]
    layout = go.Layout(
        title='Coverage and OD Relationship',
        xaxis=dict(
            title='Percentage of Coverage',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Percentage of OD pairs',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    url = py.plot(fig, filename=filename)
