from RankingOD.prepare_logs import read_logs as rlog
from RankingOD.prepare_logs import output_logs as olog
from RankingOD.VirtualOD import LineGraphOD as linedrawer

import os
import re
import timeit
import multiprocessing


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
    odpairsarray = rlog.process_log_seq(filepath)
    print(odpairsarray)
    result = olog.results_dataframe_counts(odpairsarray)
    resultforDB = olog.results_dataframe_all(odpairsarray)
    print(result.to_string())
    print(resultforDB.to_string())
    resultforDB.to_csv(csvfile, sep=',', encoding='utf-8')
    newresult = linedrawer.prepareData(result)
    linedrawer.drawLineGraph(newresult)
    print(newresult.to_string())
    print(newresult['Count'].sum())

# multiprocessing.freeze_support()
start = timeit.default_timer()
dailyProcess(r'C:\Logs\TRY')
stop = timeit.default_timer()
print('Spent %s seconds processing one day log.' % str(stop-start))









