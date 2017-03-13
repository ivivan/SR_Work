import os
import re
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from RankingOD.ParseLogs import parseXMLList as plog
import zipfile


def xmlParserString(xmlstring):
    e = ET.ElementTree(ET.fromstring(xmlstring))
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

def xmlParserResponse(xmlstring):
    e = ET.ElementTree(ET.fromstring(xmlstring))
    root = e.getroot()
    m = re.match('\{.*\}', root.tag)
    namespace = m.group(0) if m else ''
    od = []
    providercode = []


    originlist = e.find('.//'+namespace+'OriginList')
    destinationlist = e.find('.//'+namespace+'DestinationList')
    distance = e.find('.//'+namespace+'Distance')
    codelist = e.findall('.//'+namespace+'PrimaryServiceProviderCode')
    if codelist is not None:
        for e in codelist:
            providercode.append(e.text)

    for x,y in zip(originlist,destinationlist):
        od.append([x.text if originlist else 'NONE',y.text if destinationlist else 'NONE',distance.text if distance is not None else '0' ,list(set(providercode)) if codelist is not None else []])

    return od

def batchProcessing(filepath):
    odpairs = []
    files = []
    part = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".zip"):
                files.append(entry.path)

    for f in files:
        print('Start log %s' % f)
        part = parseXMLfroTXTZIP(f)
        odpairs += part
        print('Finish log %s' % f)

    print('done')
    return odpairs

def batchProcessingAll(filepath):
    odpairs = []
    files = []
    part = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".zip"):
                files.append(entry.path)

    for f in files:
        print('Start log %s:' % f)
        part = parseXMLZIPALLINFO(f)
        odpairs += part
        print('Finish log %s' % f)

    print('done')
    return odpairs

def parseXMLfroTXT(filepath):
    eachxml = ''
    ipvalue = ''
    timestamp = ''
    odpairs = []
    withinxml = False
    getxmlhead = False
    num = 0

    xmlstartpattern = re.compile(r'^<JourneyPlanningRequest')
    xmlstoppattern = re.compile(r'.*</JourneyPlanningRequest>')
    ipPattern = re.compile(r'^IP')

    with open(filepath) as f:
        for line in f:
            if line:
                if re.match(ipPattern, line) is not None:
                    ipvalue = line
                if re.match(xmlstartpattern, line) is not None:
                    eachxml += line
                    withinxml = True
                    getxmlhead = True
                elif re.match(xmlstoppattern, line) is not None:
                    if getxmlhead:
                        eachxml += line
                        withinxml = False
                        getxmlhead = False
                        odpairs.append(xmlParserString(eachxml))
                        num += 1
                        print(num)
                        eachxml=''
                elif withinxml:
                    eachxml += line

    return odpairs


def parseXMLfroTXTZIP(filepath):
    eachxml = ''
    odpairs = []
    withinxml = False
    getxmlhead = False

    xmlstartpattern = re.compile(b'^<JourneyPlanningRequest')
    xmlstoppattern = re.compile(b'.*</JourneyPlanningRequest>')
    ipPattern = re.compile(b'^IP')

    with zipfile.ZipFile(filepath) as z:
        for logfile in z.namelist():
            if not os.path.isdir(logfile):
                fileName, fileExtension = os.path.splitext(logfile)
                if fileExtension == ".txt":
                    with z.open(logfile) as f:
                        for line in f:
                            if line:
                                if re.match(ipPattern, line) is not None:
                                    ipvalue = line.decode('utf-8')
                                if re.match(xmlstartpattern, line) is not None:
                                    eachxml += line.decode('utf-8')
                                    withinxml = True
                                    getxmlhead = True
                                elif re.match(xmlstoppattern, line) is not None:
                                    if getxmlhead:
                                        eachxml += line.decode('utf-8')
                                        withinxml = False
                                        getxmlhead = False
                                        odpairs.append(xmlParserString(eachxml))
                                        eachxml=''
                                elif withinxml:
                                    eachxml += line.decode('utf-8')
    z.close()
    return odpairs





def parseXMLZIPALLINFO(filepath):
    eachxml = ''
    ipvalue = ''
    tsvalue = ''
    odpairs = []
    withinxml = False
    getxmlhead = False

    responsestartpattern = re.compile(b'^<JourneyPlanningResponse')
    responsestoppattern = re.compile(b'^</JourneyPlanningResponse>')
    ipPattern = re.compile(b'^IP')
    timestampPattern = re.compile(b'^TimeStamp')
    ipaddrpattern = re.compile(
        r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))')
    tsvaluepattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:\d{4}')

    with zipfile.ZipFile(filepath) as z:
        for logfile in z.namelist():
            if not os.path.isdir(logfile):
                fileName, fileExtension = os.path.splitext(logfile)
                if fileExtension == ".txt":
                    with z.open(logfile) as f:
                        for line in f:
                            if line:
                                if re.match(ipPattern, line) is not None:
                                    ipvalue = line.decode('utf-8')
                                if re.match(timestampPattern, line) is not None:
                                    tsvalue = line.decode('utf-8')
                                if re.match(responsestartpattern, line) is not None:
                                    eachxml += line.decode('utf-8')
                                    withinxml = True
                                    getxmlhead = True
                                elif re.match(responsestoppattern, line) is not None:
                                    if getxmlhead:
                                        eachxml += line.decode('utf-8')
                                        withinxml = False
                                        getxmlhead = False
                                        print(fileName)
                                        eachod = xmlParserResponse(eachxml)
                                        [e.insert(3, re.search(ipaddrpattern, ipvalue).group(0) if re.search(ipaddrpattern, ipvalue) else '0.0.0.0') for e in eachod]
                                        [e.insert(4,
                                                  re.search(tsvaluepattern, tsvalue).group(0) if re.search(
                                                      tsvaluepattern, tsvalue) else '29990101')
                                         for e in eachod]

                                        odpairs.extend(eachod)
                                        eachxml=''
                                elif withinxml:
                                    eachxml += line.decode('utf-8')
    z.close()
    return odpairs



if __name__ == '__main__':
    odpair = []
    odpair = parseXMLfroTXT(r'C:\Logs\F1\LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17.txt')

    result = plog.resultsTableView(odpair)
    odlists = plog.stationlist(odpair)

    print(odlists)
    print(len(odlists))
    print(result.to_string())




