
import threading, requests
from concurrent.futures import ThreadPoolExecutor
from lxml import etree

threadLock = threading.Lock()
lessonFile = open("lesson.txt", "w+", encoding="utf-8")
keyWord = input("请输入关键词:")
url = input("请输入目标:")

def getLesson(start, end):
    for i in range(start, end):
        r = requests.get(url.format(i), headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}).text
        s = etree.HTML(r)
        titles = s.xpath("/html/head/title/text()")
        print(threading.current_thread().name)
        print(url.format(i))
        print(titles)
        for title in titles:
            if keyWord in title:
                threadLock.acquire()
                lessonFile.write(title + "\n")
                lessonFile.write(url.format(i) + "\n")
                threadLock.release()
    print(threading.current_thread().name + "爬取结束")   

threadPool = ThreadPoolExecutor(100)
futures = []
for j in range(1, 101):
    futures.append(threadPool.submit(getLesson, start=j*1000-1000, end=j*1000))

def last(future):
    print(future.result())

for future in futures:
    future.add_done_callback(last)

