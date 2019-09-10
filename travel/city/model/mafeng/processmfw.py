
'''爬取游记信息的地方有些繁琐 都是用循环爬取到每个字保存在列表中 最后转换为字符串
    游记的重复检查是通过数据库的 ID列唯一检查 '''

import requests
from bs4 import BeautifulSoup
import os,sys,re,time,threading,shutil,pymysql
from selenium import webdriver
from multiprocessing import Pool, Queue, Manager
from tkinter import *
from concurrent.futures import ThreadPoolExecutor

class download1:
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect("127.0.0.1", "root", "yimeng", "test", charset="utf8")
        self.cur = self.db.cursor()
        # 通过数据库url判断是否重复爬取
        sqls = "select url from notema"
        self.cur.execute(sqls)
        self.rs = []
        for i in self.cur.fetchall():
            for j in i:
                self.rs.append(j[1:])
        self.root = Tk()  # 初始化Tk()
        self.root.title("游记")  # 设置窗口标题
        self.root.geometry('600x420+300+200')  # 设置窗口大小 注意：是x 不是*
        self.lb = Listbox(self.root, height=20)
        scrl = Scrollbar(self.root)
        scrl.pack(side=RIGHT, fill=Y)
        self.lb.configure(yscrollcommand=scrl.set)  # 指定Listbox的yscrollbar的回调函数为Scrollbar的set，表示滚动条在窗口变化时实时更新
        self.lb.pack(side=TOP, fill=BOTH)
        scrl['command'] = self.lb.yview  # 指定Scrollbar的command的回调函数是Listbar的yview
        self.l = Label(self.root, font=("Arial", 12), width=8, height=3)
        self.l.pack()

        self.l.config(text='正在爬取...')
        button = Button(self.root, text='开始爬取', font=('微软雅黑', 10), command=self.main)
        button.pack(side=BOTTOM)

        self.root.mainloop()

    # 通过游记地址 和 无头浏览器 获得每一篇游记的HTML
    def getHTMLText1(self,url,webID):
        try:
            time.sleep(3)
            number = 0
            driver = webdriver.PhantomJS()
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # 因为网速太慢 为了爬取多篇游记 找到游记的照片数量 爬取数量少于260的
            # 若要爬取所有游记 这段代码可删除
            total = soup.find('div', 'vc_total _j_help_total')
            number = re.findall(r"\d*\b</span>张", str(total))
            number = re.findall(r"\d*",number[0])
            number = int(number[0])
            print(url,number,"\n")
            if number > 60:
                print(webID,"图片过多\n")
                download1.rs.append(webID[2:])
                return "",number
            if (webID[2:] in download1.rs):
                print(webID[2:],"已经爬取\n")
                return "",number

            #页面动态加载 翻页
            for i in range(20):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            list_url = driver.page_source
            return list_url,number
        except:
            return "",number

    # 在游记页面获得每一篇游记的地址
    def getList(self,stockURL):
        soup = BeautifulSoup(stockURL, 'html.parser')
        a = soup.find_all('a')
        list=[]
        for i in a:
            try:
                href = i.attrs['href']
                list.append(re.findall(r"i/\d{7}", href)[0])
            except:
                continue
        return list


    # 找到每一篇游记 开始爬取游记的内容 在文件源代码地址的下面获得作者和游记的地点
    # 作者 出游时间 出游天数 和谁 花费
    def getInfo(self,webID):
        print(webID,"开始爬取\n")
        output_file = '/Users/dongyimeng/Desktop/youji1/'
        info_url = 'https://m.mafengwo.cn/'
        #每篇游记的URL
        url = info_url + webID + ".html"

        #获得每个URL的文件对象
        html,number= self.getHTMLText1(url,webID)

        lis = []  # 游记内容
        title =''  #游记标题
        infor = [] # 时间 天数 和谁 花费

        #文件的位置
        ospath = output_file +'m'+ webID[2:] + '/'
        # 对游记的HTML分析和 爬取数据的保存
        try:
            if html == "":
                return

            soup = BeautifulSoup(html, 'html.parser')

            #判断文件夹是否存在 创建文件夹和下一级的保存照片pic文件夹
            if os.path.exists(ospath):
                print(webID,"文件已经存在\n")
                shutil.rmtree(ospath)
                return
            else:
                os.makedirs(ospath)
                os.makedirs(ospath + 'pic/')  # 创建图片的文件夹


            # 获得作者 在HTML的头部
            writerr = soup.find('meta', attrs={'name': 'author'})
            writer = writerr['content']

            # 获得地点  在HTML的头部
            wheree = soup.find('meta', attrs={'name': 'keywords'})
            address = wheree['content']
            address = re.sub('旅游攻略', '', address)
            address = re.sub('自助游攻略', '', address)

            # 获得标题
            name = soup.find(attrs={'class': 'headtext lh80'})
            title = name.string

            self.lb.insert(END, title + '\n开始爬取\n')
            self.root.update()

            # 获得出游时间
            a = soup.find('li', 'time')
            if a:
                infor.append(a.text)
            else:
                infor.append('      ')
            #出游天数
            a = soup.find('li', 'day')
            if a:
                infor.append(a.text)
            else:
                infor.append('      ')
            #和谁出游
            a = soup.find('li', 'people')
            if a:
                infor.append(a.text)
            else:
                infor.append('      ')
            #花费
            a = soup.find('li', 'cost')
            if a:
                infor.append(a.text)
            else:
                infor.append('      ')

            # 获得游记内容 下载图片到pic文件夹
            Info = soup.find('div', '_j_content_box')
            picnum = 1
            # 保存P标签的文字内容和br标签  不要P标签下面的a标签
            for i in Info:
                if i.name == 'p':
                    lis.append("<p>")
                    for j in i:
                        if j.name == 'a':
                            lis.append(j.string)
                            continue
                        if j.name == 'img':
                            continue
                        else:
                            lis.append(str(j))
                    lis.append("</p>")

                #保存图片 div标签下面 a标签下面 的img标签
                elif i.name == 'div':
                    for j in i:
                        if j.name == 'a':
                            for k in j:
                                if k.name == 'img':  # 找到图片的标签
                                    # 下载图片到本地pic文件夹
                                    try:
                                        pict = requests.get(k['data-src'])  # 通过标签的一个属性获得图片的URL
                                    except:
                                        continue
                                    string = ospath + 'pic/' + str(picnum) + '.jpg'
                                    # 打开图片的文件夹 保存图片
                                    fp = open(string, 'wb')
                                    fp.write(pict.content)
                                    fp.close()
                                    #把图片的标签和信息保存在信息文本中
                                    lis.append("<br><img src=mafengwo/m"+webID[2:]+"/pic/"+str(picnum)+".jpg><br>")  # 将图片的本地URL保存在游记文档中
                                    picnum += 1
                        #保存h2标签 删除其中的class属性
                        elif j.name == 'h2':
                            del j['class']
                            lis.append(str(j))
            lis=''.join(lis)
            picnum = picnum - 1
            if(picnum-number>5 or picnum-number<-5):
                print(webID,title,picnum-1,number,"\n")
                shutil.rmtree(ospath)
                return
            # 写入数据库
            # 匹配汉字字母标点
            restr = r'[^a-zA-Z0-9{}【】+！……@#¥%& （）\'()～~ -\|,.，。;:：；\u4e00-\u9fa5]'
            writer1 = re.sub(restr, '', str(writer))
            title1 = re.sub(restr, '', title)
            sql = "INSERT INTO notema(title,author,datee,url,address,days,withh,cost)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % \
                  (title1, writer1[8:], infor[0][5:], 'm' + webID[2:], address, infor[1][5:], infor[2][3:], infor[3][5:])
            try:
                self.cur.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                print('\n******' + title1, writer1[8:], infor[0][5:], 'm' + webID[2:], address, infor[1][5:], infor[2][3:],
                      infor[3][5:] + "\n")

            # 写入文件名为游记的 m+ID 文件里的 date.txt
            with open(ospath +'data.txt', 'w', encoding='utf-8') as f:
                # 标题
                f.write('\n\n' + title + '\n\n\n')

                # 作者
                f.write(writer[8:] + '\n')

                # 出游的时间 出游天数 和谁 花费
                for i in infor:
                    f.write(i + '\n')

                # 游记内容
                f.write(lis)
            self.rs.append(webID[2:])
            self.lb.insert(END,url+'\n'+title+'\n爬取完毕\n')
            self.root.update()
            print(webID,"爬取完毕")
        except:
            return


    def main(self):
        print('main')
        web_list_url = 'https://m.mafengwo.cn/note/'

        # 使用无头浏览器
        driver = webdriver.PhantomJS()

        # 进入马蜂窝游记页面
        driver.get(web_list_url)

        page = 1
        while page:
            # 获取网页文件对象
            list_url = driver.page_source
            url_list = self.getList(list_url)

            pool = Pool(4)  # 创建进程池
            for i in url_list:
                if i[2:] in self.rs:
                    print(i[2:], "已经爬取")
                    continue
                print(i[2:])
                pool.apply_async(self.getInfo, args=(i,))  # 传入进程函数名和url列表 产生子进程
            pool.close()  # 关闭进程池
            pool.join()  # 主进程阻塞

            driver.find_element_by_xpath("//a[contains(text(),'加载更多')]").click()
            page = page - 1
            time.sleep(5)

        driver.quit()
        self.l.config(text='爬取完成...')
        # 关闭数据库
        self.cur.close()
        self.db.close()
