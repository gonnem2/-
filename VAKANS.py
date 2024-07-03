import requests
import fake_useragent
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import Table, String, Integer, Column, MetaData


def vakancy(search='', salary = 'false',
            education_level = []
            , experience=[],
            employment = [],
            schedule=[]):

    url ='https://belgorod.hh.ru/search/vacancy?ored_cluster=true&ored_cluster=true&area=113&hht'
    engine = sqlalchemy.create_engine("sqlite:///Vakans.db")
    conn = engine.connect()
    metadata = MetaData()

    Vakancy = Table(
        'Vakancy', metadata,
        Column('id', Integer(), primary_key=True),
        Column('title', String(200)),
        Column('salary', String(200)),
        Column('experience', String(200)),
        Column('employment_mode', String(200)),
        Column('href', String(200))
    )
    metadata.drop_all(engine)

    user_agent = fake_useragent.UserAgent()
    headers = {
            "user-agent": user_agent.random
        }

    response_main = requests.get(
        url=url, headers=headers,
        params={
            'text': search,
            'salary': salary,
            'education': education_level,
            'experience': experience,
            'employment': employment,
            'schedule': schedule

        }
    )
    print(response_main.url)


    soup_url = BeautifulSoup(response_main.text, 'html.parser')
    vakans_url = [i.find_next('a', attrs={'class': 'bloko-link'})['href'] for i in (soup_url.find_all('div', attrs={'class' : 'vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS'}))]
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
        try:
            res['title'] = soup.find('h1', attrs={'data-qa': 'vacancy-title'}).text
        except AttributeError:
            res['title'] = None
        try:
            res['salary'] = soup.find('div', attrs={'data-qa': 'vacancy-salary'}).text.replace('\xa0', '')
        except AttributeError:
            res['salary'] = None
        try:
            res['vacancy_experience'] = soup.find('span', attrs={'data-qa': 'vacancy-experience'}).text
        except AttributeError: res['vacancy_experience'] = None
        try:
            res['employment_mode'] = soup.find('p', attrs={'data-qa': 'vacancy-view-employment-mode'}).text
        except AttributeError:
            res['employment_mode'] = None

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


