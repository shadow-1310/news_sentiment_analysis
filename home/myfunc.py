import requests
import random
from datetime import datetime
import re
from bs4 import BeautifulSoup
from time import sleep

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
    p_list = content_box.findAll('p')[:-7] # list slicing is to remomve "also read" "also watch" paragraphs
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


def fetch_gnews(url):
    global compare_date
    global updated_date
    global problems
    global output
    root = "https://www.google.com/"
    scrappable = ['ANI News', 'Deccan Herald', 'The Hindu', 'Northeast Now', 'Outlook India', 'Republic World', 'The Sentinel Assam', 'Times Now']
    headers={'User-Agent': 'Mozilla/5.0'}
    n= random.randint(1,2)
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
            else:
                continue
               
        else:
            title = None
            link = None
            p_date = None
            p_time = None
            desc = None

        every_page = {'headline': title,
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