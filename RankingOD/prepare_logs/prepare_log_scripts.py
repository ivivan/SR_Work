import os
import multiprocessing
import timeit
from lxml import etree
import re
import pandas as pd


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
    outputfiledir = os.path.abspath(os.path.join(filedir, 'OUTPUT', name))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)
    csvfile = os.path.join(outputfiledir, name + '.csv')

    result = results_dataframe(processed_results_part)
    result.to_csv(csvfile, sep=',', encoding='utf-8')  # csv for OD pairs and counting
    print('done')


def process_each_log_in_zip(f):
    eachxml = []
    odpairs = []
    getxmlhead = False

    with open(f,encoding='utf-8') as log:
        for line in log:
            if not getxmlhead:
                if line[0] == '<' and '<JourneyPlanningRes' in line:
                    eachxml.append(line)
                    getxmlhead = True
            elif line[0] == '<' and '</J' in line:
                eachxml.append(line)
                getxmlhead = False
                eachod = test_lxml(''.join(eachxml))
                odpairs.extend(eachod)
                eachxml = []
            else:
                eachxml.append(line)
    return odpairs


def test_lxml(filepath):
    """use lxml to parse xml body"""
    tree = etree.ElementTree(etree.fromstring(filepath))
    root = tree.getroot()
    m = re.match('\{.*\}', root.tag)
    namespace = m.group(0) if m else ''

    originstations = []
    destinationstatoins = []
    distances = []
    journeystarttime = []
    servicecodes = set()
    od = []
    finddistance = False
    findtime = False

    for element in root.iter(namespace+'Distance', namespace+'Location', namespace+'PrimaryServiceProviderCode', namespace+'Start'):
        if not finddistance and element.tag == namespace+'Distance':
            distances.append(element.text)
            finddistance = True
        elif element.tag == namespace+'Location':
            if element.getparent().tag == namespace+'OriginList':
                originstations.append(element.text)
            else:
                destinationstatoins.append(element.text)
        elif not findtime and element.tag == namespace+'Start' and element.getparent().tag == namespace+'Timeband':
            journeystarttime.append(element.text)
            findtime = True
        elif element.tag == namespace+'PrimaryServiceProviderCode':
            servicecodes.add(element.text)

    for x, y in zip(originstations, destinationstatoins):
        od.append([x if originstations is not None else 'NONE', y if destinationstatoins is not None else 'NONE', journeystarttime[0] if journeystarttime else '2000-00-00T00:00:00.000+00:00',
                   distances[0] if distances else '0', list(servicecodes) if servicecodes is not None else []])
    return od


def results_dataframe(odarray):
    """Table View Results, O, D, C"""
    title = ('Origin', 'Destination', 'Time', 'Distance', 'PrimaryServiceProviderCode')
    df = pd.DataFrame(odarray, columns=list(title))
    return df


if __name__ == '__main__':
    multiprocessing.freeze_support()
    start = timeit.default_timer()
    print('Start processing logs at %s,' % str(start))
    multiprocess_log(r'C:\Logs\F1.20000000')
    stop = timeit.default_timer()
    print('Spent %s seconds processing daily log.' % str(stop - start))