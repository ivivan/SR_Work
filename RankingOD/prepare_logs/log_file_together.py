import os
import pandas as pd


def log_results_convert(filepath):
    """log resutls for one day"""
    files = []
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".csv"):
                files.append(entry.path)

    if len(files) < 2:
        print('Need two log result files')
    else:
        df_one = pd.read_csv(files[0])
        df_two = pd.read_csv(files[1])

    result = df_one.append(df_two, ignore_index=True)
    filedir,name = os.path.split(filepath)
    outputfiledir = os.path.abspath(os.path.join(filedir, 'all_logs'))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)
    csvfile = os.path.join(outputfiledir, 'join' + '.csv')
    result.to_csv(csvfile, sep=',', encoding='utf-8', index=False)  # csv for OD pairs, distance and servic eprovider code


if __name__ == '__main__':
    log_results_convert(r'C:\work\project\Logdata')
