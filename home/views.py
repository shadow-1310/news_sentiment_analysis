from django.shortcuts import render, HttpResponse
from datetime import date, timedelta
from transformers import pipeline
import re
import json
import requests, pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

def test(request):
    return render(request, 'test.html')


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


def fetch_article(keyword, source, api_key):
    from_date = date.today()-timedelta(days=30)
    if source == 'NewsAPI':
        base = 'https://newsapi.org/v2/'
        url = base + 'everything?q={}&searchIn=title,description&from={}&sortBy=publishedAt&apiKey={}'.format(keyword,from_date,api_key)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout = 30)
        df = pd.DataFrame(response.json()['articles'])
        df[['date', 'time']] = df['publishedAt'].apply(parse_datetime)
        df['publisher'] = df['source'].apply(lambda x: x['name'])
        df.drop(columns = ['source', 'content', 'publishedAt'], inplace = True)
        df['description'] = df['description'].apply(remove_html_tags)
        df[['sentiment', 'confidence']] = df['description'].apply(use_vader)
    
    return df


def make_article_db(request):
    API_KEY = request.POST.get('api_key', 'default')
    KEYWORD = request.POST.get('keyword', 'default')
    SOURCE = request.POST.get('source', 'default')
    result = fetch_article(KEYWORD, SOURCE, API_KEY)
    result.to_csv("{}.csv".format(KEYWORD.replace(' ', '')))
    json_records = result.reset_index().to_json(orient ='records')
    arr = []
    arr = json.loads(json_records)
    contextt = {'d': arr}
    return  render(request,'show-sentiment.html',contextt)
    # return HttpResponse(result.to_html())

def index(request):
    return render(request, 'index.html')

