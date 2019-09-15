import pandas as pd
import seaborn as sns  #用于绘制热图的工具包
from scipy.cluster import hierarchy  #用于进行层次聚类，话层次聚类图的工具包
from scipy import cluster
import matplotlib.pyplot as plt
from sklearn import decomposition as skldec #用于主成分分析降维的包

df = pd.read_excel("test.xlsx",index_col=0)  #index_col=0指定数据中第一列是类别名称，PS：计算机程序一般从整数0开始计数，所以0就代表第一列
#df = df.T    #python默认每行是一个样本，如果数据每列是一个样本的话，转置一下即可

Z = hierarchy.linkage(df, method ='ward',metric='euclidean')
hierarchy.dendrogram(Z,labels = df.index)

label = cluster.hierarchy.cut_tree(Z,height=0.8)
label = label.reshape(label.size,)

#根据两个最大的主成分进行绘图
pca = skldec.PCA(n_components = 0.95)    #选择方差95%的占比
pca.fit(df)   #主城分析时每一行是一个输入数据
result = pca.transform(df)  #计算结果
plt.figure()  #新建一张图进行绘制
print(result)
print(result[:, 0])
print(result[:, 1])
plt.scatter(result[:, 0], result[:, 1], c=label, edgecolor='k') #绘制两个主成分组成坐标的散点图
for i in range(result[:,0].size):
    plt.text(result[i,0],result[i,1],df.index[i])     #在每个点边上绘制数据名称
x_label = 'PC1(%s%%)' % round((pca.explained_variance_ratio_[0]*100.0),2)   #x轴标签字符串
y_label = 'PC1(%s%%)' % round((pca.explained_variance_ratio_[1]*100.0),2)   #y轴标签字符串
plt.xlabel(x_label)    #绘制x轴标签
plt.ylabel(y_label)    #绘制y轴标签
plt.show()
