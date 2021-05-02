# TODO need import sanitization
from urllib import request
import requests
import tempfile
import shutil
from datetime import datetime, timedelta
import csv, zipfile, os
import requests
from datetime import datetime, timedelta
from io import TextIOWrapper, StringIO
import pandas as pd
import io

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
}

CSV_HEAD_CONVERSION = {
    'SC_CODE': 'CODE', 
    'SC_NAME': 'NAME', 
    'OPEN':'OPEN', 
    'HIGH':'HIGH', 
    'LOW': 'LOW', 
    'CLOSE': 'CLOSE'
}

def scooby(any_other_day=None):
    try:
        today = datetime.today()
        which_day = today.weekday()

        if which_day > 5:
            do_agree = input('Today is weekend !! do you need last friday\'s data ? (Y/N)\n')
            if do_agree.lower() == 'y':
                how_back = 2 if which_day == 6 else 1
            else:
                return 1
            
        download_date = any_other_day if any_other_day else (datetime.today() - timedelta(days=how_back)).strftime('%d%m%y')
        bhav_copy_link = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{download_date}_CSV.ZIP'

        with requests.get(bhav_copy_link, headers=headers, verify='./bseindia-com.pem', stream=True) as response:
            response.raise_for_status()
            columns = ['code','name', 'open', 'close', 'high', 'low']
            data = unzip(response.content)
            target_csv = f'./downloads/csv/{download_date}.csv'
            writeCSV(data, target_csv, columns)
            
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)
        
def unzip(source):
    buffer = io.BytesIO(source)
    data = []
    with zipfile.ZipFile(buffer, "r") as zip_ref:
        extraction_file = zip_ref.namelist()[0]
        if extraction_file.split('.')[-1].lower() != 'csv':
            raise FileNotFoundError('Incorrect CSV file in ZIP')
        
        with zip_ref.open(extraction_file) as myfile:
            for rows in csv.DictReader(TextIOWrapper(myfile, 'utf-8')):
                data.append({key: value for key, value in dict(rows).items() if key in CSV_HEAD_CONVERSION.keys()})
    
    # TODO we will do the redis operation here from next (*) so need not to obstruct ROM at all
    return data


def writeCSV(data, target, header):
    f = StringIO(','.join(header))
    reader = csv.reader(headers)
    
    with open(target, "w") as csv_file:
        csv_writer = csv.DictWriter(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, 
            lineterminator='\n', fieldnames = CSV_HEAD_CONVERSION.keys()
        )
        # TODO * and will segement code from here to REDIS after django setup and DB connection
        csv_writer.writerow(CSV_HEAD_CONVERSION)
        for row in data:
            csv_writer.writerow(row)
                
if __name__ == '__main__':
    try:
        scooby()
        print('Hurray !! \nExecution Completed')
    except TimeoutError as te:
        print(te)
    except BaseException as b:
        print(f'\nError:\n{b}')
