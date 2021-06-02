import threading
import tkinter as tk
import crawler
from PIL import ImageTk, Image
import webbrowser
myThread = threading.Thread()

def makeWaitUI():
    wnd = tk.Tk()
    lbl = tk.Label(wnd,text="직업이름")
    lbl.grid(row=0, column=0)
    txt = tk.Entry(wnd)
    txt.grid(row=0, column=1)
    def OnClick():
        jobName = txt.get()
        wnd.destroy()
        makeLoadingUI(jobName)
    btn = tk.Button(wnd, text="OK", command=OnClick)
    btn.grid(row=1, column=1)
    lbl2 = tk.Label(wnd, text="작업시간에는 대략 3~4분이 소요됩니다.\n 작업종료 시 새 창으로 알려드립니다.")
    lbl2.grid(row=2, column=0)
    wnd.mainloop()
    
def makeLoadingUI(jobName):
    global myThread
    myThread = threading.Thread(target=crawler.StartCrawling,args=(jobName,))
    myThread.start()
    myThread.join()
    makeResultUI()


def ConstructInfoSite(keyword):
    crawler.ConstructInfoSite(keyword)

def makeResultUI():
    wnd = tk.Tk()

    lbl2 = tk.Label(wnd, text="아래 키워드들 중 더 자세한 정보를 알고싶은 키워드를 누르고 버튼 클릭 시 웹페이지로 연결됩니다. ")
    lbl2.pack()
    
    img = Image.open("img.png")
    img = img.resize((500,500),Image.ANTIALIAS)

    test = ImageTk.PhotoImage(img)
    lbl = tk.Label(wnd, width=500, height=500, image=test)      
    lbl.pack()      
    
    keywordSorted = sorted(crawler.keywords.items(),key=(lambda x :x[1]),reverse=True)

    frame = tk.Frame(wnd)
    scrollbar = tk.Scrollbar(wnd)
    scrollbar.pack(side="right",fill="y")
    listbox = tk.Listbox(frame,yscrollcommand=scrollbar.set)
    
    idx = 0
    for item in keywordSorted:
        listbox.insert(idx,str(item[0]) + " mentioned " + str(item[1]) + " times.")
        idx = idx + 1


    listbox.pack(side="left",fill=tk.BOTH,expand=True)

    scrollbar["command"]=listbox.yview
    frame.pack(fill=tk.BOTH,expand=True)

    def OnClick():
        tempTuple = listbox.curselection()
        tempStr = listbox.get(tempTuple[0])
        strings = tempStr.split("mentioned")
        ConstructInfoSite(strings[0])


    btn = tk.Button(wnd, text="GOTO", command=OnClick)
    btn.pack()
    wnd.mainloop()
    
makeWaitUI()