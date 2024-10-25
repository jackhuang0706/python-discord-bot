!pip install -q -U google-generativeai #使用AI服務(Google機器人)
!pip install discord
!pip install nest_asyncio #允許在異步編程環境中嵌套異步事件循環
!pip install pytesseract pillow discord 
!apt-get install tesseract-ocr 
!apt-get install tesseract-ocr-chi-sim tesseract-ocr-chi-tra  # 安裝中文語言包

import requests #取得天氣
import discord
import os #系統變數
from PIL import Image
import pytesseract
import asyncio #處理異步操作
import nest_asyncio #允許嵌套異步事件循環
import google.generativeai as genai #引入AI互動
%env API_KEY=YOUR_API_KEY #更換為實際的Google AI API
