# 定義查詢即時天氣的函數
def get_current_weather(address):
    result = '找不到即時天氣資訊'  # 預設結果為找不到資訊
    code = 'YOUR-CODE'  # 替換成實際的授權碼(中央氣象局)
    try:
        # 抓取即時天氣資料
        url = [
            f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization={code}',
            f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization={code}'
        ]
        for item in url:
            req = requests.get(item) 
            data = req.json()        
            station = data['records']['Station']  # 取得氣象站資料
            for i in station:
                city = i['GeoInfo']['CountyName']  # 縣市名稱
                area = i['GeoInfo']['TownName']    # 鄉鎮名稱
                if address in f'{city}{area}':  # 如果地址符合該氣象站位置
                    weather = i['WeatherElement']['Weather']  # 天氣狀況
                    temp = i['WeatherElement']['AirTemperature']  # 氣溫
                    humid = i['WeatherElement']['RelativeHumidity']  # 濕度
                    result = f'「{address}」目前天氣狀況「{weather}」，溫度 {temp} 度，相對濕度 {humid}%！'
                    break
    except Exception as e:
        print(e)  # 除錯用
    return result 
