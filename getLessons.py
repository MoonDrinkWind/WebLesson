
import threading, requests
from concurrent.futures import ThreadPoolExecutor
from lxml import etree

threadLock = threading.Lock()
lessonFile = open("lesson.txt", "a+", encoding="utf-8")

def getLesson(start, end):
    for i in range(start, end):
        url = "http://h5.nty.tv189.com/hv/C4235"+ str(i)  +".html"
        r = requests.get(url, headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}).text
        s = etree.HTML(r)
        titles = s.xpath("/html/head/title/text")
        print(threading.current_thread().name)
        print(url)
        print(titles)
        for title in titles:
            if "九" in title:
                threadLock.acquire()
                lessonFile.write(title + "\n")
                lessonFile.write(url + "\n")
                threadLock.release()
    print(threading.current_thread().name + "爬取结束")   

threadPool = ThreadPoolExecutor(10)
futures = []
for j in range(1, 11):
    futures.append(threadPool.submit(getLesson, start=j*1000-1000, end=j*1000))

def last(future):
    print(future.result())

for future in futures:
    future.add_done_callback(last)

