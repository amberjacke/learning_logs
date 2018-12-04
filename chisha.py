import tkinter
import random
import threading
import time

#  初始化窗口
root = tkinter.Tk()
root.title("随机名单")
root.geometry('500x500+400+200')
root.resizable(False,False)
root.flag = True


#  三个Lable标签
first = tkinter.Label(root, text='', font=("宋体", 20,"normal"))
first.place(x=180,y=100,width=150, height=100)

second = tkinter.Label(root, text='', font=("宋体", 20,"normal"))
second['fg'] = 'red'
second.place(x=180,y=200,width=150,height=100)

third = tkinter.Label(root,text='', font=("宋体", 20,"normal"))
third.place(x=180, y=300, width=150, height=100)


students = []
b = 0
c = input('今天你想吃几种菜？')
for b in range(int(c)):
    a = input('请输入名字：')
    students.append(a)
    b = b+1

def switch():
    root.flag=True
    while root.flag:
        i=random.randint(0, len(students)-1)
        first['text']=second['text']
        second['text']=third['text']
        third['text']=students[i]
        time.sleep(0.1)


#  开始按钮
def butStartClick():
    t=threading.Thread(target=switch)
    t.start()
btnStart=tkinter.Button(root,text='开始',command=butStartClick)
btnStart.place(x=30, y=30, width=80, height=20)

#结束按钮
def btnStopClick():
    root.flag=False
    
butStop=tkinter.Button(root,text='停止',command=btnStopClick)
butStop.place(x=160, y=30, width=80, height=20)

#启动主程序
root.mainloop()