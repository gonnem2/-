import requests
import fake_useragent
from bs4 import BeautifulSoup


baze = 'https://hh.ru/'
data = list()
user_agent = fake_useragent.UserAgent()
headers={
        "user-agent":user_agent.random
    }

response_main = requests.get(
    url="https://hh.ru/search/resume?relocation=living_or_relocation&gender=unknown&text=&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&search_period=0", headers=headers

)




soup = BeautifulSoup(response_main.text, 'html.parser')

vakans = soup.find_all('a', attrs={'data-qa':"serp-item__title"})
for i in vakans:
    res = {
        "spec": list(),
        "zan'yatost": str(),
        "grafick" : str(),
        'naviki': list(),
        'education_name': list()

    }
    response = requests.get(
        url=(baze + str(i['href'])),
        headers=headers
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    res['title'] = (soup.find('span', attrs={'class': 'resume-block__title-text'})).text
    try:
        res['salary'] = ((soup.find('span', attrs={'class': 'resume-block__salary'})).text).replace('\xa0', '').replace('\u2009', '')
    except AttributeError:
        res['salary'] = None
    for i in soup.find_all('li', attrs={'class': 'resume-block__specialization'}):
        res['spec'].append(i.text)
    try:
        res["zan'yatost"], res["grafick"] = (str(i.text.split(":")[1]) for i in soup.find_all('p', attrs={})[4:6])
    except IndexError:

        res["zan'yatost"], res["grafick"] = (str(i.text.split(":")[1]) for i in soup.find_all('p', attrs={})[3:5])

    res['opit'] = soup.find('span', attrs={'class': 'resume-block__title-text resume-block__title-text_sub'}).text.replace('\xa0', ' ')

    try:
        res['about'] = str(soup.find('div', attrs={'data-qa': 'resume-block-skills-content'}).text).replace('\n', ' ').replace('\r', '')
    except AttributeError:
        res['about'] = None

    try:
        a = soup.find('div', attrs={'data-qa':"skills-table"}).find_all('span', attrs={'class': 'bloko-tag__section bloko-tag__section_text'})
        for i in a:
            res['naviki'].append(i.text)
    except AttributeError:
        res['naviki'] = None

    for i in soup.find_all('div', attrs={'data-qa': "resume-block-education-name"}):
        res['education_name'].append(i.text)

    data.append(res)
print(len(data))


