from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ...models.import_duty import CacheRouter
from django.conf import settings
import csv
import io
import re
import zipfile
from datetime import datetime, timedelta
from io import TextIOWrapper

import requests

class ImportHandlerViewSet(viewsets.ViewSet):
    queryset = '',
    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dbOperation = CacheRouter()
        self.USABLE_COLUMNS = settings.CSV_HEAD_CONVERSION.keys()
        
    @action(detail=False, methods=['get'], description="Importing Custom Bhavcopy", name="Importing Bhavcopy")
    def handle_bhavcopy_custom_download(self, request, custom_date, how_back_ref=0, version=1):
        try:
            if settings.CLI_MODE:
                custom_date = input('Provide custom download date format should be ddmmyyyy? (Press ENTER for skip)\n')
                
            if re.match('^([0-2][0-9]|(3)[0-1])(((0)[0-9])|((1)[0-2]))\d{2}$', custom_date):
                custom_date = datetime.strptime(custom_date, '%d%m%y')
            else:
                how_back_ref = input('If not custom date then how many days back do you want to fetch ? (Press ENTER for today)\n')
                custom_date = (datetime.today() - timedelta(days=int(how_back_ref if how_back_ref else 0)))
                    
            if (datetime.today() - custom_date).days < 0:
                raise ValueError('We are yet not dealing in future dates.....')
                
            which_day = custom_date.weekday()
            if which_day >= 5:
                if settings.CLI_MODE:
                    do_agree = input('Selected date is weekend! should we import data from friday before this date ? (Y/N)\n')
                    if do_agree.lower() in ['y', 'yes']:
                        how_back_ref = int(how_back_ref) + 2 if which_day == 6 else 1
                        custom_date = (custom_date - timedelta(days=int(how_back_ref)))
                    else:
                        raise ValueError('Enjoy Your Weekend')
                else:
                    raise ValueError('Selected date is weekend! BSE have weekends off.')
                
            return self._handle_bhavcopy_download(custom_date.strftime('%d%m%y'))
        
        except TimeoutError as te:
            print(te)
        except ValueError as errval:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=errval.__str__())
        except BaseException as b:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=f'Error:{b}')

    def __import_bhavcopy_with_cron(self, request, version=1, date='today'):
        self.dbOperation.create_many({date: 'not_today', 'today': date})
        resultant = self.dbOperation.find_many(['today', date])

        return Response(status=status.HTTP_200_OK, data=resultant)

    def _handle_bhavcopy_download(self, download_date):
        try:
            bhav_copy_link = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{download_date}_CSV.ZIP'
            target_csv = f'./csv_collection/{download_date}.csv'

            with requests.get(bhav_copy_link, headers=settings.DEFAULT_HEADERS, stream=True) as response:
                response.raise_for_status()
                data = self._unzip(response.content)
                
                response = self._write_csv(data, target_csv) if settings.TO_CSV_FLAG else self._write_buffer(data)
                return Response(status=status.HTTP_200_OK, data=response)
            
        except requests.exceptions.HTTPError as errh:
            return Response(status=errh.code, data=errh)
        except requests.exceptions.ConnectionError as errc:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Error Connecting:{errc}")
        except requests.exceptions.Timeout as errt:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Timeout Error:{errt}")
        except requests.exceptions.RequestException as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Oops:{err}")
        except ValueError as errv:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Incorrect Parameter:{errv}")


    def _unzip(self, source):
        zip_buffer = io.BytesIO(source)
        data = []
        with zipfile.ZipFile(zip_buffer, "r") as zip_ref:
            extraction_file = zip_ref.namelist()[0]
            if extraction_file.split('.')[-1].lower() != 'csv':
                raise FileNotFoundError('Incorrect CSV file in ZIP')

            with zip_ref.open(extraction_file) as myfile:
                for rows in csv.DictReader(TextIOWrapper(myfile, 'utf-8')):
                    data.append({key: value for key, value in dict(rows).items() if key in self.USABLE_COLUMNS})
        exit(data)
        return data


    def _write_csv(self, data, target):
        with open(target, "w") as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL,
                lineterminator='\n', fieldnames=self.USABLE_COLUMNS
            )
            csv_writer.writerow(settings.CSV_HEAD_CONVERSION)
            for row in data:
                csv_writer.writerow(row)
        return data

    def _write_buffer(self, data):
        self.dbOperation.create_many(data)
        return True
