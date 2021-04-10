#DON'T FORGET TO USE PYTHON3 TO EXPORT!!

# encoding=utf8

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import datetime
import sys

baseurl = 'https://www.tagesschau.de/'
headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36'
}

r = requests.get(baseurl)
soup = BeautifulSoup(r.text, 'html.parser')

articlelist = soup.body.find_all('div', attrs={'class', 'teaser'})

filter = "https://www.tagesschau.de/"
articlelinks = []

for item in articlelist:
    articlelist = item.a.attrs['href']
    articlelinks.append(articlelist)

filtered = [x for x in articlelinks if x.startswith(filter)]


#testlink = 'https://www.tagesschau.de/inland/corona-bund-103.html'
information_list = []
for link in filtered:

    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    article = soup.find('article', attrs={'container'})

    title = soup.find_all('span', class_='meldungskopf__headline--text')
    titles = [c.text.strip().replace(u'\xa0', u' ') for c in title]

    subtitle = soup.find_all('span', class_='meldungskopf__topline')
    subtitles = [c.text.strip().replace(u'\xa0', u' ') for c in subtitle]

    date = soup.find_all('p', class_='meldungskopf__datetime')
    dates = [c.text.strip().replace(u'\xa0', u' ') for c in date]

    try:
        author = soup.find_all('span', class_='id-card__name')
        authors = [c.text.strip().replace(u'\xa0', u' ') for c in author]

    except:
        authors = ' '

    keyword = soup.find_all(class_='tag-btn tag-btn--emotional')
    keywords = [c.text.strip().replace(u'\xa0', u' ') for c in keyword]

    paragraph = soup.find_all(class_='textabsatz')
    paragraphs = [c.text.strip().replace(u'\xa0', u' ') for c in paragraph]


    information = {
        'title': titles,
        'subtitle': subtitles,
        'date': dates,
        'author': authors,
        'paragraphs': paragraphs,
        'keywords': keywords,
    }

    information_list.append(information)

    print(paragraphs)


df = pd.DataFrame(information_list)
#names Times

current_date = datetime.datetime.now()
filename =  str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day) + '-' + str(current_date.hour) + ':' + str(current_date.minute)

df.to_csv  (r'/Users/manuel/Documents/Coding/Python/news-scraper-DE /mainscrapus_v2.py/exports/' + str(filename + '.csv'))

print(" [x] done!")
