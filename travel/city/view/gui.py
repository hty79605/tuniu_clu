from tkinter import *

#import city.model.mafeng.threadmfw as down
#import city.model.mafeng.processmfw as down
from tkinter.ttk import Combobox

import travel.city.model.mafeng.mfw as mafw
import travel.city.model.tuniu.tuniu as tun
import tkinter.ttk as ttk
from travel.city.model.tuniu.tuniu_clu import *



root = Tk() # 初始化Tk()
root.title("游记")    # 设置窗口标题
root.geometry('600x600+400+100')    # 设置窗口大小 注意：是x 不是*

def help():
    fa1.place(x=0, y=0)

def download():
    fa2.place(x=0, y=50) #触发事件时 显示frame place位置

def analy():
    monty.place(x=0, y=100)

# button被点击之后会被执行
def click():  # 当acction被点击时,该函数则生效
    c = int(number.get())
    total = int(times.get())
    string = draw(total, c)
    #Label(root, text=string).pack()
    print(string)


def mfw():
    mafw.download1()  # 蚂蜂窝爬取文件对象
def tn():
    tun.download1()

menubar = Menu(root) #菜单栏

menubar1=Menu(menubar) #菜单
menubar2=Menu(menubar)
menubar3=Menu(menubar)

menubar1.add_command(label='文件爬取',command=download) #添加的是下拉菜单的菜单项 触发事件
menubar2.add_command(label='文件分析',command=analy)
menubar3.add_command(label='帮助',command=help)

menubar.add_cascade(label='文件爬取',menu=menubar1) #menu 指明了要把那个菜单级联到该菜单栏上
menubar.add_cascade(label='文件分析',menu=menubar2)
menubar.add_cascade(label='帮助',menu=menubar3)

fa1 = Frame(root,height=50,width=600) #Frame就是屏幕上的一块矩形区域，多是用来作为容器
Label(fa1, text='点击文件爬取，选择途牛或者蚂蜂窝网站，开始爬取').pack()

v = IntVar() #创建一个Radiobutton组，并绑定到整型变量v
v.set(1)
fa2 = Frame(root,height=50,width=600)
Radiobutton(fa2,text='途牛',variable=v,value=1,command=tn).pack()
Radiobutton(fa2,text='蚂蜂窝', variable=v, value=2,command=mfw).pack()  #pack方法会让控件显示，并根据文本内容自动调节大小 command触发事件

monty = Frame(height=50,width=600)
aLabel = Label(monty, text="A Label")  # 设置其在界面中出现的位置  column代表列   row 代表行

Label(monty, text="选择聚类次数:").grid(column=1, row=0)  # 添加一个标签，并将其列设置为1，行设置为0
Label(monty, text="输入类的个数:").grid(column=0, row=0, sticky='W')

# 按钮
action = ttk.Button(monty, text="聚类", command=click)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
action.grid(column=2, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行

# 文本框
number = StringVar()  # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
numberEntered = Entry(monty, width=12,
                          textvariable=number)  # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的number变量上，方便clickMe调用
numberEntered.grid(column=0, row=1, sticky=W)  # 设置其在界面中出现的位置  column代表列   row 代表行
numberEntered.focus()  # 当程序运行时,光标默认会出现在该文本框中

# 创建一个下拉列表
times = StringVar()
timesChosen = Combobox(monty, width=12, textvariable=times, state='readonly')
timesChosen['values'] = (5, 8, 10, 15, 20)  # 设置下拉列表的值
timesChosen.grid(column=1, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
timesChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值


root['menu'] = menubar # 最后可以用窗口的 menu 属性指定它的顶层菜单
root.mainloop() #让根窗口进入事件循环