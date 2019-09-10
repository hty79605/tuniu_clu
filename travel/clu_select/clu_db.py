import pymysql.cursors

#通过游记编号文本和分类结果文本将分类结果存入数据库
def tr_save():
    #构造编号列表
    text_num = 1000  #分析的文本数量
    source1 = open('E:/tuniu_clu/path.txt', 'r')   #读取游记文本标号, 防止BOM
    source2 = open('E:/tuniu_clu/result_3.txt', 'r')
    list_num = []
    n = 1
    while n <= text_num:
        line1 = source1.readline()
        list_num.append(line1.rstrip('\n'))
        n = n + 1
    #整合列表
    tf_list = [[] for i in range(text_num)]
    result = []
    with open('E:/tuniu_clu/result_3.txt', 'r') as f:
        for line in f:
            result.append(list(map(str, line.split(' '))))
        #print(result)
    for lst in result:
        del lst[-1]
    #print(result)
    clu = 1
    for lc in result:
        for i in lc:
            n = int(i)
            tf_list[n - 1].append(int(list_num[n - 1]))
            tf_list[n - 1].append(clu)
        clu = clu + 1
    #print(tf_list)

    #存入mysql tf表
    db = pymysql.connect(host='127.0.0.1',
                         port=3306, user='root',
                         password='hetianyu951',
                         db='test', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)  # 连接数据库
    cur = db.cursor()  # 创建游标
    sql = '''INSERT INTO TF(number,cluster)VALUES(%s,%s)'''

    for lst in tf_list:
        cur.execute(sql, lst)  # 存一行

    db.commit()  # 执行
    cur.close()
    db.close()

tr_save()