from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pylab as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

#读取表格
seeds_df = pd.read_csv("https://raw.githubusercontent.com/vihar/unsupervised-learning-with-python/master/seeds-less-rows.csv")
#谷物种类列表
varieties = list(seeds_df.pop('grain_variety'))
#Numpy array
samples = seeds_df.values

"""
Perform hierarchical clustering on samples using the
linkage() function with the method='complete' keyword argument.
Assign the result to mergings.
"""
mergings = linkage(samples, method='complete')

#method是指计算类间距离的方法,比较常用的有3种:
#single:最近邻,把类与类间距离最近的作为类间距
#average:平均距离,类与类间所有pairs距离的平均
#complete:最远邻,把类与类间距离最远的作为类间距
"""
Plot a dendrogram using the dendrogram() function on mergings,
specifying the keyword arguments labels=varieties, leaf_rotation=90,
and leaf_font_size=6.
"""
dendrogram(mergings,
 labels=varieties,
 leaf_rotation=90,
 leaf_font_size=6,
 )

plt.show()