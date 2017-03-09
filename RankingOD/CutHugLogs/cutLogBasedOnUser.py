import phoenixdb
import os
import re
from pprint import pprint

# cursor
# ipValue = ''
# tsValue = ''
# tagsValue = ''
# requestXML = []
# responseXML = []

# def databaseConnection(db_addr):
#     global cursor
#     conn = phoenixdb.connect(db_addr, autocommit=True)
#     cursor = conn.cursor()


def logToHbase(filepath):
    stream = open(filepath, 'r', encoding='utf-8')

    endPattern = re.compile(r'^End\sof\sResponse\sXML')
    endRequestPattern = re.compile(r'^End\sof\sRequest\sXML')
    startPattern = re.compile(r'^REQUEST')
    ipPattern = re.compile(r'^IP')
    timestampPattern = re.compile(r'^TimeStamp')
    tagsPattern = re.compile(r'^Tags')
    xmlPattern = re.compile(r'^XML')

    xmlstartpattern = re.compile(r'.*<.*')

    ipaddrpattern = re.compile(r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))')



    not_the_end = True
    requestHeadFinished = False
    requestBodyFinished = False
    responseHeadFinished = False
    responseBodyFinished = False

    getIP = False
    getTS = False
    getTags = False

    # global ipValue
    # global tsValue
    # global tagsValue
    # global requestXML
    # global responseXML

    ipValue = ''
    tsValue = ''
    tagsValue = ''
    requestXML = []
    responseXML = []

    while not_the_end:
        read_content = stream.readline()

        if read_content:
            if not (getIP and getTS and getTags):
                if re.match(timestampPattern, read_content) is not None:
                    tsValue = read_content
                    getTS = True
                if re.match(ipPattern, read_content) is not None:
                    ipValue = read_content
                    getIP = True
                if re.match(tagsPattern, read_content) is not None:
                    tagsValue = read_content
                    getTags = True

            elif not requestBodyFinished:
                if re.match(endRequestPattern, read_content) is None:
                    if re.match(xmlstartpattern, read_content) is not None:
                        requestXML.append(read_content)
                else:
                    requestBodyFinished = True

            elif not responseBodyFinished:
                if re.match(endPattern, read_content) is None:
                    if re.match(xmlstartpattern, read_content) is not None:
                        responseXML.append(read_content)
                else:
                    responseBodyFinished = True
                    not_the_end = False
                    break
    stream.close()

    # print(ipValue)
    print(re.search(r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))', ipValue).group(0))
    #print(tsValue)

    print(re.search(r'\d{4}.*', tsValue).group(0))
    #print(tagsValue)

    if re.search(r'Base.*', tagsValue):
        print(re.search(r'Base.*', tagsValue).group(0))


    pprint(requestXML)


    # pprint(responseXML)

if __name__ == '__main__':
    # logToHbase(r'C:\Logs\O1\LIV2-IPTAPP102-MessageRelayLog_[2016-06-13]_17\LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17_1.txt')
    files = []
    for entry in os.scandir(r'C:\Logs\O1\try'):
        if entry.is_file():
            files.append(entry.path)

    for f in files:
        logToHbase(f)

