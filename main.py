# pip install requests
# pip install bs4
# pip install html5lib

import requests
import schedule
import time
import  json

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
dict_list = []


def get_data():
    trading_data = soup.find(id='live-trading')
    rows = trading_data.find_all('tr')
    global dict_list
    for row in rows:
        my_dict = {}
        data = row.find_all('td')
        anchor = row.find_all('a')
        for a in range(len(anchor)):
            for i in range(len(data)):
                if i == 1:
                    my_dict['companyName'] = (anchor[0]['title']).split('(')[1].replace(')', '')
                    my_dict['symbol'] = anchor[0].get_text()
                    my_dict['LTP'] = data[i].get_text()
                if i == 2:
                    my_dict['change'] = data[i].get_text()
        dict_list.append(my_dict)
    dict_list.pop(0)


get_data()

# json_object = json.dumps(dictList, indent=4)
# print(json_object)


app = FastAPI()


@app.get('/')
def index():
    return dict_list


# # schedule.every(5).seconds.do(get_data)
# schedule.every().hour.do(get_data)
# schedule.every().day.at("11:00").do(get_data)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)
