"""
Copyright(c) 2020 Tatsuro Watanabe
https://github.com/ktpcschool/geocoding
"""

import json
import os

from urllib.parse import urlencode
from urllib.request import urlopen


def geocode(address):
    """
    引数で指定した住所をジオコーディングして、経度と緯度を返す
    :param address: 住所
    :return : 経度・緯度
    """

    # Yahoo!ジオコーダAPIのURL
    yahoo_geocoder_api_url = 'https://map.yahooapis.jp/geocode/V1/geoCoder'

    # アプリケーションIDは環境変数から取得する
    url = yahoo_geocoder_api_url + '?' + urlencode({
        'appid': os.environ['YAHOOJAPAN_APP_ID'],
        'output': 'json',
        'query': address,
        'recursive': 'true',
    })

    response_text = urlopen(url).read()
    response = json.loads(response_text.decode('utf-8'))
    print(response)

    if 'Feature' not in response:
        # ジオコーディングで結果が得られなかった場合はNoneを返す
        return None

    # Coordinatesというキーの値を,で分割
    coordinates = response['Feature'][0]['Geometry']['Coordinates'].split(',')

    return coordinates[0], coordinates[1]


def main():
    address = '静岡県掛川市'
    try:
        lon, lat = geocode(address)
    except TypeError:
        lon, lat = '変換不可', '変換不可'
    print(lon, lat)


if __name__ == '__main__':
    main()
