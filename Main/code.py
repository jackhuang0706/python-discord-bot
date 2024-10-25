# 設定中文語言包與 Tesseract 路徑（Colab 預設安裝於 /usr/bin/tesseract）
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
custom_config = r'--oem 3 --psm 6 -l chi_sim+chi_tra'

# 設定 Discord bot token 和 Google Generative AI API 鍵
TOKEN = 'MTI4Mzk2MDQzMjEyMTM0ODE4OQ.Gn5GJU.vpjce_nu0MoNM9bPmM8Nv6pbfJfjM3BlHbyX2Y'
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
