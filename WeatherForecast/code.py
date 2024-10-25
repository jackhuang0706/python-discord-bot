def get_weather_forecast(address):
    result = '找不到氣象預報資訊'
    code = 'CWA-66C0912B-B99B-436E-B63B-8005F28532C8'
    api_list = {
        "宜蘭縣": "F-D0047-001", "桃園市": "F-D0047-005", "新竹縣": "F-D0047-009",
        "苗栗縣": "F-D0047-013", "彰化縣": "F-D0047-017", "南投縣": "F-D0047-021",
        "雲林縣": "F-D0047-025", "嘉義縣": "F-D0047-029", "屏東縣": "F-D0047-033",
        "臺東縣": "F-D0047-037", "花蓮縣": "F-D0047-041", "澎湖縣": "F-D0047-045",
        "基隆市": "F-D0047-049", "新竹市": "F-D0047-053", "嘉義市": "F-D0047-057",
        "臺北市": "F-D0047-061", "高雄市": "F-D0047-065", "新北市": "F-D0047-069",
        "臺中市": "F-D0047-073", "臺南市": "F-D0047-077", "連江縣": "F-D0047-081",
        "金門縣": "F-D0047-085"
    }
    try:
        for name in api_list:
            if name in address:
                city_id = api_list[name]
                url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/{city_id}?Authorization={code}&elementName=WeatherDescription'
                req = requests.get(url)
                data = req.json()
                location = data['records']['locations'][0]['location']
                city = data['records']['locations'][0]['locationsName']
                for item in location:
                    area = item['locationName']
                    note = item['weatherElement'][0]['time'][0]['elementValue'][0]['value']
                    if address in f'{city}{area}':
                        result = f'「{address}」的氣象預報：\n{note}'
                        break
    except Exception as e:
        print(e)
    return result
