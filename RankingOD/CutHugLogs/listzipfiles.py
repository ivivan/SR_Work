import zipfile

def zip_summary(filepath):
    zfile = zipfile.ZipFile(filepath,'r')
    filecount = 0
    for filename in zfile.namelist():
        print(filename)
        filecount += 1
    print(filecount)

if __name__ == '__main__':
    zip_summary(r'C:\Logs\F1.20160613.zip')
