"""
Copyright(c) 2020 Tatsuro Watanabe
https://github.com/ktpcschool/geocoding
"""

import json
import os
import re
import sys

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


def reverse_geocode(lon, lat):
    """
    引数で指定した経度と緯度をリバースジオコーディングして、住所を返す
    :param lon: 経度
    :param lat: 緯度
    :return: 住所
    """

    # Yahoo!リバースジオコーダAPIのURL
    yahoo_reverse_geocoder_api_url = 'https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder'

    # アプリケーションIDは環境変数から取得する。
    url = yahoo_reverse_geocoder_api_url + '?' + urlencode({
        'appid': os.environ['YAHOOJAPAN_APP_ID'],
        'lat': lat,
        'lon': lon,
        'output': 'json',
    })

    response_text = urlopen(url).read()
    response = json.loads(response_text.decode('utf-8'))
    print(response)
    
    if 'Feature' not in response:
        # リバースジオコーディングで結果が得られなかった場合はNoneを返す
        return None

    # Addressを取得
    address = response['Feature'][0]['Property']['Address']

    return address


def main():
    lon, lat = '137.99816750', '34.76876630'

    # 経度、緯度のデータが正しいか調べる
    if not check_input_data(lon, lat):
        print('経度、緯度の値を正しく入力してください。')
        sys.exit()

    try:
        address = reverse_geocode(lon, lat)
        if not address:
            address = '変換不可'
    except TypeError:
        address = '変換不可'
    print(address)


if __name__ == '__main__':
    main()
