import os
import re
import xml.etree.ElementTree as ET
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

def xmlParserResponse(filepath):
    e = ET.parse(filepath)
    root = e.getroot()
    m = re.match('\{.*\}', root.tag)
    namespace = m.group(0) if m else ''
    od = []
    providercode = []
    originlist = []
    destinationlist = []
    distance = ''

    originlist = e.find('.//'+namespace+'OriginList')
    destinationlist = e.find('.//'+namespace+'DestinationList')
    distance = e.find('.//'+namespace+'Distance')
    for e in e.findall('.//'+namespace+'PrimaryServiceProviderCode'):
        providercode.append(e.text)

    for x,y in zip(originlist,destinationlist):
        od.append([x.text if originlist else 'NONE',y.text,distance.text if distance !='' else '0' ,list(set(providercode))])

    return od

if __name__ == '__main__':

    odpairs = []
    oneod = []

    #oneod = xmlParser(r'C:\Logs\O1\LIV2-IPTAPP102-MessageRelayLog_[2016-06-13]_17\LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17_0.xml')
    oneod = xmlParserResponse(r'C:\Logs\O1\LIV2-IPTAPP102-MessageRelayLog_[2016-06-13]_17\LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17_0.xml')

    [e.insert(3, 'dd') for e in oneod]
    [e.insert(4, 'ff') for e in oneod]
    print(oneod)


    odpairs.extend(oneod)
    # print(oneod)
    print(odpairs)

    # print([e.insert(3, 'dd') for e in oneod])
    # print(oneod)
