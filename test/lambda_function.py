import threading
import time
import sql1#,sql2

#sql1.connnect()
#sql2.connnect()

def t1():
    while(True):
        res = sql1.connnect()
        print(res)
        #print(sql1.get_user_unionid('e077a48bcb52137c9e33dee7ea7b94c8'))
        #sql1.disconnect()
        time.sleep(3)

def t2():
    while(True):
        res = sql1.connnect()
        print(res)
        #print(sql1.get_user_unionid('1dfc606cc02cb31688c6a81b33dd7cc3'))
        #sql1.disconnect()
        time.sleep(3)


thread1 = threading.Thread(target=t1)
thread2 = threading.Thread(target=t2)    
thread1.start()
thread2.start()