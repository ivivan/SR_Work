import os
import re
import zipfile
from RankingOD.prepare_logs import parse_logs as plog
from RankingOD.prepare_logs import output_logs as olog
import multiprocessing
import timeit
import numpy as np

def process_log_seq(filepath):
    odpairs = []
    files = []
    part = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".zip"):
                files.append(entry.path)

    for f in files:
        print('Start log %s:' % f)
        part = process_each_log(f)
        odpairs += part
        print('Finish log %s' % f)

    print('done')
    return odpairs


def multiprocess_log(filepath):
    result_together = []
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()
    files = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".zip"):
                files.append(entry.path)

    for f in files:
        print('Start log %s:' % f)
        result = pool.apply_async(process_each_log,[f])
        # result_together.append(result.get())
        print('Finish log %s' % f)

    pool.close()
    pool.join()

    # processed_results = [num for elem in result_together for num in elem]
    # olog.output_group(processed_results,files[0])

def process_each_log(filepath):
    eachxml = ''
    ip_value = ''
    ts_value = ''
    odpairs = []
    withinxml = False
    getxmlhead = False

    response_start_pattern = re.compile(b'^<JourneyPlanningResponse')
    response_stop_pattern = re.compile(b'^</JourneyPlanningResponse>')
    ip_pattern = re.compile(b'^IP')
    timestamp_pattern = re.compile(b'^TimeStamp')
    ipaddr_pattern = re.compile(
        r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))')
    tsvalue_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:\d{4}')

    with zipfile.ZipFile(filepath) as z:
        for logfile in z.namelist():
            if not os.path.isdir(logfile):
                file_name, file_extension = os.path.splitext(logfile)
                if file_extension == ".txt":
                    with z.open(logfile) as f:
                        for line in f:
                            if line:
                                if re.match(ip_pattern, line) is not None:
                                    ip_value = line.decode('utf-8')
                                if re.match(timestamp_pattern, line) is not None:
                                    ts_value = line.decode('utf-8')
                                if re.match(response_start_pattern, line) is not None:
                                    eachxml += line.decode('utf-8')
                                    withinxml = True
                                    getxmlhead = True
                                elif re.match(response_stop_pattern, line) is not None:
                                    if getxmlhead:
                                        eachxml += line.decode('utf-8')
                                        withinxml = False
                                        getxmlhead = False
                                        print(file_name)
                                        eachod = plog.parse_response_xml(eachxml)
                                        [e.insert(3, re.search(ipaddr_pattern, ip_value).group(0) if re.search(ipaddr_pattern, ip_value) else '0.0.0.0') for e in eachod]
                                        [e.insert(4,
                                                  re.search(tsvalue_pattern, ts_value).group(0) if re.search(
                                                      tsvalue_pattern, ts_value) else '29990101')
                                         for e in eachod]
                                        # eachod.insert(3,ip_value)
                                        # eachod.insert(4,ts_value)

                                        odpairs.extend(eachod)
                                        eachxml = ''
                                elif withinxml:
                                    eachxml += line.decode('utf-8')
    z.close()


    # filedir,name = os.path.split(filepath)
    # name,ext = os.path.splitext(name)
    # outputfiledir = os.path.abspath(os.path.join(filedir, 'DataBase', name))
    # if not os.path.exists(outputfiledir):
    #     os.makedirs(outputfiledir)
    # csvfile = os.path.join(outputfiledir, name + '.csv')
    # result = olog.results_dataframe_counts(odpairs)
    # resultforDB = olog.results_dataframe_all(odpairs)
    # resultforDB.to_csv(csvfile, sep=',', encoding='utf-8')


    # return odpairs






if __name__ == '__main__':
    # multiprocessing.freeze_support()
    # start = timeit.default_timer()
    # multiprocess_log(r'C:\Logs\ZIP')
    # stop = timeit.default_timer()
    # print('Spent %s seconds processing one day log.' % str(stop - start))
    filepath = r'C:\Logs\ZIP'
    files = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".txt"):
                files.append(entry.path)
    print(files)














