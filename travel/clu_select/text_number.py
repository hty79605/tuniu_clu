import os
#拷贝所有游记编号到path文本
path = 'E:/tuniu/'
dirs = os.listdir(path)
for dir in dirs:
    with open('E:/tuniu_clu/path.txt', 'a', encoding='utf-8') as f:
        f.write(dir + '\n')
    #print (dir)