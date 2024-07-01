from fastapi import FastAPI, Query, Request
import sqlite3 as sq
from typing import List
from VAKANS import vakancy
from rezume import rezume
from fastapi.templating import Jinja2Templates



app = FastAPI(
    title='hh'
)

conn = sq.connect('Vakans.db', check_same_thread=False)
cursor = conn.cursor()






@app.get('/get_vakans')
def get_vakans(search : str = Query(), salary : int = Query(), education_level : str = Query()):
    vakancy(search, salary, education_level)
    cursor.execute('SELECT * FROM Vakancy')
    vakans = cursor.fetchall()
    data = {}
    c = 0
    for i in vakans:
        res = dict()
        res['id'] = i[0]
        res['title'] = i[1]
        res['salary'] = i[2]
        res['experience'] = i[3]
        res['employment_mode'] = i[4]
        res['href'] = i[5]
        data[str(c)] = res
        c += 1
    return data


connn = sq.connect('rezume.db', check_same_thread=False)
cursor_ = connn.cursor()


@app.get('/get_rezume')
def get_rezume(search : str = Query(), age_from : int = Query(), age_to : int = Query(), salary_from : int = Query(), salary_to: int = Query(), experience: str = Query()):
    rezume(search, age_from, age_to, salary_from, salary_to, experience)
    cursor_.execute('SELECT * FROM rezume')
    vakans = cursor_.fetchall()
    data = {}
    c = 0
    for i in vakans:
        res = dict()
        res['id'] = i[0]
        res['title'] = i[1]
        res['salary'] = i[2]
        res['spec'] = i[3]
        res['grafick'] = i[4]
        res['naviki'] = i[5]
        res['education_name'] = i[6]
        res['zanyatost'] = i[7]
        res['opit'] = i[8]
        res['about'] = i[9]
        res['href'] = i[1]
        data[str(c)] = res
        c += 1
    return data


templates = Jinja2Templates(directory='templates')


@app.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {"request": request})