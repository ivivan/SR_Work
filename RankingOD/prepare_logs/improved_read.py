import os
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
            if entry.name.endswith(".txt"):
                files.append(entry.path)

    for f in files:
        results.append(pool.apply_async(process_each_log_in_zip, [f]))

    pool.close()
    pool.join()

    result_together = [result.get() for result in results]
    processed_results_part = [num for elem in result_together for num in elem]
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)

    outputfiledir = os.path.abspath(os.path.join(filedir, 'OUTPUT', name))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)
    csvfile = os.path.join(outputfiledir, name + '.csv')

    result = olog.results_dataframe_all(processed_results_part)
    result.to_csv(csvfile, sep=',', encoding='utf-8')  # csv for OD pairs and counting
    print('done')


def process_each_log_in_zip(f):
    eachxml = []
    odpairs = []
    getxmlhead = False

    with open(f) as log:
        print(f)
        for line in log:
            if line:
                if not getxmlhead:
                    if line[0] == '<' and '<JourneyPlanningRes' in line:
                        eachxml.append(line)
                        getxmlhead = True
                elif line[0] == '<' and '</JourneyPlanningRes' in line:
                    eachxml.append(line)
                    getxmlhead = False
                    eachod = plog.test_lxml(''.join(eachxml))
                    odpairs.extend(eachod)
                    eachxml = []
                else:
                    eachxml.append(line)
    return odpairs


if __name__ == '__main__':
    multiprocessing.freeze_support()
    start = timeit.default_timer()
    multiprocess_log(r'C:\Logs\ZIP')
    stop = timeit.default_timer()
    print('Spent %s seconds processing daily log.' % str(stop - start))
