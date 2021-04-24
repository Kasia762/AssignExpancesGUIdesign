import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#date = "23-10-2020"
#shop ='Hesburger'
#price = 15.5
#cat = "restaurant"
val =[("12-03-2019","18.34","food"),
      ("07-03-2019","1.34","restaurant"),
      ("12-04-2019","10.65","food"),
      ("12-03-2019","1.34","home"),
      ("12-06-2019","189.65","restaurant"),
      ("12-03-2020","15.32","food"),
      ("10-05-2019","160.65","bills"),
      ("12-03-2020","12.68","bills"),
      ("15-09-2019","672.21","bills"),
      ]

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


def insert_data():
    sql = '''INSERT INTO spendings 
    (date, price, cat) 
    values (?,?,?)'''
    cur.executemany(sql,val)
    conn.commit()


def select_data():
    for money in cur.execute('''SELECT avg(price) FROM spendings '''):
        print(money)
            
    for price in cur.execute('''SELECT avg(price) FROM spendings WHERE cat = "food"'''):
        print("avr price for food: %.2f" % price[0],type(price[0]))
    
    conn.commit()
  
create_table()
insert_data()
select_data()     
conn.close()


