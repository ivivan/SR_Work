import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from RankingOD.analyse_logs import prepare_df as predf
import os


def prepareData(resultsindataframe):
    resultwithnewcolumne = resultsindataframe.assign(OD=resultsindataframe['Origin']+ '_' + resultsindataframe['Destination'])
    resultwithnewcolumne.drop('Origin', axis=1, inplace=True)
    resultwithnewcolumne.drop('Destination', axis=1, inplace=True)
    return resultwithnewcolumne


def liner_od_count(df):
    fig = df[['OD', 'Count']].plot(kind='line', title="OD popularity")
    plt.xticks(range(len(df.OD)), df.OD)
    fig.set_xlabel("OD pairs", fontsize=12)
    fig.set_ylabel("Counts", fontsize=12)
    plt.show()

