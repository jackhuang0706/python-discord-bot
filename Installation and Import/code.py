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
