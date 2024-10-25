# 查詢空氣品質
def get_air_quality(address):
    result = '找不到空氣品質資訊'  # 預設結果為找不到資訊
    code = 'YOUR-CODE' # 替換成實際的授權碼(環保署)
    try:
        # 空氣品質查詢
        url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
        req = requests.get(url) 
        data = req.json()        
        records = data['records']  # 所有空氣品質紀錄
        for item in records:
            county = item['county']  # 縣市名稱
            sitename = item['sitename']  # 監測站名稱
            aqi = int(item['aqi'])  # AQI 數值
            # 將 AQI 分級轉為描述
            aqi_status = ['良好', '普通', '對敏感族群不健康', '對所有族群不健康', '非常不健康', '危害']
            msg = aqi_status[aqi // 50]
            # 組合回應文字
            if county in address or sitename in address:
                result = f'「{address}」的空氣品質（AQI）：{aqi}，狀態：{msg}。'
                break
    except Exception as e:
        print(e)  # 除錯用
    return result
