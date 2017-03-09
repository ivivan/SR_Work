import os
import re

def splitfile(filepath,linesize=5000):
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    outputname = name.replace('.','_')
    outputfiledir = os.path.abspath(os.path.join(filedir,os.path.pardir,'O1',outputname))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)

    partno = 0;
    stream = open(filepath,'r',encoding='utf-8')
    while True:
        partfilename = os.path.join(outputfiledir,name+ '_' + str(partno) + ext)
        print('write start %s' % partfilename)
        part_stream = open(partfilename,'w',encoding='utf-8')

        read_count = 0
        while read_count < linesize:
            read_content = stream.readline()
            if read_content:
                part_stream.write(read_content)
            else:
                break
            read_count += 1
        part_stream.close()
        if(read_count < linesize):
            break
        partno += 1
    print('done')

if __name__ == '__main__':
    splitfile(r'C:\Logs\F1\LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17.txt',5000)
