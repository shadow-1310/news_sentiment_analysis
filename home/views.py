from django.shortcuts import render, HttpResponse
from datetime import date, timedelta
from transformers import pipeline
import nltk
import re
import json
import requests, pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine
from home.models import article_gnews
import random
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
import warnings
import spacy
from collections import Counter
import plotly.express as px
import plotly


warnings.filterwarnings("ignore")

def extract_summary(text):
    global keyword
    result = []
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        if keyword in sentence:
            result.append(sentence)
        else:
            continue
    return "".join(result)


def scrap_ANI(url):
    article = ""
    headers={'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    publish_datetime = soup.find('span', attrs={'class': 'time-red'}).get_text().strip().split()
    publish_date = " ".join(publish_datetime[:3])
    date_format = "%b %d, %Y"
    date_time = datetime.strptime(publish_date, date_format)
    p_date = date_time.date()
    
    publish_time = publish_datetime[-1]
    time_format = "%H:%M"
    p_time = datetime.strptime(publish_time, time_format).time()
    
    content_box = soup.find('div', attrs={"class":"content count-br"})
    p_list = content_box.findAll('p')[:]
    for item in p_list:
        article += item.get_text().strip()
    return p_date, p_time, article


def scrap_deccan_herald(url):
    article = ""
    headers={'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    publish_box = soup.find('div', attrs={'class': 'article-author__time'})
    publish_datetime = publish_box.find('ul', attrs={'class': 'crud-items'})
    publish_datetime = publish_datetime.findAll('li')[0].get_text().strip().split()
    publish_date = " ".join(publish_datetime[:3]).strip(',')
    date_format = "%b %d %Y"
    date_time = datetime.strptime(publish_date, date_format)
    p_date = date_time.date()
    
    publish_time = publish_datetime[-2]
    time_format = "%H:%M"
    p_time = datetime.strptime(publish_time, time_format).time()
    
    content_box = soup.find('div', attrs={"class":"content"})
    p_list = content_box.findAll('p')[:]
    for item in p_list:
        article += item.get_text().strip()
    return p_date, p_time, article


def scrap_hindu(url):
    article = ""
    headers={'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    publish_datetime = soup.find('p', attrs={'class': 'publish-time'}).get_text()
    publish_datetime = publish_datetime.split(" | ")[0].strip().split()
    publish_date = " ".join(publish_datetime[:3])
    date_format = "%B %d, %Y"
    date_time = datetime.strptime(publish_date, date_format)
    p_date = date_time.date()
    
    publish_time = " ".join(publish_datetime[3:])
    time_format = "%I:%M %p"
    p_time = datetime.strptime(publish_time, time_format).time()
    
    content_box = soup.find('div',attrs={"class":"articlebodycontent col-xl-9 col-lg-12 col-md-12 col-sm-12 col-12"})
    p_list = content_box.findAll('p')[:-3]
    for p in p_list:
        article += p.get_text()
    return p_date, p_time, article


def scrap_NEnow(url):
    article = ""
    headers={'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    publish_datetime = soup.find('time', attrs={'class': 'entry-date published'}).get_text().strip().split()
    publish_date = " ".join(publish_datetime[:3])
    date_format = "%B %d, %Y"
    date_time = datetime.strptime(publish_date, date_format)
    p_date = date_time.date()
    
    publish_time = " ".join(publish_datetime[3:])
    time_format = "%I:%M %p"
    p_time = datetime.strptime(publish_time, time_format).time()
    
    content_box = soup.find('div', attrs={"class":"main-content"})
    p_list = content_box.findAll('p')[:-1]
    for item in p_list:
        article += item.get_text().strip()
    return p_date, p_time, article


def scrap_outlook(url):
    article = ""
    headers={'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    time_div = soup.find('div', attrs={'class': 'desc'})
    publish_datetime = time_div.find('p').get_text().strip("Updated: ").split()
    publish_date = " ".join(publish_datetime[0:3])
    date_format = "%d %b %Y"
    date_time = datetime.strptime(publish_date, date_format)
    p_date = date_time.date()
    
    publish_time = " ".join(publish_datetime[3:])
    time_format = "%I:%M %p"
    p_time = datetime.strptime(publish_time, time_format).time()
    
    content_box = soup.find('div',attrs={"id":"articleBody"})
    p_list = content_box.findAll('p')
    for p in p_list:
        article += p.get_text().strip()
    return p_date, p_time, article


def scrap_republic(url):
    article = ""
    headers={'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    publish_datetime = soup.find('span', attrs={'class': 'time-elapsed'}).get_text().strip("Last Updated: ").split()
    publish_date = " ".join(publish_datetime[:3])
    pattern = r"(\d+)(st|nd|rd|th)"
    replacement = r"\1"
    publish_date = re.sub(pattern, replacement, publish_date)
    date_format = "%d %B, %Y"
    date_time = datetime.strptime(publish_date, date_format)
    p_date = date_time.date()

    publish_time = publish_datetime[-2]
    time_format = "%H:%M"
    p_time = datetime.strptime(publish_time, time_format).time()
    
    content_box = soup.find('div', attrs={"class":"width100 storytext"})
    p_list = content_box.findAll('p')[:]
    for item in p_list:
        article += item.get_text().strip()
    return p_date, p_time, article


def scrap_sentinel_assam(url):
    article = ""
    headers={'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    publish_datetime = soup.find('span', attrs={'class': 'convert-to-localtime'}).get_text().split()
    publish_date = " ".join(publish_datetime[:3])
    date_format = "%d %b %Y"
    date_time = datetime.strptime(publish_date, date_format)
    p_date = date_time.date()
    
    publish_time = " ".join(publish_datetime[3:5])
    time_format = "%I:%M %p"
    p_time = datetime.strptime(publish_time, time_format).time()
    
    content_box = soup.find('div', attrs={"class":"content details-content-story"})
    p_list = content_box.findAll('p')[:-3] # list slicing is to remomve "also read" "also watch" paragraphs
    for item in p_list:
        article += item.get_text().strip()
    return p_date, p_time, article


def scrap_timesnow(url):
    article = ""
    headers={'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    publish_datetime = soup.find('p', attrs={'class': '_3zhGX'}).get_text()
    publish_datetime = publish_datetime.replace("Updated ", "")
    publish_date = publish_datetime.split(" | ")[0]
    date_format = "%b %d, %Y"
    date_time = datetime.strptime(publish_date, date_format)
    p_date = date_time.date()
    
    publish_time = publish_datetime.split(" | ")[1].strip(" IST")
    time_format = "%I:%M %p"
    p_time = datetime.strptime(publish_time, time_format).time()
    
    body_box = soup.findAll('div', attrs={'class': '_18840'})
    for item in body_box:
        article += item.get_text().strip()
    return p_date, p_time, article

global compare_date
compare_date = date.today()

def fetch_gnews(url):
    root = "https://www.google.com/"
    global method
    global compare_date
    global keyword
    scrappable = ['ANI News', 'Deccan Herald', 'The Hindu', 'Northeast Now', 'Outlook India', 'Republic World', 'The Sentinel Assam', 'Times Now']
    headers={'User-Agent': 'Mozilla/5.0'}
    # n= random.randint(1,2)
    n = random.uniform(0,0.5)
    sleep(n)
    webpage = requests.get(url, headers).text
    soup = BeautifulSoup(webpage, 'lxml')
    
    next_page = soup.find('a', attrs={'aria-label':'Next page'})
    next_page = (next_page['href'])
    next_page_link = root + next_page
    print(next_page_link)
    
    if len(soup.find_all('div', attrs={'class': 'Gx5Zad fP1Qef xpd EtOod pkphOe'})) == 0:
        flag = False
    else:
        flag = True

    for item in soup.find_all('div', attrs={'class': 'Gx5Zad fP1Qef xpd EtOod pkphOe'}):
        problem_source = None
        problem_link = None
        try:
            source = (item.find('div', attrs={'class': 'BNeawe UPmit AP7Wnd lRVwie'}).get_text())
        except:
            source = None
        if source in scrappable:
            title = (item.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).get_text())
            title = title.split("|")[0]
            
            raw_link = (item.find('a', href=True)['href'])
            link = (raw_link.split("/url?q=")[1]).split('&sa=U&')[0]
            
            if source == 'ANI News':
                try:
                    p_date, p_time, desc = scrap_ANI(link)
                    compare_date = p_date
                except:
                    problem_source = source
                    problem_link = link
            
            elif source == 'Deccan Herald':
                try:
                    p_date, p_time, desc = scrap_deccan_herald(link) 
                    compare_date = p_date
                except:
                    problem_source = source
                    problem_link = link
                    
            elif source == 'The Hindu':
                try:
                    p_date, p_time, desc = scrap_hindu(link)
                    compare_date = p_date
                except:
                    problem_source = source
                    problem_link = link
                    
            elif source == 'Northeast Now':
                try:
                    p_date, p_time, desc = scrap_NEnow(link)
                    compare_date = p_date
                except:
                    problem_source = source
                    problem_link = link
                    
            elif source == 'Outlook India':
                try:
                    p_date, p_time, desc = scrap_outlook(link)
                    compare_date = p_date
                except:
                    problem_source = source
                    problem_link = link
                    
            elif source == 'Republic World':
                try:
                    p_date, p_time, desc = scrap_republic(link)
                    compare_date = p_date
                except:
                    problem_source = source
                    problem_link = link
                    
            elif source == 'The Sentinel Assam':
                try:
                    p_date, p_time, desc = scrap_sentinel_assam(link)
                    compare_date = p_date
                except:
                    problem_source = source
                    problem_link = link
                    
            elif source == 'Times Now':
                try:
                    p_date, p_time, desc = scrap_timesnow(link)
                    compare_date = p_date
                except:
                    problem_source = source
                    problem_link = link
            
            every_page = {'keyword': keyword,
                      'method' : method,
                      'headline': title,
                      'publish_date': p_date,
                         'publish_time': p_time,
                      'source': source,
                         'article':desc,
                         'url': link}
            output.append(every_page)
            
            recheck = {'problem_source': problem_source,
                  'problem_link': problem_link}
            
            problems.append(recheck)                       
                
    if compare_date < updated_date:
        flag = False

    if flag:
        fetch_gnews(next_page_link)
    else:
        print("End Of result")


def test(request):
    # df = pd.read_csv("hb.csv")
    # engine = create_engine("sqlite:///db.sqlite3")
    # df.to_sql(article_gnews._meta.db_table,
    #           if_exists="replace", con=engine, index=False)

    # Build the raw SQL query
    keyword = "Himanta Biswa"
    query = "SELECT id, MAX(publish_date) AS p_date FROM home_article_gnews GROUP BY keyword HAVING keyword = %s"
    params = ['{}'.format(keyword)]

    # Execute the raw SQL query using the `Raw` queryset method
    max_date = article_gnews.objects.raw(query, params)
    print("Hello this is the latest date for mama", max_date[0].p_date)
    # article_gnews.objects.all().delete()
    return HttpResponse("success bro")


def parse_datetime(text):
    try:
        date = text.split("T")[0]
        time = text.split("T")[1][:-1]
    except:
        date = 'Not Available'
        time = 'Not Available'
    return pd.Series([date, time])


def remove_html_tags(text):
    pattern = re.compile("<.*?>|\r\n|\r")
    return pattern.sub("", text).replace("\xa0", "")


def use_vader(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    score_comp = score['compound']
    if score_comp > 0:
        verdict = 'POSITIVE'
    elif score_comp < 0:
        verdict = 'NEGATIVE'
    else:
        verdict = 'NEUTRAL'
        
    return pd.Series([verdict, score_comp])


def fetch_article(keyword, method, api_key):
    from_date = date.today()-timedelta(days=30)
    if method == 'NewsAPI':
        base = 'https://newsapi.org/v2/'
        url = base + 'everything?q={}&searchIn=title,description&from={}&sortBy=publishedAt&apiKey={}'.format(keyword,from_date,api_key)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout = 30)
        df = pd.DataFrame(response.json()['articles'])
        df[['date', 'time']] = df['publishedAt'].apply(parse_datetime)
        df['source'] = df['source'].apply(lambda x: x['name'])
        df.rename(columns={'title': 'headline', 'description':'summary', 'content':'article', 'date':'publish_date','time':'publish_time'}, inplace=True)
        df.drop(columns = ['publishedAt', 'urlToImage', 'author'], inplace = True)
        df[['sentiment', 'confidence']] = df['summary'].apply(use_vader)
        df['keyword'] = keyword
        df['method'] = method
        df = df.reset_index(drop=True)
        df.index.name = 'id'

    elif method == 'gnews':
        global compare_date
        compare_date = date.today()
        global updated_date # write raw SQL query to fetch the latest date from database
        try:
            query = "SELECT id, MAX(publish_date) AS p_date FROM home_article_gnews GROUP BY keyword HAVING keyword = %s"
            params = ['{}'.format(keyword)]
            max_date = article_gnews.objects.raw(query, params)
            updated_date = max_date[0].p_date
        except:
            updated_date = date.today() - timedelta(days=60)
        first = "https://www.google.com/search?q={}&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwjAvsKDyOXtAhXBhOAKHXWdDgcQpwUIKQ&biw=1604&bih=760&dpr=1.2".format(keyword)
        global output
        global problems
        output = []
        problems = []
        fetch_gnews(first)
        df = pd.DataFrame(output)
        df.dropna(subset=['article'],inplace=True)
        df = df[df['article'] != '']
        df['summary'] = df['article'].apply(extract_summary)
        df[['sentiment', 'confidence']] = df['summary'].apply(use_vader)
        df = df.reset_index(drop=True)
        df.index.name = 'id'
    return df

def unix_to_user(timestamp):
    date_time = datetime.fromtimestamp(int(timestamp)/1000)
    return date_time.strftime("%d-%m-%Y")

def make_article_db(request):
    global method
    global keyword
    global results
    API_KEY = request.POST.get('api_key', 'default')
    keyword = request.POST.get('keyword', 'default').title()
    method = request.POST.get('method', 'default')
    
    result = fetch_article(keyword, method, API_KEY)
    engine = create_engine("sqlite:///db.sqlite3")
    result.to_sql(article_gnews._meta.db_table,
              if_exists="replace", con=engine, index=False)
    # return HttpResponse("writing finished to database")
    fetch_query = '''SELECT publish_date, publish_time, source, headline, summary, sentiment, article, confidence, method, keyword FROM home_article_gnews WHERE keyword = "{}" AND method="{}"'''.format(keyword.replace('"', '""'), method.replace('"', '""'))
    # params = ['{}'.format(keyword)]
    results = pd.read_sql(fetch_query, engine)
    # results['publish_date'] = results['publish_date'].apply(unix_to_user)
    # result.to_csv("{}.csv".format(keyword.replace(' ', '')))
    json_records = results.reset_index().to_json(orient ='records', date_format='iso')
    arr = []
    arr = json.loads(json_records)
    contextt = {'d': arr}
    return  render(request,'show-sentiment.html',contextt)
    # return HttpResponse(result.to_html())

def index(request):
    return render(request, 'index.html')

def ner_counter(text):
    nlp = spacy.load("en_core_web_lg")
    text1 = nlp(text)
    persons = [x.text for x in text1.ents if x.label_ == "PERSON"]
    locations = [x.text for x in text1.ents if x.label_ == "GPE"]
    count_person = Counter(persons)
    count_gpe= Counter(locations)

    df_person = pd.DataFrame.from_dict(count_person, orient='index').reset_index()
    df_person.rename(columns={'index': 'person', 0: 'count'}, inplace=True)
    df_person = df_person.sort_values(by=['count'], ascending =False).reset_index(drop=True).head(10)

    df_gpe = pd.DataFrame.from_dict(count_gpe, orient='index').reset_index()
    df_gpe.rename(columns={'index': 'location', 0: 'count'}, inplace=True)
    df_gpe = df_gpe.sort_values(by=['count'], ascending =False).reset_index(drop=True).head(10)

    return df_person, df_gpe


def analyze(request):
    corpus = " ".join(results['article'])
    person, location = ner_counter(corpus)

    fig_person = px.bar(person, x='count', y='person', orientation='h', title="Count for mention of Persons", template="plotly_white",color_discrete_sequence=px.colors.qualitative.Dark2,)
    graph_person = plotly.offline.plot(fig_person, auto_open = False, output_type="div")
    
    fig_location = px.bar(location, x='count', y='location', orientation='h', title="Count for mention of locations", template="plotly_white",color_discrete_sequence=px.colors.qualitative.Dark2,)
    graph_location = plotly.offline.plot(fig_location, auto_open = False, output_type="div")

    params = {
        'graph_person': graph_person,
        'graph_location': graph_location,
    }
    return render(request, 'analysis.html', params)

