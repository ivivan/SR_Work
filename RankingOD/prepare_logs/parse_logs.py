import multiprocessing
import re
import xml.etree.cElementTree as ET
from lxml import etree


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
