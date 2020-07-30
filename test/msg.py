import json
conn = None

def main(unionid,body):
    global conn
    from sql import conn
    method = body['method']
    
    if method == 'get_msg_type':
        return get_msg_type()
    elif method == 'get_msgs':
        imei = None
        main_code = None
        page_no = body['page_no']
        page_size = body['page_size']
        if 'imei' in body.keys():
            imei = body['imei']
        if 'main_code' in body.keys():
            main_code = body['main_code']
        date = '1=1'    
        if 'date_start' in body.keys():
            date = "gmt_create between '{}' and '{}'".format(body['date_start'],body['date_end'])
        return get_msgs(unionid,imei,main_code,page_no,page_size,date)
    elif method == 'set_msg_read':
        return set_msg_read(body['id'])
    elif method == 'set_msgs_read':
        return set_msgs_read(unionid)        
    elif method == 'get_unread_count':
        imei = None
        main_code = None
        date = '1=1'    
        if 'date_start' in body.keys():
            date = "gmt_create between '{}' and '{}'".format(body['date_start'],body['date_end'])        
        if 'imei' in body.keys():
            imei = body['imei']
        if 'main_code' in body.keys():
            main_code = body['main_code']
        return get_unread_count(unionid,imei,main_code,date)  

def get_msgs(unionid,imei,msg_code,page_no,page_size,date):
    #1.多个imei、msg_code的字符串表达式
    exp_imeitype_msgcode = sql_imei_maincode(unionid,imei,msg_code,date)
    
    #2.最终需要生成的sql查询条件
    limit = ' order by gmt_create desc limit ' + str(page_no * page_size) + ',' + str(page_size)
    sql_exp = exp_imeitype_msgcode + limit
    #3.开始查询符合条件的分页数据
    alerts = get_device_msgs(sql_exp)
    
    #4.查询全部符合条件的数据总量
    totalElements = get_count_nopage(exp_imeitype_msgcode)
    
    #4.生成返回内容
    total_page = (totalElements + page_size - 1) / page_size
    total_page = int(total_page)
    res = {}
    res['pageNo'] = page_no
    res['pageSize'] = page_size
    res['totalPages'] = total_page
    res['totalElements'] = totalElements
    res['content'] = alerts
    return response(res)
 
def sql_imei_maincode(unionid,imei,main_code,date='1=1'):
    sql = None
    if imei :
        imei = "imei='{}'".format(imei)
    else:
        imeis = get_imeis(unionid)
        imei = 'imei in {} '.format(imeis)
    if main_code:
        main_code = 'main_code={}'.format(main_code)
    else:
        main_code = 'main_code in (1,2)'
    sql = ' where {} and {} and {}'.format(imei,main_code,date)
    return sql

def get_imeis(unionid):
    results = []
    with conn.cursor() as cur:
        sql = "select imei from user_device where unionid='{}'".format(unionid)
        cur.execute(sql)
        for row in cur.fetchall():
            results.append(row[0])
        results = json.dumps(results)
        results = '({})'.format(results[1:len(results)-1])
        return results 
    
#考虑到大页码，先找出符合条件的非业务主键id，再用id获得具体数据
def get_device_msgs(exp):
    with conn.cursor() as cur:
        sql = 'select id from device_msg' + exp
        cur.execute(sql)
        rows = cur.fetchall()
        ids = []
        for row in rows:
            ids.append(row[0])
        return get_alerts(ids)

#用id主键数组查询数据返回内容
def get_alerts(ids):
    if not ids:
        return
    msgs = []
    str_ids = json.dumps(ids)
    str_ids = '(' + str_ids[1:len(str_ids)-1] + ')'
    with conn.cursor() as cur:
        sql = 'select id,gmt_create,is_read,msg_content,device_name,filter_name,main_content from device_msg where id in ' + str_ids + ' order by gmt_create desc'
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            msgs.append({
                'id': row[0],
                'gmt_create': row[1].strftime("%Y-%m-%d %H:%M:%S"),
                'is_read': bool(row[2]),
                'display_content':row[3],
                'device_name':row[4],
                'filter_name':row[5],
                'main_content':row[6]
            })
    return msgs

'''
msg_types = [
    [1,'滤芯信息'],
    [2,'设备故障'],
    [3,'状态更新'],
    [4,'盐位计信息']]
'''

#消息定义
msg_types = [
    [1,'滤芯信息'],
    [2,'设备故障'],
    [4,'盐位计信息']]    

#返回消息代码及名称
def get_msg_type():
    res = []
    for msg_type in msg_types:
        res.append({'main_code':msg_type[0], 'main_content':msg_type[1]})
    return response(res)

#返回不分页的数据总量
def get_count_nopage(exp):
    with conn.cursor() as cur:
        sql = 'select count(*) from device_msg' + exp
        cur.execute(sql)
        return cur.fetchone()[0]

#返回未读消息数量
def get_unread_count(unionid,imei,msg_code,date):
    with conn.cursor() as cur:
        sql = 'select count(*) from device_msg' + sql_imei_maincode(unionid,imei,msg_code) + ' and is_read=0' + ' and {}'.format(date)
        cur.execute(sql)
        return response({'count':cur.fetchone()[0]})

#返回设置消息已读    
def set_msg_read(id):
    with conn.cursor() as cur:
        sql = 'update device_msg set is_read=1 where id=' + str(id)
        cur.execute(sql)
        conn.commit()
        return response({'id':id})

#返回设置全部消息已读    
def set_msgs_read(unionid):
    with conn.cursor() as cur:
        sql = "select imei from user_device where unionid='{}'".format(unionid)
        cur.execute(sql)
        devices = []
        for row in cur.fetchall():
            devices.append(row[0])
        str_ids = json.dumps(devices)
        str_ids = '({})'.format(str_ids[1:len(str_ids)-1])
        sql = 'update device_msg set is_read=1 where imei in {}'.format(str_ids)
        cur.execute(sql)
        conn.commit()
        return response('')

def response(data):
    return {'code':0,'msg':'','data':data}