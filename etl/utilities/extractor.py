import pandas as pd
import os


def csv_file_path(path_file):
    return os.path.abspath(path_file) 


def extract_data(filepath:str, date_col:list=[]):
    
    try:
        df = pd.read_csv(csv_file_path(filepath), parse_dates=date_col)
        print('Extract completed ...!')
    
    except FileNotFoundError as err:
        print('File not found ...!', err)
    
    except Exception as err:
        print('Extract data failed ...!', err)
    
    return df