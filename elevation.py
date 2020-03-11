"""
Copyright(c) 2020 Tatsuro Watanabe
https://github.com/ktpcschool/geocoding
"""

import json
import re
import sys

from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


def check_input_data(lon, lat):
    regex_lon = re.compile('^[-+]?\d{1,3}\.?\d*$')
    regex_lat = re.compile('^[-+]?\d{1,2}\.?\d*$')
    lon_match = regex_lon.match(lon)
    lat_match = regex_lat.match(lat)

    if lon_match and lat_match and (-180 <= float(lon) <= 180) and (-90 <= float(lat) <= 90):
        return True
    else:
        return False


def get_elevation(lon, lat):
    """
    引数で指定した経度と緯度から標高と標高データのデータソースを返す
    :param lon: 経度
    :param lat: 緯度
    :return　elevation, hsrc: 標高、標高データのデータソース
    """

    # 国土地理院の標高APIのURL
    elevation_api_url = 'https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php'

    # アプリケーションIDは環境変数から取得する。
    url = elevation_api_url + '?' + urlencode({
        'lon': lon,
        'lat': lat,
        'outtype': 'JSON',
    })

    response_text = urlopen(url).read()
    response = json.loads(response_text.decode('utf-8'))
    # print(response)
    elevation = response['elevation']
    hsrc = response['hsrc']
    return elevation, hsrc


def main():
    lon, lat = '137.99816750', '34.76876630'

    # 経度、緯度のデータが正しいか調べる
    if not check_input_data(lon, lat):
        print('経度、緯度の値を正しく入力してください。')
        sys.exit()

    try:
        elevation, hsrc = get_elevation(lon, lat)
        if elevation == '-----' or hsrc == '-----':
            elevation = '取得不可'
            hsrc = '取得不可'

        print('標高値: {}'.format(elevation))
        print('標高データのデータソース: {}'.format(hsrc))
    except HTTPError as e:
        print('Error code: ', e.code)
    except URLError as e:
        print('Reason: ', e.reason)
    except Exception as e:
        print('他のエラーです: ', e)


if __name__ == '__main__':
    main()
