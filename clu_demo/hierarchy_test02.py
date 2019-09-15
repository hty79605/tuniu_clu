import os
import jieba
import re
import shutil
import codecs
from sklearn.feature_extraction.text import CountVectorizer
import time
import clu_demo.hierarchy_test03


from clu_demo.hierarchy_test03 import drawdendrogram, hcluster


#分词
def segment():
    #停用词表
    stopwords = {}.fromkeys([line.rstrip() for line in open('E:/python/算法练习/jieba01/stopword.txt','r+',encoding = 'utf-8')])
    num = 1
    while num<=50:
        textpath = "E:/python/算法练习/jieba01/tuniu_text/" + str(num) + ".txt"
        savepath = "E:/python/算法练习/jieba01/text_fork/" + str(num) + ".txt"
        content=open(textpath,'r+',encoding = 'utf-8').read()          #读取游记文本内容
        writer=open(savepath,'w+',encoding = 'utf-8')                   #写入分词结果文件夹

        text=jieba.cut(content)#分词,默认是精确分词
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
    path = "E:/python/算法练习/jieba01/text_fork/"
    resName = "E:/python/算法练习/jieba01/merge_text.txt"
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

#词袋,层次聚类
def vec():

    # 文档预料 空格连接
    corpus = []
    # 读取预料 一行预料为一个文档
    for line in open('E:/tuniu_clu/merge_text.txt', 'r', encoding='utf-8').readlines():
        corpus.append(line.strip())
    time.sleep(1)

    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(corpus)
    data = x.toarray()
    colnames = vectorizer.get_feature_names()
    rownames = [str(i) for i in range(1,51)]
    #print(arr)
    return rownames, colnames, data

def main():
    tuniu_num, words, data = vec()
    # print(tuniu_num)
    # print(words)
    # print(data)
    clust = hcluster(data)  #构建聚类树
    drawdendrogram(clust,tuniu_num,jpeg='tuniuclust.jpg')  # 绘制聚类树
if __name__ == '__main__':
    main()