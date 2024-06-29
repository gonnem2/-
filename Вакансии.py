import requests
import fake_useragent
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import Table, String, Integer, Column, MetaData

url = "https://hh.ru/search/vacancy?text=&page=2&hhtmFrom=resume_search_result&hhtmFromLabel=vacancy_search_line"
baze = 'https://hh.ru/'

engine = sqlalchemy.create_engine("sqlite:///Vakans.db")
conn = engine.connect()
metadata = MetaData()
metadata.drop_all(engine)

Vakancy = Table(
    'Vakancy', metadata,
    Column('id', Integer(), primary_key=True),
    Column('title', String(200)),
    Column('salary', String(200)),
    Column('experience', String(200)),
    Column('employment_mode', String(200)),
    Column('href', String(200))
)


data = list()
user_agent = fake_useragent.UserAgent()
headers={
        "user-agent":user_agent.random
    }

response_main = requests.get(
    url=url, headers=headers
)

soup_url = BeautifulSoup(response_main.text, 'html.parser')
vakans_url = [i.find_next('a', attrs={'class': 'bloko-link'})['href'] for i in (soup_url.find_all('div', attrs={'data-qa' : 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'}))]

for i in vakans_url:
    res = {
        'title': str,
        'salary': str,
        'vacancy_experience': str,
        'employment_mode': str,
        'href': str




    }
    response = requests.get(url=i, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    res['href'] = i

    res['title'] = soup.find('h1', attrs={'data-qa': 'vacancy-title'}).text
    try:
        res['salary'] = soup.find('span', attrs={'data-qa': 'vacancy-salary-compensation-type-gross'}).text.replace('\xa0', '')
    except AttributeError:
        res['salary'] = None
    res['vacancy_experience'] = soup.find('span', attrs={'data-qa': 'vacancy-experience'}).text
    res['employment_mode'] = soup.find('p', attrs={'data-qa': 'vacancy-view-employment-mode'}).text

    metadata.create_all(engine)

    ins = Vakancy.insert().values(
        title = res['title'],
        salary = res['salary'],
        experience = res['vacancy_experience'],
        employment_mode = res['employment_mode'],
        href = res['href']

    )
    print(ins.compile().params)
    conn.execute(ins)
conn.commit()














