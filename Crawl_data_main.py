from bs4 import BeautifulSoup
import requests
import json
import re
import pandas as pd
from tqdm import tqdm


def write_json(data, filename):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def Extend_json(data_new, fileJson):
    with open(fileJson, encoding='utf-8') as f:
        temp_data = json.load(f)
        temp_data.append(data_new)
        write_json(temp_data, fileJson)
        print("Save Done")


url = 'https://vietnamnet.vn/vn/kinh-doanh/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/95.0.148 Chrome/89.0.4389.148 Safari/537.36"}

response = requests.get(url, headers=headers)  # trích html

soup = BeautifulSoup(response.content, "html.parser")  # gọn html
titles = soup.findAll('h3', class_='m-t-5')
links = [link.find('a').attrs["href"] for link in titles]
#
i = 0
dict_data = {}
list_Category = []
list_titles = []
list_content = []

for link in tqdm(links):
    dict_save = {}
    news = requests.get('https://vietnamnet.vn' + link, headers=headers)
    soup = BeautifulSoup(news.content, "html.parser")
    mydivs = soup.find_all("div", {"class": "top-cate-head-subcate-child"})
    Category = [link.find('a').attrs["title"] for link in mydivs]
    list_Category.append(Category)
    titles = soup.find("h1", class_="title f-22 c-3e")
    list_titles.append(titles.text)
    dict_save["Category"] = str(Category).strip('[]')
    dict_save["Title"] = titles.text
    body = soup.find("div", id="ArticleContent")
    content = ""
    try:
        content = body.findChildren("p", recursive=False)[0].text + body.findChildren("p", recursive=False)[1].text
    except:
        content = ""
    list_content.append(content)
    dict_save["Content"] = content
    Extend_json(dict_save, "data_crawl_web.json")

dict_data['Category'] = list_Category
dict_data['titles'] = list_titles
dict_data['content'] = list_content

dataFrame = pd.DataFrame(dict_data)
dataFrame.to_excel(r'dataWeb2.xlsx')

dataFrame = pd.read_json("data_crawl_web.json")
dataFrame.info()
print(dataFrame.head())
