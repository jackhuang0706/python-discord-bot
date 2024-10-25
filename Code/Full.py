!pip install -q -U google-generativeai
!pip install discord
!pip install nest_asyncio
!pip install pytesseract pillow discord
!apt-get install tesseract-ocr
!apt-get install tesseract-ocr-chi-sim tesseract-ocr-chi-tra  # 安裝中文語言包
# weather
import requests
# picture chatting
import discord
import os
from PIL import Image
import pytesseract
import asyncio
import nest_asyncio # import nest_asyncio to allow nested event loops
import google.generativeai as genai
%env API_KEY=YOUR_API_KEY

# 定義查詢地震資訊的函數
def earth_quake():
    result = []
    code = 'YOUR-OWN-KEY'
    try:
        # 小區域地震資料查詢網址
        url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={code}'
        req1 = requests.get(url)
        data1 = req1.json()
        eq1 = data1['records']['Earthquake'][0]
        t1 = eq1['EarthquakeInfo']['OriginTime']

        # 顯著有感地震資料查詢網址
        url2 = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={code}'
        req2 = requests.get(url2)
        data2 = req2.json()
        eq2 = data2['records']['Earthquake'][0]
        t2 = eq2['EarthquakeInfo']['OriginTime']

        result = [eq1['ReportContent'], eq1['ReportImageURI']]
        if t2 > t1:
            result = [eq2['ReportContent'], eq2['ReportImageURI']]
    except Exception as e:
        print(e)
        result = ['抓取失敗...', '']
    return result
# 定義查詢即時天氣的函數
def get_current_weather(address):
    result = '找不到即時天氣資訊'  # 預設結果為找不到資訊
    code = 'YOUR-OWN-KEY'  # 中央氣象局的授權碼
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

# 定義查詢空氣品質的函數
def get_air_quality(address):
    result = '找不到空氣品質資訊'  # 預設結果為找不到資訊
    code = 'YOUR-OWN-KEY'
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

def get_weather_forecast(address):
    result = '找不到氣象預報資訊'
    code = 'YOUR-OWN-KEY'
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


# 設定中文語言包與 Tesseract 路徑（Colab 預設安裝於 /usr/bin/tesseract）
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
custom_config = r'--oem 3 --psm 6 -l chi_sim+chi_tra'

# 設定 Discord bot token 和 Google Generative AI API 鍵
TOKEN = 'YOUR-TOKEN' #替換為自己的Discord-bot API
API_KEY = os.environ["API_KEY"]

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True  # 允許 bot 讀取訊息內容
client = discord.Client(intents=intents) # 在這裡傳入 intents 参数

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return


 # 檢查是否有圖片附件
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # 支援更多圖片格式
                file_path = f"/content/{attachment.filename}"
                await attachment.save(file_path)

                try:
                    # 使用 PIL 開啟圖片並進行 OCR 轉文字
                    img = Image.open(file_path)
                    text = pytesseract.image_to_string(img, config=custom_config)

                    # 檢查提取的文字是否為空
                    if not text.strip():  # 如果提取內容為空
                        raise ValueError("OCR結果為空")

                    # 在提取到的文字前面加上「圖片顯示」
                    await message.channel.send(f"圖片顯示：\n{text}")

                except ValueError:
                    await message.channel.send("未能識別出圖片中的文字。")

                except Exception as e:
                    if 'contents must not be empty' in str(e):
                        await message.channel.send("未能識別出圖片中的文字。")
                    else:
                        await message.channel.send(f"發生錯誤：{str(e)}")

                finally:
                    os.remove(file_path)  # 刪除臨時文件

    else:
        address = message.content.split(maxsplit=1)[1] if len(message.content.split()) > 1 else ""

        if message.content.startswith('&地震'):
            earthquake_info = earth_quake()
            await message.channel.send(earthquake_info[0])
            if earthquake_info[1]:
                await message.channel.send(earthquake_info[1])

        elif message.content.startswith('&即時天氣') and address:
            weather_info = get_current_weather(address)
            await message.channel.send(weather_info)

        elif message.content.startswith('&氣象預報') and address:
            forecast_info = get_weather_forecast(address)
            await message.channel.send(forecast_info)

        elif message.content.startswith('&空氣品質') and address:
            air_quality_info = get_air_quality(address)
            await message.channel.send(air_quality_info)
        else:
            # 啟用聊天功能，將訊息傳遞給 AI 模型
            prompt = message.content.strip()
            try:
                response = model.generate_content(prompt)
                if hasattr(response, 'text'):  # 檢查是否有 text 屬性
                    await message.channel.send(response.text)
                else:
                    await message.channel.send("無法獲取內容。")
            except Exception as e:
                await message.channel.send(f"出錯了: {e}")

    
    await message.channel.send("--------------------\n")   
    await message.channel.send("指令說明：\n"
                               "(圖片)  - 顯示圖片上的文字\n"
                               "&即時天氣 (縣市名稱) - 查詢即時天氣\n"
                               "&氣象預報 (縣市名稱) - 查詢氣象預報\n"
                               "&空氣品質 (縣市名稱) - 查詢空氣品質\n"
                               "&地震 - 查詢最新地震資訊\n"
                               "(輸入聊天內容) - 陪你聊天"
                               )   


# 导入并应用 nest_asyncio
import nest_asyncio
nest_asyncio.apply()

client.run(TOKEN)
