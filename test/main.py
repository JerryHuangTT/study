a= [1,2,3,4]
print(a[1:])  

import threading
import time
import sql1,sql2

import numpy as np 

a= 2 * np.arange(10 // 2) 
#a= np.arange()

sql1.connnect()
sql2.connnect()

def t1():
    while(True):
        #sql1.connnect()
        print(sql1.get_user_unionid('e077a48bcb52137c9e33dee7ea7b94c8'))
        #sql1.disconnect()
        time.sleep(3)

def t2():
    while(True):
        #sql2.connnect()
        print(sql2.get_user_unionid('1dfc606cc02cb31688c6a81b33dd7cc3'))
        #sql2.disconnect()
        time.sleep(3)


thread1 = threading.Thread(target=t1)
thread2 = threading.Thread(target=t2)    
thread1.start()
thread2.start()