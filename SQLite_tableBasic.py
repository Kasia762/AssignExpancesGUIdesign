import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    import Tkinter as TK
except ImportError:
    import tkinter as TK

def makeWindow(window):
    global nameVar, phoneVar, name2Var, select
    

    frame1 = TK.Frame(window)
    frame1.pack()

    
    TK.Label(frame1, text="date", bg="pink").grid(row=0, column=0, sticky=TK.W)
    nameVar = TK.StringVar()
    name = TK.Entry(frame1, textvariable=nameVar)
    name.grid(row=0, column=1, sticky=TK.W, pady=10, ipadx=50)
  
    TK.Label(frame1, text="amount", bg="pink").grid(row=1, column=0, sticky=TK.W)
    phoneVar= TK.StringVar()
    phone= TK.Entry(frame1, textvariable=phoneVar)
    phone.grid(row=1, column=1, sticky=TK.W, pady=10, ipadx=50)
    
    TK.Label(frame1, text="cat", bg="pink").grid(row=2, column=0, sticky=TK.W)
    name2Var = TK.StringVar()
    name2 = TK.Entry(frame1, textvariable=name2Var)
    name2.grid(row=2, column=1, sticky=TK.W, pady=10, ipadx=50)
  
    frame2 = TK.Frame(window)       # Row of buttons
    frame2.pack()
    b1 = TK.Button(frame2, text="Add", command=addEntry)
    #b2 = TK.Button(frame2, text="Update", command=updateEntry)
    #b3 = TK.Button(frame2, text="Delete", command=deleteEntry)
    #b4 = TK.Button(frame2, text="Load", command=loadEntry)
    b1.pack(side=TK.LEFT,ipadx=10, padx=5)
    #b2.pack(side=TK.LEFT,ipadx=10, padx=5)
    #b4.pack(side=TK.LEFT,ipadx=10, padx=5)
    #b3.pack(side=TK.LEFT,ipadx=10, padx=30)

    frame3 = TK.Frame(window)       # select of names
    frame3.pack(padx=5, pady=5)
    scroll = TK.Scrollbar(frame3, orient=TK.VERTICAL)
    select = TK.Listbox(frame3, yscrollcommand=scroll.set, height=8, width=50)
    scroll.config (command=select.yview)
    scroll.pack(side=TK.RIGHT, fill=TK.Y)
    select.pack(side=TK.LEFT,  fill=TK.BOTH, expand=1)
    return win


val = [([nameVar.get(),phoneVar.get(),name2Var.get()])]


'''val =[("12-03-2019","18.34","food"),
      ("07-03-2019","1.34","restaurant"),
      ("12-04-2019","10.65","food"),
      ("12-03-2019","1.34","home"),
      ("12-06-2019","189.65","restaurant"),
      ("12-03-2020","15.32","food"),
      ("10-05-2019","160.65","bills"),
      ("12-03-2020","12.68","bills"),
      ("15-09-2019","672.21","bills"),
      ]'''

conn = sqlite3.connect('spend.db')
cur = conn.cursor()

def create_table():
    try:
        cur.execute('''CREATE TABLE spendings 
                    (DATE VARCHAR,                
                     PRICE FLOAT, 
                     CAT VARCHART)''') 
    except sqlite3.OperationalError:
        pass
    conn.commit()


def addEntry():
    sql = '''INSERT INTO spendings 
    (DATE, PRICE, CAT) 
    values (?,?,?)'''
    cur.executemany(sql,val)
    conn.commit()


def select_data():
    for money in cur.execute('''SELECT sum(PRICE) FROM spendings '''):
        print(money)
            
    for price in cur.execute('''SELECT avg(PRICE) FROM spendings WHERE CAT = "food"'''):
        print("avr price for food: %.2f" % price[0],type(price[0]))
    for foodSum in cur.execute('''SELECT sum(PRICE) FROM spendings WHERE CAT ="food"'''):
        print("sum for food: ", foodSum)
    
    conn.commit()
  
create_table()

select_data()     
conn.close()

win = TK.Tk()

win = makeWindow(win)


win.configure(bg="pink")
win.title("My Phone Book")
win.geometry("500x300")
win.mainloop()
