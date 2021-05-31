# TODO need import sanitization
import csv
import io
import re
import zipfile
from datetime import datetime, timedelta
from io import TextIOWrapper

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
}

CSV_HEAD_CONVERSION = {
    'SC_CODE': 'CODE',
    'SC_NAME': 'NAME',
    'OPEN': 'OPEN',
    'HIGH': 'HIGH',
    'LOW': 'LOW',
    'CLOSE': 'CLOSE'
}


def content_scooby(download_date):
    try:
        bhav_copy_link = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{download_date}_CSV.ZIP'
        target_csv = f'./downloads/csv/{download_date}.csv'

        with requests.get(bhav_copy_link, headers=headers, verify='./bseindia-com.pem', stream=True) as response:
            response.raise_for_status()
            columns = ['code', 'name', 'open', 'close', 'high', 'low']
            data = unzip(response.content)
            write_buffer(data, target_csv)

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


def write_buffer(data, target):
    with open(target, "w") as csv_file:
        csv_writer = csv.DictWriter(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL,
            lineterminator='\n', fieldnames=CSV_HEAD_CONVERSION.keys()
        )
        # TODO * and will segment code from here to REDIS after django setup and DB connection
        csv_writer.writerow(CSV_HEAD_CONVERSION)
        for row in data:
            csv_writer.writerow(row)


if __name__ == '__main__':
    try:
        custom_date = input('Provide custom download date format should be ddmmyyyy\n')
        if not re.match('^([0-2][0-9]|(3)[0-1])(((0)[0-9])|((1)[0-2]))\d{4}$', custom_date):
            custom_date = datetime.today()
        else:
            datetime.strftime('%d%m%y')

        how_back_ref = input('How many days back ?')
        if isinstance(how_back_ref, int):
            custom_date = (datetime.today() - timedelta(days=int(how_back_ref))).strftime('%d%m%y')

        which_day = custom_date.weekday()

        if which_day > 5:
            do_agree = input('Selected date is weekend !! do you need last friday\'s data ? (Y/N)\n')
            if do_agree.lower() in ['y', 'yes']:
                how_back_ref = 2 if which_day == 6 else 1
            else:
                exit('Enjoy Your Weekend')

        content_scooby(custom_date)

        print('Hurray !! \nExecution Completed')

    except TimeoutError as te:
        print(te)
    except BaseException as b:
        print(f'\nError:\n{b}')
