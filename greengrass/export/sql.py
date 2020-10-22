import sqlite3
import pandas as pd

conn = None
def connect():
    global conn
    if not conn:
        conn = sqlite3.connect('/tmp/data.db',check_same_thread = False)#允许多线程使用

def select():
    cur = conn.cursor()
    sql = 'select timestamp,x1,x2,y1,y2,z1,z2,type from device'
    cur.execute(sql)
    print('start to read')
    data = cur.fetchall()
    print('rows:'.format(len(data)))
    df = pd.DataFrame(columns=['timestamp','x1','x2','y1','y2','z1','z2','type'],
                                data=data)
    print('start to save')
    df.to_csv('/tmp/data.csv',index=False)
    print('finish saving')
    '''
    sql = 'delete from device'
    cur.execute(sql)
    conn.commit()
    '''