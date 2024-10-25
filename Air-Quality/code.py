# 定義查詢空氣品質的函數
def get_air_quality(address):
    result = '找不到空氣品質資訊'  # 預設結果為找不到資訊
    code = 'CWA-66C0912B-B99B-436E-B63B-8005F28532C8'
    try:
        # 空氣品質查詢網址
        url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
        req = requests.get(url)  # 發送請求取得空氣品質資料
        data = req.json()        # 轉換為 JSON 格式
        records = data['records']  # 取得所有空氣品質紀錄
        for item in records:
            county = item['county']  # 縣市名稱
            sitename = item['sitename']  # 監測站名稱
            aqi = int(item['aqi'])  # AQI 數值
            # 將 AQI 分級轉為描述
            aqi_status = ['良好', '普通', '對敏感族群不健康', '對所有族群不健康', '非常不健康', '危害']
            msg = aqi_status[aqi // 50]
            # 如果地址符合縣市或監測站名稱，則組合回應文字
            if county in address or sitename in address:
                result = f'「{address}」的空氣品質（AQI）：{aqi}，狀態：{msg}。'
                break
    except Exception as e:
        print(e)  # 打印錯誤訊息以便除錯
    return result  # 返回空氣品質資訊
