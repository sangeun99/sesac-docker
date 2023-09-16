import requests
from bs4 import BeautifulSoup

def get_naver_sports_news() :
    data = requests.get('https://sports.news.naver.com/index')
    soup = BeautifulSoup(data.text, 'html.parser')

    naver_news_url = 'https://sports.news.naver.com/'

    news = soup.select('.today_list > li')

    for n in news:
        a_tag = n.select_one('a')
        print(naver_news_url + a_tag['href'])
        title = n.select_one('.title')
        print(title.text)

def get_naver_land(type):
    if type == 'headline' :
        data = requests.get('https://land.naver.com/news/')
        soup = BeautifulSoup(data.text, 'html.parser')

        naver_land_url = 'https://land.naver.com/'
        headline = soup.select('.section_group')[0]
        headlines = headline.select('li')
        for h in headlines:
            a_tag = h.select('a')[1]
            print(h.select('a')[0].text + h.select('a')[1].text.strip())
            print(naver_land_url + a_tag['href'])
            detail = requests.get(naver_land_url + a_tag['href'])
            detail_soup = BeautifulSoup(detail.text, 'html.parser')
            print(detail_soup.select_one('#articleBody').text)

    if type == 'report' : 
        report = soup.select('.section_group')[3]
        reports = report.select('li')
        for r in reports:
            print(r.select_one('a').text)

if __name__ == "__main__" :
    get_naver_sports_news()
    # get_naver_land('headline')
    # get_naver_land('report')