from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os, requests

def lambda_handler(event,context):
    # Headless Chromeを使うための設定を追加
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--v=99")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    # Headless Chromeを起動
    options.binary_location = "./bin/headless-chromium"
    driver = webdriver.Chrome(executable_path="./bin/chromedriver", chrome_options=options)


    # Chromeの検索結果ページにアクセス
    driver.get('https://cas.ecs.kyoto-u.ac.jp/cas/login?service=https%3A%2F%2Fpanda.ecs.kyoto-u.ac.jp%2Fsakai-login-tool%2Fcontainer')

    sleep(1)

    #ログイン
    user_id = driver.find_element_by_name("username")
    user_id.clear()
    
    my_id = os.environ["MY_ID"]
    my_password = os.environ["MY_PASSWORD"]

    user_id.send_keys(my_id)

    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(my_password)

    login = driver.find_element_by_class_name("btn-submit")
    login.click()
    sleep(1)

    #各科目のページに遷移
    base_url = driver.current_url
    
    
    links = {
    "弾性体の力学解析":"2020-110-3200-000",
    "流体力学":"2020-110-3165-000",
    "一般力学":"2020-110-3010-100",
    "基礎有機化学I":"2020-888-N347-014",
    "地球環境学のすすめ":"2020-888-Y201-001",
    "社会基盤デザインＩ":"2020-110-3181-000",
    "工業数学B2":"2020-110-3174-000",
    "確率統計解析及び演習":"2020-110-3003-000",
    "水文学基礎":"2020-110-3030-000",
    "地球工学基礎数理":"2020-110-3005-000",
    }
    
    
    for subject,link_id in links.items():
        unkadai(base_url,subject,link_id,driver)

    # ブラウザを閉じる
    driver.close()
    # Google Chrome Canaryを終了する
    driver.quit()


def unkadai(base_url,subject,link_id,driver):
    driver.get(base_url)
    other_link = driver.find_element_by_xpath("//*[@id='topnav']/li[6]/a")
    other_link.click()
    sleep(1)
    nav = driver.find_element_by_id(link_id)
    nav.click()

    url = driver.find_element_by_xpath("//a[contains(@title,'課題')]").get_attribute("href")
    driver.get(url)

    
    url = driver.find_element_by_xpath("//a[contains(@title,'リセット')]").get_attribute("href")
    driver.get(url)
    sleep(1)
    
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    base = soup.select("tr")

    for k in base:
        status =k.select_one("td:nth-child(3)")
        if status is not None:
            if "未開始" in status.text:
                dt = datetime.today()
                highlightday = k.select_one("td:nth-child(5) > span")
                if highlightday is not None:
                    highlightday = highlightday.text
                    highlightday = datetime.strptime(highlightday,'%Y/%m/%d %H:%M')
                    if highlightday >dt:
                        a =  k.select_one("td:nth-child(2)>h4>a")
                        if a is not None:
                            task = (subject+':'+a.text)
                            line_notify(task)

def line_notify(message):
    line_notify_token = os.environ["LINE_ACCESS_TOKEN"]
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)