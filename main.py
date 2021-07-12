# pip install requests
# pip install bs4
# pip install html5lib

import requests
import schedule
import time

from bs4 import BeautifulSoup
from fastapi import FastAPI
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://merolagani.com/LatestMarket.aspx'

# Step 1: Get the HTML
r = requests.get(url, headers=headers)
htmlContent = r.content

# Step 2: Parse the HTML
soup = BeautifulSoup(htmlContent, 'html.parser')
# print(soup.prettify())

# Step 3: HTML tree traversal
tradingData = soup.find(id='live-trading')
rows = tradingData.find_all('tr')
dictList = []
for row in rows:
    myDict = {}
    data = row.find_all('td')
    anchor = row.find_all('a')
    for a in anchor:
        for i in range(len(data)):
            if i == 1 and a.get_text()!='':
                myDict[a.get_text()] = data[i].get_text()
    dictList.append(myDict)
dictList.pop(0)

# print(dictList)
# json_object = json.dumps(dictList, indent=4)
# print(json_object)

app = FastAPI()


@app.get('/')
def index():
    return dictList


schedule.every(5).seconds.do(index)
schedule.every().hour.do(index)
schedule.every().day.at("11:00").do(index)

while 1:
    schedule.run_pending()
    time.sleep(1)
