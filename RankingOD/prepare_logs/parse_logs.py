import multiprocessing
import re
# import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
from lxml import etree
from io import StringIO, BytesIO

def parse_response_xml(xmlstring):
    """extract information from response xml body in logs"""
    e = ET.ElementTree(ET.fromstring(xmlstring))
    root = e.getroot()
    m = re.match('\{.*\}', root.tag)
    namespace = m.group(0) if m else ''
    od = []
    provider_code = []

    origin = e.find('.//'+namespace+'OriginList')
    destination = e.find('.//'+namespace+'DestinationList')
    distance = e.find('.//'+namespace+'Distance')
    all_codes = e.findall('.//'+namespace+'PrimaryServiceProviderCode')

    if all_codes is not None:
        for e in all_codes:
            provider_code.append(e.text)

    for x, y in zip(origin, destination):
        od.append([x.text if origin else 'NONE', y.text if destination else 'NONE', distance.text if distance is not None else '0', list(set(provider_code)) if all_codes is not None else []])

    return od

def parse_response_xml_lxml(xmlstring):
    """extract information from response xml body in logs"""

    e = etree.ElementTree(etree.fromstring(xmlstring))
    root = e.getroot()
    m = re.match('\{.*\}', root.tag)
    namespace = m.group(0) if m else ''
    od = []
    provider_code = []

    origin = e.find('.//'+namespace+'OriginList')
    destination = e.find('.//'+namespace+'DestinationList')
    distance = e.find('.//'+namespace+'Distance')
    all_codes = e.findall('.//'+namespace+'PrimaryServiceProviderCode')

    if all_codes is not None:
        for e in all_codes:
            provider_code.append(e.text)

    for x, y in zip(origin, destination):
        od.append([x.text if origin else 'NONE', y.text if destination else 'NONE', distance.text if distance is not None else '0', list(set(provider_code)) if all_codes is not None else []])

    return od

if __name__ == '__main__':
    multiprocessing.freeze_support()