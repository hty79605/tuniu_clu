import pymysql
import re

db = pymysql.connect("127.0.0.1", "root", "yimeng", "test", charset="utf8")
cur = db.cursor()

rs = []

writer = '长颈鹿是我'
title = '一个人的旅途\'穿越大西北 青海甘肃七日游'
address = '青海'



infor = ['出发时间/2017-05-03','出行天数/7 天','人物/一个人','人均费用/3000RMB']
webID = 'm8759138'

restr = r'[^a-zA-Z0-9{}【】+！……@#¥%& （）()～~ -\|,.，。;:：；\u4e00-\u9fa5]'
writer1 = re.sub(restr, '', str(writer))
title1 = re.sub(restr, ' ', title)

#sql1 = "select url from notema "

sql = "INSERT INTO notema(title,author,datee,url,address,days,withh,cost)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % \
              (title1, writer1, infor[0][5:],webID, address, infor[1][5:], infor[2][3:], infor[3][5:])
try:
    cur.execute(sql)
    db.commit()
except:
    db.rollback()
    print('\n******' + writer[8:], address, title, webID[2:] + "\n")
