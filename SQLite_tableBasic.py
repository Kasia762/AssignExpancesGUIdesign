import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#date = "23-10-2020"
#shop ='Hesburger'
#price = 15.5
#cat = "restaurant"
val =[("12-03-2019","Lidl","12.34","food"),
      ("07-03-2019","Hesburger","12.34","restaurant"),
      ("12-04-2019","McDonald","10.65","food"),
      ("12-03-2019","Obi","12.34","home"),
      ("12-06-2019","Hesburger","189.65","restaurant"),
      ("12-03-2020","Biedronka","156.32","food"),
      ("10-05-2019","rent","1200.65","bills"),
      ("12-03-2020","electricity","126.68","bills"),
      ("15-09-2019","water","652.21","bills"),
      ]

conn = sqlite3.connect('spend.db')
cur = conn.cursor()
try:
    cur.execute('CREATE TABLE spendings (date VARCHAR, shop VARCHAR, price FLOAT, cat VARCHART)')
    conn.commit()
except sqlite3.OperationalError:
    pass
sql = 'INSERT INTO spendings (date, shop, price, cat) values (?,?,?,?)'
#val = (date, shop, price, cat)
#cur.execute(sql, val)
cur.executemany(sql,val)
conn.commit()

#data = cur.fetchall()
for row in cur.execute('SELECT * FROM spendings ORDER BY price'):
    print(row)
        
for money in cur.execute('SELECT avg(price) FROM spendings '):
    print(money)
        
for price in cur.execute('SELECT avg(price) FROM spendings WHERE cat = "food"'):
    print("avr price for food: %.2f" % price[0],type(price[0]))
        
conn.close()


