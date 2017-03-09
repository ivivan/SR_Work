import os
import re
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

def xmlParser(filepath):
    e = ET.parse(filepath)
    root = e.getroot()
    m = re.match('\{.*\}', root.tag)
    namespace = m.group(0) if m else ''

    od = []
    for origin in e.findall(namespace+'OriginList'):
        location = origin.find(namespace+'Location')
        od.append(location.text)

    for destination in e.findall(namespace+'DestinationList'):
        location = destination.find(namespace+'Location')
        od.append(location.text)
    return od

def calculateODPairs(filepath):
    odpairs = []
    files = []

    for entry in os.scandir(filepath):
        if entry.is_file():
            files.append(entry.path)

    for f in files:
        oneod = xmlParser(f)
        odpairs.append(oneod)

    return odpairs

def resultsTableView(odarray):
    aTuple = ('Origin', 'Destination')
    df = pd.DataFrame(odarray, columns=list(aTuple))
    group_df = df.groupby(['Origin', 'Destination']).size().reset_index(name='Count')
    sorted_df = group_df.sort_values(by='Count', ascending=0).reset_index(drop=True)
    return sorted_df

def stationlist(odpairlist):
    odlists_temp = np.array(odpairlist).ravel()
    odlists_unique = np.unique(odlists_temp)
    return odlists_unique



if __name__ == '__main__':
    odpairsarray = calculateODPairs(r'C:\Logs\O1\LIV2-IPTAPP102-MessageRelayLog_[2016-06-13]_17')
    result = resultsTableView(odpairsarray)
    odlists = stationlist(odpairsarray)

    print(odlists)
    print(len(odlists))
    print(result.to_string())


