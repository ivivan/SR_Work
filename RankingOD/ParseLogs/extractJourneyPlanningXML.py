import os
import re

def splitfile(filepath):
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    outputname = name.replace('.','_')
    outputfiledir = os.path.abspath(os.path.join(filedir,os.path.pardir,'O1',outputname))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)

    partno = 0
    stream = open(filepath,'r',encoding='utf-8')
    xmlstartpattern = re.compile(r'^<JourneyPlanningRequest')
    xmlstoppattern = re.compile(r'.*</JourneyPlanningRequest>')
    ipPattern = re.compile(r'^IP')

    while True:
        partfilename = os.path.join(outputfiledir,name+ '_' + str(partno) + '.xml')
        print('write start %s' % partfilename)
        part_stream = open(partfilename,'w',encoding='utf-8')
        not_the_end = True
        to_the_end = False
        withinxml = False
        getxmlhead = False
        ipvalue = ''

        while not_the_end:
            read_content = stream.readline()
            if read_content:
                if re.match(ipPattern, read_content) is not None:
                    ipvalue = read_content
                if re.match(xmlstartpattern, read_content) is not None:
                    part_stream.write(read_content)
                    withinxml = True
                    getxmlhead = True
                elif re.match(xmlstoppattern, read_content) is not None:
                    if getxmlhead:
                        part_stream.write(read_content)
                        withinxml = False
                        not_the_end = False
                        getxmlhead = False
                elif withinxml:
                    part_stream.write(read_content)
            else:
                to_the_end = True
                break


        part_stream.close()

   #     newoutputfilename = os.path.join(outputfiledir, name + '.[' + re.search(r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))', ipvalue).group(0) + '].' + str(partno) + '.xml')
    #    os.rename(partfilename, newoutputfilename)

        if to_the_end:
            os.remove(partfilename)
            break
        partno += 1

    print('done')

if __name__ == '__main__':
    splitfile(r'C:\Logs\F1\LIV2-IPTAPP102-MessageRelayLog.[2016-06-13].17.txt')