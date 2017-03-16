import multiprocessing
import re
import xml.etree.cElementTree as ET
from lxml import etree


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


def test_lxml(filepath):
    """use lxml to parse xml body"""
    tree = etree.ElementTree(etree.fromstring(filepath))
    root = tree.getroot()
    m = re.match('\{.*\}', root.tag)
    namespace = m.group(0) if m else ''

    originstations = []
    destinationstatoins = []
    distances = []
    servicecodes = set()
    od = []
    finddistance = False

    for element in root.iter(namespace+'Distance', namespace+'Location', namespace+'PrimaryServiceProviderCode'):
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

    for x, y in zip(originstations, destinationstatoins):
        od.append([x if originstations is not None else 'NONE', y if destinationstatoins is not None else 'NONE',
                   distances[0] if distances else '0', list(servicecodes) if servicecodes is not None else []])
    return od


if __name__ == '__main__':
    multiprocessing.freeze_support()
    test_lxml(
        r'/Users/Ivan/Downloads/TEST/LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17_1.txt')
