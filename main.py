import sqlite3
from fastapi import FastAPI, Query, Request
import sqlite3 as sq
from fastapi.templating import Jinja2Templates
from VAKANS import vakancy


app = FastAPI(
    title='hh'
)

conn = sq.connect('Vakans.db', check_same_thread=False)
cursor = conn.cursor()

templates = Jinja2Templates(directory='templates')

@app.get('/base/spisock')
def get_base_page(request: Request):
    return templates.TemplateResponse('spisok_vakans.html', {"request": request})


@app.get('/get_vakans')
def get_vakans(request: Request,
               search: str = '',
               salary: str = 'false',
               education: list = Query(default=[]),
               experience: list = Query(default=[]),
               employment: list = Query(default=[]),
               schedule: list = Query(default=[])
               ):
    vakancy(search, salary, education_level=education, experience=experience, employment=employment, schedule=schedule)
    try:
        cursor.execute('SELECT * FROM Vakancy')
        vakans = cursor.fetchall()
        data = []

        for i in vakans:
            res = dict()
            res['id'] = i[0]
            res['title'] = i[1]
            res['salary'] = i[2]
            res['experience'] = i[3]
            res['employment_mode'] = i[4]
            res['href'] = i[5]
            data.append(res)

        return templates.TemplateResponse('spisok_vakans.html', {"request": request, 'data': data})
    except sqlite3.OperationalError:
        return 'Таких вакансий нет'


connn = sq.connect('rezume.db', check_same_thread=False)
cursor_ = connn.cursor()

@app.get('/base')
def get_base_page(request: Request):
    vakancy()
    return templates.TemplateResponse('base.html', {"request": request, 'data': cursor.execute('SELECT * FROM Vakancy').fetchall()})