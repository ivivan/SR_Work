import os
import pandas as pd


def log_results_convert(filepath):
    """log resutls for one day"""
    files = []
    filedir, name = os.path.split(filepath)
    for entry in os.scandir(filepath):
        if entry.is_file():
            if entry.name.endswith(".csv"):
                files.append(entry.path)

    if len(files) < 2:
        print('Need two log result files')
    else:
        df_one = pd.read_csv(files[0],index_col=0)
        df_two = pd.read_csv(files[1],index_col=0)

    result = df_one.append(df_two)
    result['Date'] = name  # add date column, date is just the filename
    outputfiledir = os.path.abspath(os.path.join(filedir, os.path.pardir,'join_logs',name))
    if not os.path.exists(outputfiledir):
        os.makedirs(outputfiledir)
    csvfile = os.path.join(outputfiledir, name + '.csv')
    result.to_csv(csvfile, sep=',', encoding='utf-8', index=False)  # csv for OD pairs, distance and servic eprovider code


if __name__ == '__main__':
    log_results_convert(r'C:\work\project\logprocess\download_log\20170307')
