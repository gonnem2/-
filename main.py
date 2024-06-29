from fastapi import FastAPI, Query
import sqlite3 as sq
from typing import List
from VAKANS import vakancy

app = FastAPI(
    title='hh'
)

conn = sq.connect('Vakans.db', check_same_thread=False)
cursor = conn.cursor()






@app.get('/get_vakans')
def get_vakans():

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
def get_rezume(param: List[str] = Query('test')):
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
        data[str(c)] = res
        c += 1
    return data
