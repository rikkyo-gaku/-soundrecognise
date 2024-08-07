import speech_recognition as sr
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime

def whether():
    #urlの固定
    url = 'https://weather.yahoo.co.jp/weather/jp/14/4610.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    elems = soup.select("p")
    #今日、明日の天気の取得
    today_whether = soup.select_one('#main > div.forecastCity > table > tr > td > div > p.pict')
    tomorrow_whether = soup.select_one('#main > div.forecastCity > table > tr > td + td > div > p.pict')

    #本日のコメントの取得
    comment = soup.select_one('p.comment')

    #日付の取得
    today = soup.select_one('#main > div.forecastCity > table > tr > td > div > p')
    tomorrow = soup.select_one('#main > div.forecastCity > table > tr > td + td > div > p')

    #\nを削除
    today_whether =  today_whether.text.replace("\n", "")
    tomorrow_whether =tomorrow_whether.text.replace("\n", "")
    comment = comment.text.replace("\n", "")
    today = today.text.replace("\n", "")
    tomorrow = tomorrow.text.replace("\n", "")

    #データの作成
    data = {
       "date" : [today, tomorrow],
        "whether" :[today_whether, tomorrow_whether],
        "comment" : [comment, "NULL"]
    }

    df = pd.DataFrame(data)
    return df




while True:
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16_000) as source:
        print("なにか話してください")
        audio = r.listen(source)
        print("音声を取得しました")
    recognized_text = r.recognize_google(audio, language='ja-JP')
    print(recognized_text)

    if (recognized_text == "ひらけごま"):
        chrome = webdriver.Chrome()
        print("success")
        chrome.get("https://www.google.co.jp")
    elif(recognized_text == "天気"):
        print(whether())
        """
    elif(recognized_text == "アプリの名前"):
        subprocess.Popen(r'C:～')
        """
    elif(recognized_text == "ストップ"):
        break




    '''
    終了するかどうかも入れるwhile true break 

    何とかを開いてといったものもできるようにする(入力されたものを用意しておく必要がない)
    chatgptにコードを書かせる?
    -> chatgpt はapiの取得に費用が掛かる。

    実行中のアプリケーションの場所は取得できるっぽい

    検索が入ってたらwebを開いてその前の言葉を検索するとか？
    '''
