# 設定中文語言包與 Tesseract 路徑
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # Colab的預設路徑
custom_config = r'--oem 3 --psm 6 -l chi_sim+chi_tra'

# 設定 Discord bot token 和 Google Generative AI API 鍵
TOKEN = 'YOUR-TOKEN' # 替換成實際的Disord Bot API
API_KEY = os.environ["API_KEY"]

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True  # 允許bot讀取訊息內容
client = discord.Client(intents=intents) # 傳入intents參數

# 登錄
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# 訊息處理
@client.event
async def on_message(message):
    # 避免無窮回答
    if message.author == client.user:
        return


 # 檢查是否有圖片附件
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # 支援圖片格式
                file_path = f"/content/{attachment.filename}"
                await attachment.save(file_path)

                try:
                    # 開啟圖片並進行OCR轉文字
                    img = Image.open(file_path)
                    text = pytesseract.image_to_string(img, config=custom_config)

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
                    
    # 沒有圖片附件
    else:
        address = message.content.split(maxsplit=1)[1] if len(message.content.split()) > 1 else ""

        # 根據指令前綴字執行不同的功能
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
            # 開始AI聊天
            prompt = message.content.strip()
            try:
                response = model.generate_content(prompt)
                if hasattr(response, 'text'):  # 檢查是否有 text 屬性
                    await message.channel.send(response.text)
                else:
                    await message.channel.send("無法獲取內容。")
            except Exception as e:
                await message.channel.send(f"出錯了: {e}")

    #發送指定，說明機器人功能
    await message.channel.send("--------------------\n")   
    await message.channel.send("指令說明：\n"
                               "(圖片)  - 顯示圖片上的文字\n"
                               "&即時天氣 (縣市名稱) - 查詢即時天氣\n"
                               "&氣象預報 (縣市名稱) - 查詢氣象預報\n"
                               "&空氣品質 (縣市名稱) - 查詢空氣品質\n"
                               "&地震 - 查詢最新地震資訊\n"
                               "(輸入聊天內容) - 陪你聊天"
                               )   


# 允許執行異步任務
import nest_asyncio
nest_asyncio.apply()

#開始執行
client.run(TOKEN)
