import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
import time

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

conn = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='forums')

# id = 1 (5 replies)
# id = 4 (26 replies)
comm = "SELECT id, url FROM topic WHERE id>=10001 AND id<=12000 AND is_replies=0"
cursor = conn.cursor()
cursor.execute(comm)
data = cursor.fetchall()
conn.commit()
conn.close()

for r in data:
    id = str(r[0])
    url = "https://www.tripadvisor.com" + r[1]
    # print(url)

    r = requests.get(url)
    r.encoding = "utf-8"
    html_page = BeautifulSoup(r.text, "html.parser")

    # Find No. Of Pages
    selector = 'a.paging.taLnk'
    pages = html_page.select(selector)
    pages = int(len(pages)/2)

    url_list = list()
    url_list.append(id+","+url)

    if pages >= 1:
        for i in range(1, pages+1):
            url_split = url.split("-")
            url_page = url_split[0]+"-"+url_split[1]+"-"+url_split[2]+"-"+url_split[3]+"-o"+str(i*10)+"-"+url_split[4]+"-"+url_split[5]
            url_list.append(id+","+url_page)

    for url in url_list:
        url = url.split(",")
        id = url[0]
        url = url[1]
        r = requests.get(url)
        r.encoding = "utf-8"
        html_page = BeautifulSoup(r.text, "html.parser")

        selector = 'div.post'
        postContent = html_page.select(selector)

        for i in range(0, int(len(postContent))):
            if i == 0:
                selector = 'span.topTitleText'
                topicTitle = postContent[i].select(selector)
                topicTitleText = topicTitle[i].text
                topicTitleText = topicTitleText.strip()
                topicTitleText = topicTitleText.replace("\n", " ")
                topicTitleText = topicTitleText.replace("'", "\\'")
                if id == "9515":
                    topicTitleText = "Restaurants"
                # print(str(i)+". Title: "+topicTitleText)

                selector = 'div.postDate'
                postDate = postContent[i].select(selector)
                postDateText = postDate[0].text
                # print(str(i)+". Title: "+topicTitleText+ ", Post Date: "+postDateText+"\n")

                selector = 'div.postBody'
                postBody = postContent[i].select(selector)
                postBodyText = postBody[0].text
                postBodyText = postBodyText.strip()
                postBodyText = postBodyText.replace("\n", " ")
                postBodyText = postBodyText.replace("'", "\\'")
                # print(str(i)+". Title: "+topicTitleText+ ", Post Date: "+postDateText+"\n"+postBodyText+"\n\n")

                conn = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='forums')
                cursor = conn.cursor()
                comm = "UPDATE topics SET title='"+topicTitleText+"', message='"+postBodyText+"', is_replies=1 WHERE id="+str(id)
                cursor.execute(comm)
                conn.commit()
                conn.close()
            else:
                selector = 'span.postNum'
                postNumber = postContent[i].select(selector)
                postNumberText = postNumber[0].text
                postNumberText = postNumberText.strip()
                postNumberText = postNumberText.replace("\n", " ")
                postNumberText = postNumberText.replace("'", "\\'")
                # print(str(i)+". postNumber: "+postNumberText)

                selector = 'span.titleText'
                title = postContent[i].select(selector)
                titleText = title[0].text
                titleText = titleText.strip()
                titleText = titleText.replace("\n", " ")
                titleText = titleText.replace("'", "\\'")
                titleText = remove_emojis(titleText)
                if id == "9515" :
                    titleText = "Restaurants"
                # print(str(i)+". title: "+titleText)

                selector = 'div.postBody'
                postBody = postContent[i].select(selector)
                postBodyText = postBody[0].text
                if id == "3632" and postNumberText=="9.":
                    postBodyText ="we forgot stay away from parasails or u cud end up in a tree as many do,  stay away from \timeshare scammers hey are everywhere,  theres a couple of white skinned blokes doing the rounds at the beach,  they make an excuse to chat to you,then out come the cards for the most  expensive night be you will ever have.dont give them   any money/card etc., or your hotel,your phone number.  just tell em no & walk away,if they persist in following you just look  around calling police,police."
                postBodyText = postBodyText.strip()
                postBodyText = postBodyText.replace("\n", " ")
                postBodyText = postBodyText.replace("'", "\\'")
                postBodyText = remove_emojis(postBodyText)
                # print(str(i)+". Title: "+postTitleText+ ", Post Date: "+postDateText+"\n"+postBodyText+"\n\n")

                selector = 'div.postDate'
                postDate = postContent[i].select(selector)
                postDateText = postDate[0].text
                # print(str(i)+". Title: "+postTitleText+ ", Post Date: "+postDateText+"\n")

                selector = 'div.username'
                user = postContent[i].select(selector)
                if len(user) > 0 :
                    userText = user[0].text
                    userText = userText.strip()
                    userText = userText.replace("\n", " ")
                    userText = userText.replace("'", "\\'")
                    userText = remove_emojis(userText)
                    # print(str(i)+". username: "+userText)

                    selector = 'a'
                    user = user[0].select(selector)
                    userUrl = user[0]["href"].strip()
                    # print(str(i)+". username: "+usernameUrl)
                else :
                    userText=''
                    userUrl=''

                conn = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='forums')
                cursor = conn.cursor()
                comm = "INSERT INTO replies(topic_id, topic_num, topic_title, topic_message, topic_posted, creator, creator_url) VALUES("+id+", "+postNumberText+", '"+titleText+"', '"+postBodyText+"', '"+postDateText+"', '"+userText+"', '"+userUrl+"')"
                cursor.execute(comm)
                conn.commit()
                conn.close()

    print(id)
    time.sleep(10)

