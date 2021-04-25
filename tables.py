# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:53:00 2021

@author: ilia
"""

import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#date = "23-10-2020"
#shop ='Hesburger'
#price = 15.5
#cat = "restaurant"
val =[
      ("12-03-2019","Lidl","12.34","food"),
      ("07-03-2019","Hesburger","12.34","restaurant"),
      ("12-04-2019","McDonald","10.65","food"),
      ("12-03-2019","Obi","12.34","home"),
      ("12-06-2019","Hesburger","189.65","restaurant"),
      ("12-03-2020","Biedronka","156.32","food"),
      ("10-05-2019","rent","1200.65","bills"),
      ("12-03-2020","electricity","126.68","bills"),
      ("15-09-2019","water","652.21","bills")
     ]

#conn = sqlite3.connect('spend.db')
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
try:
    cur.execute(''' 
                CREATE TABLE categories (
                    cat_id INTEGER NOT NULL  PRIMARY KEY,
                    cat_name TEXT NOT NULL,
                    cat_limit FLOAT
                    );
                ''')
    cur.execute('''
                CREATE TABLE contractors (
                    cont_id INTEGER NOT NULL  PRIMARY KEY,
                    cont_name TEXT
                    );
                ''')
    cur.execute('''
                CREATE TABLE transactions (
                    trans_id INTEGER NOT NULL  PRIMARY KEY,
                    trans_date DATE NOT NULL,
                    trans_amount REAL NOT NULL,
                    cont_id INTEGER NOT NULL,
                    cat_id INTEGER NOT NULL,
                    CONSTRAINT contractors_cont_id_fk
                        FOREIGN KEY (cont_id)
                        REFERENCES contractors (cont_id),
                    CONSTRAINT categories_cat_id_fk
                        FOREIGN KEY (cat_id)
                        REFERENCES categories (cat_id)
                    );
                ''')
    conn.commit()
except sqlite3.OperationalError as err:
    print("error creating database")
    print(err)
pass



## Generate list of tuples with contractor names
## could be used in CSV importer
## but should be checked is there item already
ind_cont = 1
contr_list = list()
for a in val:
    contr_list.append(  (a[  ind_cont  ],)  )
contr_list = (list(set(contr_list)))
# print(contr_list)

sql = 'INSERT INTO contractors ( cont_name ) values (?)'
cur.executemany(sql,contr_list)
conn.commit()



## Generate list of tuples with categories names
## could be used in CSV importer
## but should be checked is there item already
ind_cat = 3
contr_list = list()
for a in val:
    contr_list.append(  (a[  ind_cat  ],)  )
contr_list = (list(set(contr_list)))
# print(contr_list)

sql = 'INSERT INTO categories ( cat_name ) values (?)'
cur.executemany(sql,contr_list)
conn.commit()



## Generate list of tuples with date and amount names
## could be used in CSV importer
## but should be checked is there item already
ind_date = 0
ind_amount = 2
contr_list = list()
for a in val:
    contr_list.append(  (a[  ind_date  ], a[ ind_amount ] ,
                      a[ ind_cont ] , a[ ind_cat ] ) )
contr_list = (list(set(contr_list)))
# print(contr_list)
            
sql= '''
        INSERT INTO transactions
        ( trans_date, trans_amount,
          cont_id,
          cat_id ) VALUES 
        ( ?, ?,
             (SELECT cont_id FROM contractors WHERE cont_name = ? ),
             (SELECT cat_id FROM categories WHERE cat_name = ? )
        )
     '''   
cur.executemany(sql,contr_list)
conn.commit()



#
#================================================================
#================================================================
# print out all tables
print("Transactions table:")
print("================")
for row in cur.execute('''
                       SELECT *
                       FROM transactions
                       '''):
    print(row)

print("\n\n Contractors table:")
print("================")
for row in cur.execute('''
                       SELECT *
                       FROM contractors
                       '''):
    print(row)

print("\n\n Categories table:")
print("================")
for row in cur.execute('''
                       SELECT *
                       FROM categories
                       '''):
    print(row)
print("")

#================================================================
#================================================================
#####  some sensible request to database

#data = cur.fetchall()
print("\n\n\n Select all transactions and also names of category from other tables")
for row in cur.execute('''
                       SELECT tr.trans_date , tr.trans_amount , ct.cat_name, cr.cont_name
                       FROM transactions AS tr 
                           NATURAL JOIN contractors AS cr
                           NATURAL JOIN categories AS ct
                       ORDER BY tr.trans_amount DESC ;
                       '''):
    print(row)

       
conn.close()


