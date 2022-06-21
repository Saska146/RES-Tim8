import sqlite3
from datetime import datetime


class ModelDB:
    def __init__(self, code, value, timestamp, dataset):
        self.Value = value
        self.Timestamp = timestamp
        self.Dataset = dataset
        self.Code = code


def insertData(data: ModelDB):
    con = sqlite3.connect('res_lb.db')

    cur = con.cursor()

    dtime = datetime.now()
    # Insert a row of data
    cur.execute("""INSERT INTO res_lb (value, timestamp, dataset, code) 
    VALUES (?,?,?,?)""",
                (str(data.Value), str(dtime), str(data.Dataset), str(data.Code)))

    con.commit()
    con.close()


def readData():
    con = sqlite3.connect('res_lb.db')
    cur = con.cursor()

    cur.execute("""SELECT * FROM res_lb""")
    retList = cur.fetchall()

    con.close()
    return retList


def readDataByCode(code):
    con = sqlite3.connect('res_lb.db')
    cur = con.cursor()

    cur.execute(f"""SELECT * FROM res_lb where code = {code}""")
    retList = cur.fetchall()

    con.close()
    return retList


def readLastValueByCode(code_: int):
    con = sqlite3.connect('res_lb.db')
    cur = con.cursor()

    selectQ = """select * from res_lb where code = (?) order by timestamp desc"""
    cur.execute(selectQ, (str(code_),))
    retVal = cur.fetchone()
    con.close()

    return retVal


def readAll():
    lista = [1, 2, 3, 4, 5, 6, 7, 8]
    retList = []
    for i in lista:
        retList.append(readLastValueByCode(i))
    return retList


def readByDateAndCode(datefrom, dateto, timefrom, timeto, code_):
    con = sqlite3.connect('res_lb.db')
    cur = con.cursor()
    dataset = MapDataset(code_)
    str1 = f'{datefrom} {timefrom}'
    str2 = f'{dateto} {timeto}'
    selectQ = f"""select value from res_lb where code = {code_.value} and timestamp > datetime('{str1}') and timestamp < datetime('{str2}')"""
    cur.execute(selectQ)
    retVal = cur.fetchall()
    con.close()

    return retVal


def MapDataset(code_id):
    code_id = code_id.value
    if 1 <= code_id <= 2:
        return 1
    elif 3 <= code_id <= 4:
        return 2
    elif 5 <= code_id <= 6:
        return 3
    elif 7 <= code_id <= 8:
        return 4

# if __name__ == '__main__':
# model = ModelDB(4,323,datetime.now(),2)
# insertData(model)
# print(readByDateAndCode("2022-06-12 19:15:47","2022-06-12 19:45:00",4))
# print(readLastValueByCode(4))
