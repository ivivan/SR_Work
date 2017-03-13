from RankingOD.ParseLogs import parseXMLTXT as plogxml
from RankingOD.ParseLogs import parseXMLList as plog
from RankingOD.VirtualOD import LineGraphOD as linedrawer
from RankingOD.VirtualOD import HeatMap as heatmapdrawer
import plotly.plotly as py
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import os
import re
import timeit




def dailyProcess(filepath):

    outputname = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".zip"):
                name, ext = os.path.splitext(entry.name)
                if re.search(r'\d{8}$',name):
                    outputname.append(re.search(r'\d{8}$',name).group(0))

    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    outputfiledir = os.path.abspath(os.path.join(filedir, 'DataBase', outputname[0]))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)

    csvfile = os.path.join(outputfiledir, name + '.csv')
    odpairsarray = plogxml.batchProcessingAll(filepath)
    print(odpairsarray)
    result = plog.resultsTableViewForCount(odpairsarray)
    resultforDB = plog.resultsTableViewAllInfo(odpairsarray)
    print(result.to_string())
    print(resultforDB.to_string())
    resultforDB.to_csv(csvfile, sep=',', encoding='utf-8')
    newresult = linedrawer.prepareData(result)
    linedrawer.drawLineGraph(newresult)
    print(newresult.to_string())
    print(newresult['Count'].sum())


start = timeit.default_timer()
dailyProcess(r'C:\Logs\TRY')
stop = timeit.default_timer()
print('Spent %s seconds processing one day log.' % str(stop-start))









