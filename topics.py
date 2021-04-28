import requests
from bs4 import BeautifulSoup
import mysql.connector
import time

def replace_special_characters(msg):
    replaced = msg
    replaced = replaced.replace('\'', '')
    replaced = replaced.replace(',', '')
    return replaced

r = requests.get("https://www.tripadvisor.com/ShowForum-g293920-i5037-Phuket.html")
r.encoding = "utf-8"

html_page = BeautifulSoup(r.text, "html.parser")

# Find No. Of Topics
selector = 'span.pgCount'
topic_count = html_page.select(selector)
topic_count = topic_count[0].text.split()[2]

# Find No. Of Pages
selector = 'a.paging.taLnk'
page_count = html_page.select(selector)
page_count = page_count[len(page_count)-1].text

#page_count = 2780;
for i in range(2780, int(page_count)+1):
    
    if(i == 1) :
        url = "https://www.tripadvisor.com/ShowForum-g293920-i5037-Phuket.html"
    else :
        url = "https://www.tripadvisor.com/ShowForum-g293920-i5037-o"+ str((i-1) * 20) +"-Phuket.html"
    
    r = requests.get(url)
    r.encoding = "utf-8"

    html_page = BeautifulSoup(r.text, "html.parser")

    selector = 'table.topics'
    tables = html_page.select(selector)

    selector = 'tr'
    rows = tables[0].select(selector)

    for j in range(1, int(len(rows))):        
        forum = ''
        topic_title = ''
        topic_url = ''
        creator = ''
        creator_url = ''
        replies = ''
        lastposted = ''
        lastPoster = ''
        lastPoster_url = ''

        selector = 'td'
        columns = rows[int(j)].select(selector)
        if len(columns) == 5:
            forum = columns[1].text.strip()

            selector = 'a'
            topic = columns[2].select(selector)

            topic_title = replace_special_characters(topic[0].text.strip())
            topic_url = topic[0]["href"].strip()
            creator = replace_special_characters(topic[1].text.strip())
            creator_url = topic[1]["href"].strip()

            replies = replace_special_characters(columns[3].text.strip())

            try:
                selector = 'a'
                lastpost = columns[4].select(selector)
                lastposted = lastpost[0].text.strip()
                lastPoster = replace_special_characters(lastpost[1].text.strip())
                lastPoster_url = lastpost[1]["href"].strip()
            except:
                try:
                    lastposted = columns[4].text.strip().split("\n\n")[0]
                    selector = 'a'
                    lastpost = columns[4].select(selector)
                    lastPoster = replace_special_characters(lastpost[0].text.strip())
                    lastPoster_url = lastpost[0]["href"].strip()
                except:
                    print("except")

            conn = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='forums')
            cursor = conn.cursor()
            comm = "INSERT INTO topics(forum, title, creator, replies, lastposter, lastposted, url, creator_url, lastPoster_url, page) VALUES('"+ forum +"', '"+ topic_title +"', '"+ creator +"', "+ replies +", '"+ lastPoster +"', '"+ lastposted +"', '"+ topic_url +"', '"+ creator_url +"', '"+ lastPoster_url +"', "+ str(i) +")"
            cursor.execute(comm)
            conn.commit()
            conn.close()

    print("page: "+str(i))
    time.sleep(10)
