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
        od.append([x.text if origin else 'NONE', y.text if destination else 'NONE',
                   distance.text if distance is not None else '0', list(set(provider_code)) if all_codes is not None else []])

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
        od.append([x.text if origin else 'NONE', y.text if destination else 'NONE',
                   distance.text if distance is not None else '0', list(set(provider_code)) if all_codes is not None else []])

    return od


def test_lxml(filepath):
    # tree = etree.ElementTree(etree.fromstring(filepath))
    tree = etree.parse(open(filepath))
    root = tree.getroot()
    m = re.match('\{.*\}', root.tag)
    namespace = m.group(0) if m else ''

    originstations = []
    destinationstatoins = []
    distances = []
    servicecodes = set()
    od = []

    finddistance = False

    # count = 0
    # for element in root.iter(namespace+'JourneyList', namespace+'JourneyPlanningRequest'):
    #     for j in element.iter(namespace+'Distance'):
    #         count += 1
    #         if j.tag == namespace+'Distance':
    #             distances.append(j.text)
    #             break
    # print(count)
    # print(distances)

    for element in root.iter(namespace+'Distance', namespace+'Location', namespace+'PrimaryServiceProviderCode'):
        # count += 1
        if not finddistance and element.tag == namespace+'Distance':
            distances.append(element.text)
            finddistance = True
        elif element.tag == namespace+'Location':
            if element.getparent().tag == namespace+'OriginList':
                originstations.append(element.text)
            else:
                destinationstatoins.append(element.text)
        elif element.tag == namespace+'PrimaryServiceProviderCode':
            servicecodes.add(element.text)

    # if element.tag == namespace+'Location' and element.getparent().tag == namespace+'OriginList':
    #     originstations.append(element.text)
    # if element.tag == namespace+'Location' and element.getparent().tag == namespace+'DestinationList':
    #     destinationstatoins.append(element.text)
    # if not finddistance and element.tag == namespace+'Distance':
    #     distances.append(element.text)
    #     finddistance = True
    # if element.tag == namespace+'PrimaryServiceProviderCode':
    #     servicecodes.add(element.text)
    # count += 1
    # print(count)
    # print(originstations)
    # print(destinationstatoins)
    # print(distances)
    # print(servicecodes)

    for x, y in zip(originstations, destinationstatoins):
        od.append([x if originstations is not None else 'NONE', y if destinationstatoins is not None else 'NONE',
                   distances[0] if distances is not None else '0', list(servicecodes) if servicecodes is not None else []])
    # print(od)
    return od


if __name__ == '__main__':
    multiprocessing.freeze_support()
    test_lxml(
        r'/Users/Ivan/Downloads/TEST/LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17_1.txt')
