!pip install -q -U google-generativeai
!pip install discord
!pip install nest_asyncio
!pip install pytesseract pillow discord
!apt-get install tesseract-ocr
!apt-get install tesseract-ocr-chi-sim tesseract-ocr-chi-tra

import requests
import discord
import os
from PIL import Image
import pytesseract
import asyncio
import nest_asyncio
import google.generativeai as genai
%env API_KEY=YOUR_API_KEY

def earth_quake():
    result = []
    code = 'YOUR-OWN-KEY'
    try:
        url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={code}'
        req1 = requests.get(url)
        data1 = req1.json()
        eq1 = data1['records']['Earthquake'][0]
        t1 = eq1['EarthquakeInfo']['OriginTime']

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

def get_current_weather(address):
    result = '找不到即時天氣資訊' 
    code = 'YOUR-OWN-KEY'
    try:
        url = [
            f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization={code}',
            f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization={code}'
        ]
        for item in url:
            req = requests.get(item) 
            data = req.json()   
            station = data['records']['Station']  
            for i in station:
                city = i['GeoInfo']['CountyName']
                area = i['GeoInfo']['TownName'] 
                if address in f'{city}{area}': 
                    weather = i['WeatherElement']['Weather'] 
                    temp = i['WeatherElement']['AirTemperature'] 
                    humid = i['WeatherElement']['RelativeHumidity']  
                    result = f'「{address}」目前天氣狀況「{weather}」，溫度 {temp} 度，相對濕度 {humid}%！'
                    break
    except Exception as e:
        print(e) 
    return result 

def get_air_quality(address):
    result = '找不到空氣品質資訊'
    code = 'YOUR-OWN-KEY'
    try:
        url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
        req = requests.get(url)
        data = req.json()    
        records = data['records'] 
        for item in records:
            county = item['county'] 
            sitename = item['sitename'] 
            aqi = int(item['aqi'])
            aqi_status = ['良好', '普通', '對敏感族群不健康', '對所有族群不健康', '非常不健康', '危害']
            msg = aqi_status[aqi // 50]
            if county in address or sitename in address:
                result = f'「{address}」的空氣品質（AQI）：{aqi}，狀態：{msg}。'
                break
    except Exception as e:
        print(e) 
    return result

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

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
custom_config = r'--oem 3 --psm 6 -l chi_sim+chi_tra'

TOKEN = 'YOUR-TOKEN' 
API_KEY = os.environ["API_KEY"]

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents) 

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')): 
                file_path = f"/content/{attachment.filename}"
                await attachment.save(file_path)

                try:
                    img = Image.open(file_path)
                    text = pytesseract.image_to_string(img, config=custom_config)

                    if not text.strip(): 
                        raise ValueError("OCR結果為空")

                    await message.channel.send(f"圖片顯示：\n{text}")

                except ValueError:
                    await message.channel.send("未能識別出圖片中的文字。")

                except Exception as e:
                    if 'contents must not be empty' in str(e):
                        await message.channel.send("未能識別出圖片中的文字。")
                    else:
                        await message.channel.send(f"發生錯誤：{str(e)}")

                finally:
                    os.remove(file_path)

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
            prompt = message.content.strip()
            try:
                response = model.generate_content(prompt)
                if hasattr(response, 'text'):
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

import nest_asyncio
nest_asyncio.apply()

client.run(TOKEN)
