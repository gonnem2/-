import requests
import fake_useragent
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import Table, String, Integer, Column, MetaData


def rezume(title='false', age_from='false', age_to='false', salary_from='false', salary_to='false', experinece='false'):
    engine = sqlalchemy.create_engine("sqlite:///rezume.db")
    conn = engine.connect()

    metadata = MetaData()

    rezume = Table(
        'rezume', metadata,
        Column('id', Integer(), primary_key=True),
        Column('title', String(200)),
        Column('salary', String(200)),
        Column('spec', String(200)),
        Column('grafick', String(200)),
        Column('naviki', String(200)),
        Column('education_name', String(200)),
        Column("zanyatost", String(200)),
        Column("about", String(200)),
        Column("opit", String(200)),
        Column('href', String(200))
    )
    metadata.drop_all(engine)

    baze = 'https://hh.ru/'

    user_agent = fake_useragent.UserAgent()
    headers = {
        "user-agent": user_agent.random
    }
    experience1 = 'noExperience' if experinece == 'noExperience' else 'false'
    experinece2 = 'between3And6' if experinece == 'between3And6' else 'false'
    experince3 = 'between1And3' if experinece2 == 'between1And3' else 'false'

    response_main = requests.get(
        url=f"https://hh.ru/search/resume?relocation=living_or_relocation&gender=male&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&search_period=0&order_by=relevance&filter_exp_period=all_time&experience=moreThan6&experience={experience1}&experience={experinece2}&experience={experince3}&label=only_with_age&label=only_with_salary&label=only_with_gender&text={title}&age_from={age_from}&age_to={age_to}&salary_from={salary_from}&salary_to={salary_to}",
        headers=headers,
        params={
            'gender': "male"
        }

    )

    soup = BeautifulSoup(response_main.text, 'html.parser')

    vakans = soup.find_all('a', attrs={'data-qa': "serp-item__title"})
    for i in vakans:
        res = {
            "spec": list(),
            "zanyatost": str(),
            "grafick": str(),
            'naviki': list(),
            'education_name': list()

        }
        href = baze + str(i['href'])
        response = requests.get(
            url=(href),
            headers=headers
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        res['title'] = (soup.find('span', attrs={'class': 'resume-block__title-text'})).text
        try:
            res['salary'] = ((soup.find('span', attrs={'class': 'resume-block__salary'})).text).replace('\xa0',
                                                                                                        '').replace(
                '\u2009', '')
        except AttributeError:
            res['salary'] = None
        for i in soup.find_all('li', attrs={'class': 'resume-block__specialization'}):
            res['spec'].append(i.text)

        try:
            res["zanyatost"], res["grafick"] = (str(i.text.split(":")[1]) for i in soup.find_all('p', attrs={})[4:6])
        except IndexError:

            res["zanyatost"], res["grafick"] = (str(i.text.split(":")[1]) for i in soup.find_all('p', attrs={})[3:5])

        res['opit'] = soup.find('span',
                                attrs={'class': 'resume-block__title-text resume-block__title-text_sub'}).text.replace(
            '\xa0', ' ')

        try:
            res['about'] = str(soup.find('div', attrs={'data-qa': 'resume-block-skills-content'}).text).replace('\n',
                                                                                                                ' ').replace(
                '\r', '').replace('•\t', '')
        except AttributeError:
            res['about'] = None

        try:
            a = soup.find('div', attrs={'data-qa': "skills-table"}).find_all('span', attrs={
                'class': 'bloko-tag__section bloko-tag__section_text'})
            for i in a:
                res['naviki'].append(i.text)
        except AttributeError:
            res['naviki'] = []

        for i in soup.find_all('div', attrs={'data-qa': "resume-block-education-name"}):
            res['education_name'].append(i.text)

        metadata.create_all(engine)

        ins = rezume.insert().values(
            title=res['title'],
            salary=res['salary'],
            spec=' | '.join(map(str, res['spec'])),
            grafick=res['grafick'],
            naviki=' | '.join(map(str, res['naviki'])),
            education_name=' | '.join(map(str, res['education_name'])),
            zanyatost=res['zanyatost'],
            opit=res['opit'],
            about=res['about'],
            href= href

        )
        print(ins.compile().params)
        conn.execute(ins)
    conn.commit()





