#sql 为以后分库分表准备
import pymysql
import boto3
import os
import ssl

conn = None
def connnect():
    global conn
    if(conn is None or not conn.open):
        conn=pymysql.connect(host=os.environ['db_host'],
        user=os.environ['db_user'],
        password=os.environ['db_pwd'],
        database=os.environ['db_name'],
        charset='utf8',
        connect_timeout=5)
    return conn


def disconnect():
    return


def get_user_unionid(token):
    sql = 'select unionid from user_infor where token=%s'
    with conn.cursor() as cur:
        cur.execute(sql,(token))
        row = cur.fetchone()
        if row:
            return row[0]      
                 
def get_ssl_ctx():
    ca_name = '/tmp/ca.pem'
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(os.environ['s3_bucket']).download_file(os.environ['s3_cafile'],ca_name)
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_verify_locations(ca_name)
        return ssl_ctx
    except Exception as e:
        print(e)
        return None
