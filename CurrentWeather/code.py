# 定義查詢即時天氣的函數
def get_current_weather(address):
    result = '找不到即時天氣資訊'  # 預設結果為找不到資訊
    code = 'CWA-66C0912B-B99B-436E-B63B-8005F28532C8'  # 中央氣象局的授權碼
    try:
        # 即時天氣資料查詢網址列表
        url = [
            f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization={code}',
            f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization={code}'
        ]
        for item in url:
            req = requests.get(item)  # 發送請求取得天氣資料
            data = req.json()         # 轉換為 JSON 格式
            station = data['records']['Station']  # 取得氣象站資料
            for i in station:
                city = i['GeoInfo']['CountyName']  # 獲取縣市名稱
                area = i['GeoInfo']['TownName']    # 獲取鄉鎮名稱
                if address in f'{city}{area}':  # 如果地址符合該氣象站位置
                    weather = i['WeatherElement']['Weather']  # 取得天氣狀況
                    temp = i['WeatherElement']['AirTemperature']  # 取得氣溫
                    humid = i['WeatherElement']['RelativeHumidity']  # 取得濕度
                    # 組合回應文字
                    result = f'「{address}」目前天氣狀況「{weather}」，溫度 {temp} 度，相對濕度 {humid}%！'
                    break
    except Exception as e:
        print(e)  # 打印錯誤訊息以便除錯
    return result  # 返回即時天氣資訊
