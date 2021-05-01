import requests

def scooby(today_bhav_date = '300421'):
	bhav_copy_link = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{today_bhav_date}_CSV.ZIP'

	with requests.get(bhav_copy_link) as bhav_content:
		print(bhav_content)
			
if __name__ == '__main__':
	scooby()