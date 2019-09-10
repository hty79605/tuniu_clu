import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql.cursors
import re
import os
import sys
import time
import datetime
from multiprocessing.dummy import Pool
from tkinter import *
class download1:
    #模拟爬虫头部
    def __init__(self):
        self.request_headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        'cookie': "uid=ea62e6364dd70780f85787e579947adf; MOBILE_APP_SETTING_STATE-128=CLOSE; MOBILE_APP_SETTING_STATE-132=CLOSE; _tacz2=taccsr%3Dsogou%7Ctacccn%3D%28organic%29%7Ctaccmd%3Dmkt_06022201%7Ctaccct%3D%2525E9%252580%252594%2525E7%252589%25259B%7Ctaccrt%3D%28none%29; _pzfxuvpc=1505198145453%7C2218184043499025928%7C8%7C1509090044739%7C6%7C1427748190107039527%7C1010828185145768630; Hm_lvt_51d49a7cda10d5dd86537755f081cc02=1507717366,1507717392,1509090037,1509090045; __xsptplus352=352.7.1509090046.1509090046.1%231%7Csogou%7Cbrand%7Cbrand%7C%25E9%2580%2594%25E7%2589%259B%7C%23%23kxzUX6LCjRaK4cxLoZK0fjQkVzNTt5e8%23; BSFIT_DEVICEID=3810a6f242134d2a9dc0a5fef03dd111; __ozlvd1940=1509852949; s_nr=1509852949175; tuniu_partner=MTAxLDAsLDlmZDgyZThjYTZkNGMwMTlmZTUyNzdlYjJmNTcxYzQ1; tuniuuser_citycode=MTkwNg%3D%3D; _tacau=MCxkYjk3NjNjYy04NDk0LTc4YjUtYjNhNC02YjJhZTU1MjNlNjUs; _taca=1505198142679.1510665421722.1511172695269.22; _tacc=1; __utmt=1; _csrf=3427aa51656ad94a38eb68f1512ecefb4f825ed9a70092af6a74c37ee98fe2f1a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22gzO7UMJkk9QeU7n_U24MR34H3QsJTWLw%22%3B%7D; __utma=1.73627975.1505198146.1510665422.1511172698.22; __utmb=1.4.9.1511172703353; __utmc=1; __utmz=1.1511172698.22.12.utmcsr=tuniu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; p_phone_400=4007-999-999; p_phone_level=0; p_global_phone=%2B0086-25-8685-9999; OLBSESSID=9ts4hsocgmv41nheg6bfg4glv1; _tact=NGM4NmJjZTItY2NmYy1jOTFiLWU3NzYtZTdmOTc3ZTE5M2Qx; _tacb=OGY1MmMyOGMtYjMxZS01OTJhLTcyNzgtNDU4ZDU3NDhkM2Mz; BSFIT_OkLJUJ=7AAOVM5AC84IP3R5; fp_ver=4.5.2",
        'host': "www.tuniu.com",
        'referer': "http://trips.tuniu.com/",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        }
        self.root = Tk()  # 初始化Tk()
        self.root.title("游记")  # 设置窗口标题
        self.root.geometry('700x420+300+200')  # 设置窗口大小 注意：是x 不是*
        self.lb = Listbox(self.root, height=20)
        scrl = Scrollbar(self.root)  # 滚动条
        scrl.pack(side=RIGHT, fill=Y)
        self.lb.configure(yscrollcommand=scrl.set)  # 指定Listbox的yscrollbar的回调函数为Scrollbar的set，表示滚动条在窗口变化时实时更新
        self.lb.pack(side=TOP, fill=BOTH)
        scrl['command'] = self.lb.yview  # 指定Scrollbar的command的回调函数是Listbar的yview
        self.l = Label(self.root, font=("Arial", 12), width=8, height=3)
        self.l.pack()

        # self.l.config(text='正在爬取...')
        button = Button(self.root, text='开始爬取', font=('微软雅黑', 10), command=self.main)
        button.pack(side=BOTTOM)

        self.root.mainloop()

    def geturlList(self,URL):   #获取一页游记的url
        soup = BeautifulSoup(URL, 'html.parser')
        url_list = []
        u = soup.find_all('a', attrs={'class': 'list-img'})  # 返回游记url所在标签的列表
        for i in u:  # 遍历得到每个标签
            try:
                href = i.attrs['href']  # 得到标签里的url
                url_list.append(href)  # 放入url列表
            except:
                continue  # 若该标签没有href程序继续执行
        return url_list

    def getinList(self,url):    #下载游记内容和图片 将游记信息存入MySQL数据库tr表
        db = pymysql.connect(host='127.0.0.1',
                             port=3306, user='root',
                             password='hetianyu951',
                             db='test', charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)  # 连接数据库
        num = url.split('/')[-1]
        r = requests.get(url, headers=self.request_headers)
        time.sleep(1)
        html = r.text  # 下载游记
        soup = BeautifulSoup(html, 'html.parser')

        txt_list = []  # 临时保存游记内容的列表
        img_list = []  # 临时保存图片地址的列表
        root = 'E:/tuniu/'  # 根目录
        fpath = root + num + '/data.txt'  # 游记存储路径
        ipath = root + num + '/pic/'  # 图片存储路径
        # 方便创建路径文件夹
        path1 = root + num
        path3 = path1 + '/pic'

        if os.path.exists(path1):
            print("游记重复，爬取结束")  # 差异爬取
            sys.exit()
        #获取图片url
        up = soup.find_all('div', attrs={'class': 'section-img'})  # 返回图片所在标签列表
        for i in up:
            for j in i:
                try:
                    img = j.attrs['data-src']  # 获取图片
                    img_list.append(img)  # 存入临时图片列表
                except:
                    continue

        # 清洗标签并增加图片编号
        ul = soup.find_all('div', attrs={'class': 'content-left'})[0]
        c1 = ul.find_all('div', attrs={'class': 'count-content'})[0]
        c1.decompose()
        c2 = ul.find_all('div', attrs={'class': 'content-comment'})[0]
        c2.decompose()
        s = ul.find_all('script')
        for i in s:
            i.decompose()
        for i in ul.descendants:
            if i.name == 'div':
                try:
                    for j in i.descendants:
                        if j.name == 'p':
                            j.decompose()
                except:
                    pass
        pic_num = 0
        for i in ul.descendants:
            if i.name == 'img':
                pic_num = pic_num + 1
                del i['src']
                del i['str']
                del i['style']
                i['data-src'] = 'tuniu/'+ num + '/pic/'+ str(pic_num) + '.jpg'
            if i.name == 'p':
                del i['class']
                try:
                    del i['id']
                    for j in i.descendants:
                        if j.name == 'div':
                            j.decompose()
                except:
                    pass
        data = re.findall(r"(<p>[^<]+</p>)|(<img[^>]*>)", str(ul)) #正则提取p标签和img标签

        # 下载到本地
        for i in data:  # 遍历得到每个标签
            for j in i:  # 遍历得到标签内容
                txt_list.append(j)  # 存入临时游记列表

        # 创建游记存储路径
        if not os.path.exists(path1):  # 创建编号文件路径
            os.mkdir(path1)
        with open(fpath, 'a', encoding='utf-8') as f:  # 存入已创建好的文件
            for k in txt_list:  # 按条存储
                f.write(str(k) + '\n')  # 转为字符串，每条换行

        # 创建图片存储路径
        img_num = 1
        # k.split('/')[-1]
        if not os.path.exists(path3):
            os.mkdir(path3)
        for k in img_list:
            if 'base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==' in k:   #IE6兼容图片问题
                continue
            apath = ipath + str(img_num) + '.jpg'  # 以图片url作图片名
            img_num += 1
            with open(apath, 'wb') as f:
                a = requests.get(k)  # 下载图片
                f.write(a.content)   # 转换二进制编码

        lst = []
        title = soup.find_all('h1', attrs={'class': 'headtext lh80'})  # 返回游记题目所在标签的列表
        lst.append(title[0].text.lstrip())                                         # 获取标题

        self.lb.insert(END, title[0].text.lstrip() + '\n开始爬取\n')
        self.root.update()

        print(title[0].text.lstrip())
        author = soup.find_all('div', attrs={'class': 'auther-name'})  # 返回作者所在标签的列表
        str_a = author[0].text
        lst.append(str_a[:-3])                                            # 获取作者
        ftime = soup.find_all('span', attrs={'class': 'time'})          # 返回游记日期所在标签的列表
        lst.append(re.findall(r"\d{4}-\d{2}-\d{2}", ftime[0].text)[0])  # 获取发表时间
        lst.append(num)                                                   # 获取文件编号
        views = soup.find_all('span', attrs={'class': 'liulan'})       # 获取浏览数
        lst.append(re.findall(r"\d*", views[0].text)[4])
        support = soup.find_all('a', attrs={'title': '顶'})             # 获取顶（支持）数
        lst.append(support[0].text)

        cur = db.cursor()  # 创建游标
        sql = '''INSERT INTO TR(title,author,ftime,number,views,support)VALUES(%s,%s,%s,%s,%s,%s)'''
        cur.execute(sql, lst)  # 存一行
        db.commit()  # 执行
        cur.close()
        db.close()

        self.lb.insert(END, title[0].text.lstrip() + '\n爬取完成\n')
        self.root.update()


    def main(self):  # 主函数
        starttime = datetime.datetime.now() #开始计时
        count = 0  # 记录次数
        url_tuniu = 'http://trips.tuniu.com/'  # 途牛网主页
        driver = webdriver.PhantomJS()  # 模拟浏览器
        driver.get(url_tuniu)  # 爬取主页

        p = 0
        while p < 169:
            driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click()  # 模拟点击翻页
            p = p + 1
            time.sleep(2)

        page = 0  # 初始化页数
        while page < 4:  #下载页数
            url_list = []
            url_list = self.geturlList(driver.page_source)
            pool = Pool(5) #创建进程池
            pool.map(self.getinList, url_list)  # 传入进程函数名和url列表 产生子进程
            pool.close() #关闭进程池
            pool.join() #主进程阻塞
            count = count + 1    # 存储次数加1
            print("\r当前进度: {:.2f}%".format(count * 100 / 4), end="") #显示页数进度
            driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click()  # 模拟点击翻页
            page = page + 1  # 页数加1
            time.sleep(4)    # 睡眠防止被封 翻页等待时间
        driver.quit()        # 关闭浏览器驱动

        endtime = datetime.datetime.now() #结束计时
        print('\n运行时间：')
        print(endtime - starttime)