import os
import re


def splitfile(filepath):
    filedir, name = os.path.split(filepath)
    name, ext = os.path.splitext(name)
    outputname = name.replace('.', '_')
    outputfiledir = os.path.abspath(os.path.join(filedir, os.path.pardir, 'O1', outputname))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)

    partno = 0 
    stream = open(filepath, 'r', encoding='utf-8')
    endPattern = re.compile(r'^End\sof\sResponse\sXML')
    while True:
        partfilename = os.path.join(outputfiledir, name + '_' + str(partno) + ext)
        print('write start %s' % partfilename)
        part_stream = open(partfilename, 'w', encoding='utf-8')
        not_the_end = True
        to_the_end = False

        while not_the_end:
            read_content = stream.readline()
            if read_content:
                if re.match(endPattern, read_content) is None:
                    part_stream.write(read_content)
                else:
                    part_stream.write(read_content)
                    not_the_end = False
            else:
                to_the_end = True
                break
        part_stream.close()

        if to_the_end:
            break
        partno += 1

    print('done')


if __name__ == '__main__':
    splitfile(r'C:\Logs\F1\LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17.txt')
