# 读取表格型数据，获取特征数据集。
from math import sqrt

from PIL import Image, ImageDraw


def readfile(filename):
    lines=[line for line in open(filename)]

    # 第一行是列标题
    colnames=lines[0].strip().split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip().split('\t')
        # 每行的第一列是行名
        rownames.append(p[0])
        # 剩余部分就是该行对应的数据
        onerow = [float(x) for x in p[1:]]
        data.append(onerow)
    return rownames,colnames,data


# 定义一个聚类，包含左右子聚类。
class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left    #左子聚类
        self.right=right  #右子聚类
        self.vec=vec      #聚类的中心点
        self.id=id        #聚类的id
        self.distance=distance  #左右子聚类间的距离（相似度）

# 计算两行的皮尔逊相似度
def pearson(v1,v2):
    # 简单求和
    sum1=sum(v1)
    sum2=sum(v2)

    # 求平方和
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])

    # 求乘积之和
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

    # 计算r
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: return 0

    return 1.0-num/den


# 根据数据集形成聚类树
def hcluster(rows,distance=pearson):
    distance_set={}
    currentclustid=-1

    # 最开始聚类就是数据集中的行，每行一个聚类
    clust=[bicluster(rows[i],id=i) for i in range(len(rows))]   #原始集合中的聚类都设置了不同的正数id，（使用正数是为了标记这是一个叶节点）（使用不同的数是为了建立配对集合）

    while len(clust)>1:
        lowestpair=(0,1)
        closest=distance(clust[0].vec,clust[1].vec)

        # 遍历每一对聚类，寻找距离最小的一对聚类
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                # 用distance_set来缓存距离最小的计算值
                if (clust[i].id,clust[j].id) not in distance_set:
                    distance_set[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)

                d=distance_set[(clust[i].id,clust[j].id)]

                if d<closest:
                    closest=d
                    lowestpair=(i,j)

        # 计算距离最近的两个聚类的平均值作为代表新聚类的中心点
        mergevec=[(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]

        # 将距离最近的两个聚类合并成新的聚类
        newcluster=bicluster(mergevec,left=clust[lowestpair[0]],
                             right=clust[lowestpair[1]],
                             distance=closest,id=currentclustid)

        # 不再原始集合中的聚类id设置为负数。为了标记这是一个枝节点
        currentclustid-=1
        # 删除旧的聚类。（因为旧聚类已经添加为新聚类的左右子聚类了）
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]   #返回聚类树

def getheight(clusttree):
    # 若是叶节点则高度为1
    if clusttree.left==None and clusttree.right==None: return 1

    # 否则，高度为左右分枝的高度之和
    return getheight(clusttree.left)+getheight(clusttree.right)

def getdepth(clusttree):
    # 一个叶节点的距离是0.0
    if clusttree.left==None and clusttree.right==None: return 0

    # 一个叶节点的距离=左右两侧分支中距离较大者 + 该支节点自身的距离
    return max(getdepth(clusttree.left),getdepth(clusttree.right))+clusttree.distance

def drawnode(draw,clust,x,y,scaling,labels):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2
        # 线的长度
        ll=clust.distance*scaling
        # 聚类到其子节点的垂直线
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

        # 连接左侧节点的水平线
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

        # 连接右侧节点的水平线
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

        # 调用函数绘制左右子节点
        drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
        drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
    else:
        # 如果这是一个叶节点，则绘制节点的标签文本
        draw.text((x+5,y-7),labels[clust.id],(0,0,0))

# 绘制树状图——为每一个最终生成的聚类创建一个高度为20像素，宽度固定的图片。其中缩放因子是由固定宽度除以总的深度得到的
def drawdendrogram(clusttree, labels, jpeg='clusters.jpg'):
    # 高度和宽度
    h = getheight(clusttree) * 20
    w = 1200
    depth = getdepth(clusttree)

    # 由于宽度是固定的，因此我们需要对距离值做相应的调整。（因为显示窗口宽度固定，高度可上下拖动）
    scaling = float(w - 150) / depth

    # 新建一个白色背景的图片
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # 画根节点（会迭代调用画子节点）
    drawnode(draw, clusttree, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')

if __name__=='__main__':
    blognames,words,data = readfile('blogdata.txt')  #加载数据集
    #clust = hcluster(data)  #构建聚类树
    #drawdendrogram(clust,blognames,jpeg='blogclust.jpg')  # 绘制聚类树