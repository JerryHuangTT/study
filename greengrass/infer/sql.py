import sqlite3

conn = None
def connect():
    global conn
    if not conn:
        #允许多线程使用
        conn = sqlite3.connect('/tmp/data.db',check_same_thread = False)
    if conn:
        #没表格自动创建
        create_tb()

def create_tb():
    sql = '''create table if not exists device
       (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       timestamp BIGINT,
       x1         REAL,
       x2         REAL,
       y1         REAL,
       y2         REAL,
       z1         REAL,
       z2         REAL,
       type      INT);'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def insert(rows):
    cur = conn.cursor()
    sql = """insert into device(
    timestamp,x1,x2,y1,y2,z1,z2,type)
    values(?,?,?,?,?,?,?,?)"""
    cur.executemany(sql,rows)
    conn.commit()

def select(name):
    cur = conn.cursor()
    sql = 'select * from device'
    cur.executemany(sql,[name])
    return cur.fetchall()