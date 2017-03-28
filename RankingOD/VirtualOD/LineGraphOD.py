import networkx as nx
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import plotly.offline as offline
import numpy as np

plotly.tools.set_credentials_file(username='ivivan', api_key='BsmuQgUrCGvEa7P6VWOs')


def prepareData(resultsindataframe):
    resultwithnewcolumne = resultsindataframe.assign(OD=resultsindataframe['Origin']+ '_' + resultsindataframe['Destination'])
    resultwithnewcolumne.drop('Origin', axis=1, inplace=True)
    resultwithnewcolumne.drop('Destination', axis=1, inplace=True)
    return resultwithnewcolumne


def drawLineGraph(prepareddata,filename):
    """OD Popularity"""
    data = [
        go.Scatter(
            x=prepareddata['OD'], # assign x as the dataframe column 'x'
            y=prepareddata['Count']
        )
    ]
    layout = go.Layout(
        title='OD Pairs Popularity',
        xaxis=dict(
            title='OD Pairs',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            ),
            dtick=10000
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
    py.plot(fig, filename=filename)


def line_per_od(dataframe,filename):
    """line graph for long tail analysis. X: percentage Y: od pairs"""
    data = [
        go.Scatter(
            x=dataframe['percentage'], # assign x as the dataframe column 'x'
            y=dataframe['od_needed']
        )
    ]
    layout = go.Layout(
        title='Required OD Pairs Under Different Query Coverage Rates',
        xaxis=dict(
            title='Query Coverage Rate (Percentage)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Number of OD Pairs Required',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename)


def line_od_per(dataframe,filename):
    """line graph for long tail analysis. X: od pairs Y: percentage"""
    data = [
        go.Scatter(
            x=dataframe['od_needed'], # assign x as the dataframe column 'x'
            y=dataframe['percentage'],
        )
    ]
    layout = go.Layout(
        title='Relationship between Query Coverage Rate and Number of OD Pairs',
        xaxis=dict(
            title='Number of OD Pairs Required',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Query Coverage Rate (Percentage)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename)


def line_odper_per(dataframe,filename):
    """line graph for long tail analysis. X: od percentage Y: percentage"""
    data = [
        go.Scatter(
            x=dataframe['od_needed'], # assign x as the dataframe column 'x'
            y=dataframe['percentage']
        )
    ]
    layout = go.Layout(
        title='Relationship between Query Coverage Rate and OD Pairs',
        xaxis=dict(
            title='OD Pairs (Percentage)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Query Coverage Rate (Percentage)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename)


def line_per_odper(dataframe,filename):
    """line graph for long tail analysis. X: percentage Y: od percentage"""
    data = [
        go.Scatter(
            x=dataframe['percentage'], # assign x as the dataframe column 'x'
            y=dataframe['od_needed']
        )
    ]
    layout = go.Layout(
        title='Relationship between Query Coverage Rate and OD Pairs',
        xaxis=dict(
            title='Query Coverage Rate (Percentage)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='OD Pairs (Percentage)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename)


def line_per_odper_fitting_fuction(dataframe, function, filename):
    """line graph for long tail analysis. X: percentage Y: od percentage"""

    # calculate new x's and y's
    x_new = np.linspace(0.5, 1, 50)
    y_new = function(x_new)

    data_origin = go.Scatter(
        x=dataframe['percentage'],  # assign x as the dataframe column 'x'
        y=dataframe['od_needed'],
        mode='markers',
        marker=go.Marker(color='rgb(255, 127, 14)'),
        name='Data'
    )

    data_fitting = go.Scatter(
        x=x_new,
        y=y_new,
        mode='lines',
        marker=go.Marker(color='rgb(31, 119, 180)'),
        name='Fit'
    )

    # annotation = go.Annotation(
    #     x=6,
    #     y=-4.5,
    #     text='$\textbf{Fit}: 5.634e-16X^3 - 1.849e-10X^2 + 1.635e-05X + 0.535$',
    #     showarrow=False
    # )

    data = [data_origin, data_fitting]

    layout = go.Layout(
        title='Coverage and OD Relationship with Polynomial Fit in Python',
        plot_bgcolor='rgb(229, 229, 229)',
        xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        # annotations=[annotation]
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename)
