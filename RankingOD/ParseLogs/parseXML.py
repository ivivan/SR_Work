import os
import re
import xml.etree.ElementTree as ET

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

if __name__ == '__main__':

    odpairs = []
    oneod = []

    oneod = xmlParser(r'C:\Logs\O1\LIV2-IPTAPP102-MessageRelayLog_[2016-06-13]_17\LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17.[172.22.136.186].9173.xml')
    odpairs.append(oneod)
    print(odpairs)
