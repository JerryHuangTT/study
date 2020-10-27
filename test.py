import schedule
import time

# 定义需要执行的方法
def job():
    print("a simple scheduler in python.")

schedule.every().day.at("16:05").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)