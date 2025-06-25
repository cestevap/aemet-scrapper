import os
import requests
from datetime import datetime, timezone
import tarfile
import io
import time
import sys


def fetch_data():
    headers = {'accept': 'application/json'}
    params = {'api_key': API_KEY}
    retries = 0
    while retries < 3:
        try:
            r = requests.get(URL, headers=headers, params=params)
            if r.status_code != 200:
                print("API call failed:", r.status_code)
                raise Exception("Failed to get initial data")

            data_url = r.json()['datos']
            data = requests.get(data_url).text.encode('utf-8')
            now = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
            os.makedirs('output/', exist_ok=True)
            archive_path = f'output/aemet_obs_{now}.json.tar.xz'

            data_io = io.BytesIO(data)
            info = tarfile.TarInfo(name=f'aemet_obs_{now}.json')
            info.size = len(data)

            with tarfile.open(archive_path, 'w:xz') as tar:
                tar.addfile(tarinfo=info, fileobj=data_io)
            print(f"Downloaded at {now}")
            break
        except Exception as e:
            retries = retries + 1
            print(f"Error: {e}")
            print("Retrying in 30 seconds...")
            time.sleep(15)
    else:
        print("Failed to download data after 10 retries.")
        sys.exit(1)

if __name__ == '__main__':
    URL = 'https://opendata.aemet.es/opendata/api/observacion/convencional/todas'
    API_KEY = os.getenv('AEMET_API_KEY')
    if API_KEY.startswith('eyJ'):
        print("Correct apy key")
    else:
        print("incorrect apy key: {}".format(API_KEY))
    fetch_data()
