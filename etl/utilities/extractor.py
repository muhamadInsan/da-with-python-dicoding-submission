import pandas as pd


def extract_data(filepath:str, date_col:list=[]):
    
    try:
        df = pd.read_csv(filepath, parse_dates=date_col)
        print('Extract completed ...!')
    
    except FileNotFoundError as err:
        print('File not found ...!', err)
    
    except Exception as err:
        print('Extract data failed ...!', err)

    return df