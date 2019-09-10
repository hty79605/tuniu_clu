import os
import jieba
import re
import shutil
import codecs
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import time
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as mp
from pylab import *

#支持中文
#mpl.rcParams['font.sans-serif'] = ['SimHei']

pa = 'E:/'
#分词
def segment():
    if os.path.isdir(pa+"tuniu_clu/tuniu_text"):            #重建游记文本文件夹
        shutil.rmtree(pa+"tuniu_clu/tuniu_text", True)
    os.makedirs(pa+"tuniu_clu/tuniu_text")

    path = pa+"tuniu/"
    respath = pa+"tuniu_clu/text_fork/"
    if os.path.isdir(pa+"tuniu_clu/text_fork"):             #重建分词结果文件夹
        shutil.rmtree(pa+"tuniu_clu/text_fork", True)
    os.makedirs(pa+"tuniu_clu/text_fork")

    #停用词表
    stopwords = {}.fromkeys([line.rstrip() for line in open(pa+'/tuniu_clu/stopword.txt','r+',encoding = 'utf-8')])

    source = open(pa+'/tuniu_clu/path.txt', 'r')   #读取游记文本标号, 防止BOM
    num = 1

    while num<=50:
        line = source.readline()
        line = line.rstrip('\n')
        textpath = path + line + "/data.txt"
        print(textpath)
        copypath = pa+"/tuniu_clu/tuniu_text/" + str(num) + ".txt"
        shutil.copyfile(textpath,copypath)                             #将游记拷贝到文本文件夹
        savepath = respath + str(num) + ".txt"

        content=open(textpath,'r+',encoding = 'utf-8').read()          #读取游记文本内容
        writer=open(savepath,'w+',encoding = 'utf-8')                   #写入分词结果文件夹
        #print content  #打印文本内容
        text=jieba.cut(content)#分词,默认是精确分词
        #print "/".join(text)
        for word in text:
            #通过合并所有中文内容得到纯中文内容
            word=''.join(re.findall(u'[\u4e00-\u9fa5]+', word))#去掉不是中文的内容
            word=word.strip()
            if (len(word) != 0 ):
                #print word
                if word not in stopwords:  #去除停用词
                    writer.write(word+' ')
        writer.flush()
        writer.close()
        print("保存好了")
        num = num +1

#合并，文档预料
def merge_file():
    path = pa+"/tuniu_clu/text_fork/"
    resName = pa+"/tuniu_clu/merge_text.txt"
    if os.path.exists(resName):         #重建合并文本
        os.remove(resName)

    result = codecs.open(resName, 'w', 'utf-8')
    num = 1
    while num <= 50:
        #name = "%04d" % num
        fileName = path + str(num) + ".txt"
        source = open(fileName,'r+',encoding = 'utf-8')
        line = source.readline()
        line = line.strip('\n')
        line = line.strip('\r')

        while line != "":
            #line = unicode(line, "utf-8")
            line = line.replace('\n', ' ')
            line = line.replace('\r', ' ')
            result.write(line + ' ')
            line = source.readline()
        else:
            print('End file: ' + str(num))
            result.write('\r\n')
            source.close()
        num = num + 1
    else:
        print('End All')
        result.close()

#计算IDF,Kmeans,评估
def clu(k_clu,k):
    #                            计算TFIDF

    # 文档预料 空格连接
    corpus = []
    # 读取预料 一行预料为一个文档
    for line in open(pa+'/tuniu_clu/merge_text.txt', 'r', encoding='utf-8').readlines():
        corpus.append(line.strip())
    time.sleep(1)

    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()

    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()

    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()

    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()

    # 打印特征向量文本内容
    print('Features length: ' + str(len(word)))
    resName = pa+"/tuniu_clu/result" + str(k) + ".txt"         #矩阵结果文本
    if os.path.exists(resName):
        os.remove(resName)
    result1 = codecs.open(resName, 'w', encoding='utf-8')
    for j in range(len(word)):
        result1.write(word[j] + ' ')
    result1.write('\r\n\r\n')

    # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    for i in range(len(weight)):
        #print(u"-------这里输出第", i+1, u"个文本的词语tf-idf权重------")
        for j in range(len(word)):
            #print weight[i][j],
            result1.write(str(weight[i][j]) + ' ')
        result1.write('\r\n\r\n')

    result1.close()

    #                              聚类Kmeans

    print('Start Kmeans:')

    clf = KMeans(n_clusters=k_clu)
    s = clf.fit(weight)
    print(s)

    # 中心点
    print(clf.cluster_centers_)

    # 每个样本所属的簇
    print(clf.labels_)
    i = 1
    while i <= len(clf.labels_):
        print(i, clf.labels_[i - 1])
        i = i + 1

        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print(clf.inertia_)

    clu_list = [[] for i in range(k_clu)]
    n = 1
    path = pa+'/tuniu_clu/tuniu_text/'
    while n <= 50:
        clu_list[clf.labels_[n - 1]].append(str(n))
        n = n + 1
    # print(clu_list)

    # 分类结果文本

    resName2 = pa+"/tuniu_clu/result_" + str(k) + ".txt"
    if os.path.exists(resName2):
        os.remove(resName2)
    result2 = codecs.open(resName2, 'w', encoding='utf-8')
    i = 0
    while i < k_clu:
        #result2.write('Label: ' + str(i + 1) + ' ')
        for k in clu_list[i]:
            result2.write(str(k) + ' ')
        result2.write('\r\n')

        i = i + 1
    result2.close()
    return clf.inertia_

#传入聚类次数和类数画出评估图
def draw(total,c):
    segment()          #分词
    merge_file()        #合并文本
    m = 0
    k = 1  #聚类序号 第k次
    y = []
    while k <= total:   #total 聚类总次数
        i = clu(c,k)   #生成tf-idf矩阵、聚类 c类的个数
        y.append(i)
        if k == 1:
            m = i
            k_min = k
        if i < m:
            m = i
            k_min = k  #k_min最小评估值
        k = k + 1
    string = '最小评估值：' + str(m) + '\n第 '+ str(k_min) + ' 次聚类效果最好'
    #print('最小评估值：' + str(m) + '\n第 '+ str(k_min) + ' 次聚类效果最好')
    if total == 5:
        names = ['1', '2', '3', '4', '5']
    if total == 8:
        names = ['1', '2', '3', '4', '5','6','7','8']
    if total == 10:
        names = ['1', '2', '3', '4', '5','6','7','8','9','10']
    if total == 15:
        names = ['1', '2', '3', '4', '5','6','7','8''9','10','11','12','13','14','15']
    if total == 20:
        names = ['1', '2', '3', '4', '5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
    x = range(len(names))
    mp.plot(x, y, marker='o', mec='r', mfc='w', label=u'评估值inertia曲线图')
    mp.legend()  # 让图例生效
    mp.xticks(x, names, rotation=45)
    mp.margins(0)
    mp.subplots_adjust(bottom=0.15)
    mp.xlabel(u"聚类序号")  # X轴标签
    mp.ylabel("inertia")  # Y轴标签
    mp.title("A simple plot")  # 标题
    plt.show()
    return string