import os
import re
import zipfile
from RankingOD.prepare_logs import parse_logs as plog
from RankingOD.prepare_logs import output_logs as olog
import multiprocessing
import timeit


def multiprocess_log(filepath):
    """each process processes log files witnin one zip file"""
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()

    files = []
    results = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".zip"):
                files.append(entry.path)

    for f in files:
        for log in list_log_in_zip(f):
            results.append(pool.apply_async(process_each_log_in_zip, [log, f]))

    pool.close()
    pool.join()

    result_together = [result.get() for result in results]
    processed_results = [num for elem in result_together for num in elem]

    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    nametwo = name+'count'
    outputfiledir = os.path.abspath(os.path.join(filedir, 'DataBase', name))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)
    csvfile = os.path.join(outputfiledir, name + '.csv')
    csvfiletwo = os.path.join(outputfiledir, nametwo + '.csv')
    result = olog.results_dataframe_counts(processed_results)
    resultforDB = olog.results_dataframe_all(processed_results)
    resultforDB.to_csv(csvfile, sep=',', encoding='utf-8')  # csv for all information
    result.to_csv(csvfiletwo, sep=',', encoding='utf-8')  # csv for OD pairs and counting
    print('done')


def list_log_in_zip(filepath):
    files = []
    with zipfile.ZipFile(filepath) as z:
        for logfile in z.namelist():
            if not os.path.isdir(logfile):
                file_name, file_extension = os.path.splitext(logfile)
                if file_extension == ".txt":
                    files.append(logfile)
    return files

def process_each_log_in_zip(logfile, f):
    eachxml = ''
    ip_value = ''
    ts_value = ''
    odpairs = []
    getxmlhead = False
    findip = False
    findts = False

    response_start_pattern = re.compile(b'^<JourneyPlanningResponse')
    response_stop_pattern = re.compile(b'^</JourneyPlanningResponse>')
    ip_pattern = re.compile(b'^IP')
    timestamp_pattern = re.compile(b'^TimeStamp')
    ipaddr_pattern = re.compile(
        r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))')
    tsvalue_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:\d{4}')

    with zipfile.ZipFile(f).open(logfile) as log:
        print(logfile)
        for line in log:
            if line:
                if not getxmlhead:
                    if not findip and re.match(ip_pattern, line) is not None:
                        ip_value = line.decode('utf-8')
                        findip = True
                    if not findts and re.match(timestamp_pattern, line) is not None:
                        ts_value = line.decode('utf-8')
                        findts = True
                    if re.match(response_start_pattern, line) is not None:
                        eachxml += line.decode('utf-8')
                        getxmlhead = True
                elif re.match(response_stop_pattern, line) is not None:
                    eachxml += line.decode('utf-8')
                    getxmlhead = False
                    eachod = plog.test_lxml(eachxml)
                    [e.insert(3, re.search(ipaddr_pattern, ip_value).group(0) if re.search(ipaddr_pattern,
                                                                                           ip_value) else '0.0.0.0')
                     for e in eachod]
                    [e.insert(4,
                              re.search(tsvalue_pattern, ts_value).group(0) if re.search(
                                  tsvalue_pattern, ts_value) else '29990101')
                     for e in eachod]
                    odpairs.extend(eachod)
                    eachxml = ''
                else:
                    eachxml += line.decode('utf-8')

    zipfile.ZipFile(f).close()
    return odpairs


if __name__ == '__main__':
    multiprocessing.freeze_support()
    start = timeit.default_timer()
    multiprocess_log(r'C:\Logs\ZIP')
    stop = timeit.default_timer()
    print('Spent %s seconds processing daily log.' % str(stop - start))
