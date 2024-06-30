import requests
import fake_useragent
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import Table, String, Integer, Column, MetaData


def vakancy(search= 'false', salary = 'false', education_level = 'false'):

    higher = 'higher' if education_level == 'higher' else 'false'
    not_required_or_not_specified = 'not_required_or_not_specified' if education_level == 'not_required_or_not_specified' else 'false'
    special_secondary = 'special_secondary' if education_level == 'special_secondary' else 'false'

    url = f"https://hh.ru/search/vacancy?text={search}&salary={salary}&ored_cluster=true&only_with_salary=true&education={higher}&education={not_required_or_not_specified}&education={special_secondary}&page=1&hhtmFrom=resume_search_result&hhtmFromLabel=vacancy_search_line"
    baze = 'https://hh.ru/'
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
    headers={
            "user-agent":user_agent.random
        }

    response_main = requests.get(
        url=url, headers=headers
    )

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















