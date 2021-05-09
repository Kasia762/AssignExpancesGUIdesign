# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:53:00 2021

@author: ilia
"""
"""
learn the function __initCreateTables

after that, understand how works:
__tableExists
testPrintAllTables
getContractorsList
getAllTransactions

and finally, write correct SQL query for 
 getAllTransactionsPeriod
getTransactionsPeriod
"""

import sqlite3
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class App_data:
    _class_counter = 0
    
            
    def __init__(self):
        self.__debug = True
        if type(self)._class_counter > 0:
            print("One instance of class",type(self), " already exist.")
            print("For now only one instance is allowed.")
            raise ValueError
            
        type(self)._class_counter += 1
        self.databaseFilename = "app.database.db"
         
        self.default_categories = (
              ("Rent",),
              ("Travel",),
              ("Groceries",),
              ("Subscriptions",),
              ("Guilty Pleasures",),
              ("Lotto",),
             )

        self.default_contractors = (
              ("Lidl",),
              ("S-Market",),
              ("K-Market",),
             )
        
        ### Open connection immideally when running
        ### if no database exist, create it
       # self.database = sqlite3.connect(':memory:', 
       #                 detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.database = sqlite3.connect(self.databaseFilename, 
                        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        print("Loading db")
       # self.__loadDB(self.database, self.databaseFilename)
        if not self.__tableExists(self.database, "transactions"):
            print("Creating tables in database...")
            self.__initCreateTables()
        else:
            print("Tables are exists. Skip")

        
    def __loadDB(self, db, dbfn):
        try:
            databasef = sqlite3.connect(dbfn)
            databasef.backup(db)
            databasef.close()
        except:
            ## error to create db
            return False
            pass

    
    def __saveDB(self, db, dbfn):
    ### DO NOT DELETE, 
    ### DO NOT MERGE into saveDataBase()
        """
        usage:
            __saveDB(self.database, self.databaseFilename)

        """
        try:
            databasef = sqlite3.connect(dbfn)
            db.backup(databasef)
            databasef.commit()
            databasef.close()
        except:
            ## error to create db
            return False
            pass


    def saveDataBase(self):
        return self.__saveDB(self.database, self.databaseFilename)


    def __tableExists(self, db, tablename):
        if ( tablename == None ) or ( db == None ):
            print("--- no names, tab:", tablename, " , db:", db)
            return False
        cur = db.cursor()
        sql = 'SELECT COUNT(*) FROM sqlite_master WHERE type = ? AND name = ?'
        cur.execute(sql, ("table", tablename,) )
        data = cur.fetchone()
        count = data[0]
        return ( count > 0 )
        
        
        
    def __initCreateTables(self):        
        self.cur = self.database.cursor()
        ## Creating tables
        try:
            self.cur.execute(''' 
                        CREATE TABLE categories (
                            cat_id INTEGER NOT NULL  PRIMARY KEY,
                            cat_name TEXT NOT NULL,
                            cat_limit FLOAT
                            );
                        ''')
            self.cur.execute('''
                        CREATE TABLE contractors (
                            cont_id INTEGER NOT NULL  PRIMARY KEY,
                            cont_name TEXT NOT NULL
                            );
                        ''')
            self.cur.execute('''
                        CREATE TABLE transactions (
                            trans_id INTEGER NOT NULL  PRIMARY KEY,
                            trans_date DATE NOT NULL,
                            trans_amount REAL NOT NULL,
                            cont_id INTEGER,
                            cat_id INTEGER,
                            CONSTRAINT contractors_cont_id_fk
                                FOREIGN KEY (cont_id)
                                REFERENCES contractors (cont_id),
                            CONSTRAINT categories_cat_id_fk
                                FOREIGN KEY (cat_id)
                                REFERENCES categories (cat_id)
                            );
                        ''')
            self.database.commit()
        except sqlite3.OperationalError as err:
            print("error creating tables")
            print(err)
        
        ### Load defaults into tables
        ## contractors
        sql = 'INSERT INTO contractors ( cont_name ) values (?)'
        self.cur.executemany(sql, self.default_contractors)
        self.database.commit()

        ## categories
        sql = 'INSERT INTO categories ( cat_name ) values (?)'
        self.cur.executemany(sql, self.default_categories)
        self.database.commit()



    def __testPrintTable(self, db, tablename):
        if self.__tableExists(db, tablename):
            cur = db.cursor()
            # print out all tables
            hello = "DEBUG: Table: " + str(tablename)
            print("\n\n", hello)
            print("-" * len(hello) )
            sql = 'SELECT * FROM ' + str(tablename)
            cur.execute(sql)
            data = cur.fetchall()
            for row in data:
                print(row)
                

                
    def testPrintAllTables(self):
        db = self.database
        hello = "Debug: printing all tables in database:"
        print(hello)
        print("=" * len(hello) )
        cur = db.cursor()
        sql = 'SELECT name FROM sqlite_master WHERE type = "table";'
        cur.execute(sql )
        data = cur.fetchall()
        print("Founded tables: ")
        print(data)
        # print out all tables
        for row in data:
            self.__testPrintTable(db, row[0] )
            

    def getAllTransactions(self):
        ## TODO: check database connection
        cur = self.database.cursor()
        sql = '''
            SELECT tr.trans_id, tr.trans_date, tr.trans_amount, ct.cat_name , cr.cont_name
            FROM transactions AS tr 
            LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
            LEFT OUTER JOIN contractors AS cr
                ON tr.cont_id = cr.cont_id
            ORDER BY tr.trans_date DESC 
            ;
            '''
        cur.execute(sql)
        data = cur.fetchall()
        return data
    
    def getTransaction_byid(self, id_value):
        ## TODO: check database connection
        cur = self.database.cursor()
        sql = '''
            SELECT tr.trans_id, tr.trans_date, tr.trans_amount, ct.cat_name , cr.cont_name
            FROM transactions AS tr 
            LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
            LEFT OUTER JOIN contractors AS cr
                ON tr.cont_id = cr.cont_id
            WHERE tr.trans_id = ?
            ;
            '''
        cur.execute(sql,(id_value,))
        data = cur.fetchall()
        return data
    
    #name!!!
    def chartMonth(self,month):
        cur = self.database.cursor()
        sql ='''
        SELECT SUM(tr.trans_amount),ct.cat_name
        FROM  transactions AS tr
        LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
        WHERE  strftime('%m',tr.trans_date) IN (?)
        GROUP BY ct.cat_name;
        '''
        cur.execute(sql,(month,))
        data = cur.fetchall()
        return data
        
    
    
    def getAllTransactionsPeriod(self,startDate, endDate):
                
        ## TODO: check database connection
        cur = self.database.cursor()
        sql = '''
        SELECT tr.trans_id, tr.trans_date, tr.trans_amount, ct.cat_name , cr.cont_name
        FROM transactions AS tr
        LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
            LEFT OUTER JOIN contractors AS cr
                ON tr.cont_id = cr.cont_id
        WHERE tr.trans_date BETWEEN ? AND ?
        ORDER BY tr.trans_date DESC
        '''
        period = (startDate, endDate,)
        cur.execute(sql,period)
        data = cur.fetchall()
        return data
        


    def getTransactionsPeriod(self, startDate, endDate, category, contractor):
    
        ## TODO: check database connection
        cur = self.database.cursor()
        sql = '''
        SELECT tr.trans_id, tr.trans_date, tr.trans_amount, ct.cat_name , cr.cont_name
        FROM transactions AS tr
        LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
            LEFT OUTER JOIN contractors AS cr
                ON tr.cont_id = cr.cont_id
        WHERE (tr.trans_date BETWEEN ? AND ?)
        AND ( ct.cat_name = ?) 
        AND ( cr.cont_name = ?)
        ORDER BY tr.trans_date DESC
        '''
        
        cur.execute(sql, (startDate, endDate, category, contractor))
        data = cur.fetchall()
        return data


    def getBalance(self):
        ## TODO: check database connection
        cur = self.database.cursor()
        sql = '''
            SELECT  SUM(tr.trans_amount)
            FROM  transactions AS tr ;
            '''
        cur.execute(sql)
        data = cur.fetchone()[0]
        data = data if data else 0.0
        return data


    def getContractorList(self):
        ## TODO: check database connection
        cur = self.database.cursor()
        sql = '''
            SELECT  cr.cont_name , cr.cont_id
            FROM  contractors AS cr
            ORDER BY cr.cont_name ASC ;
            '''
        cur.execute(sql)
        data = cur.fetchall()
        return data
        

    def getCategoriesList(self):
        ## TODO: check database connection
        cur = self.database.cursor()
        sql = '''
            SELECT  ct.cat_name , ct.cat_id
            FROM categories AS ct
            ORDER BY  ct.cat_name  ASC ;
            '''
        cur.execute(sql)
        data = cur.fetchall()
        return data
        
    
    def addTransaction(self, date, amount, category, contractor):
        
        ## TODO: 1. data types checking
        # DATETIME converting:
        #     %Y: Year (4 digits)
        #     %m: Month
        #     %d: Day of month
        #     %H: Hour (24 hour)
        #     %M: Minutes
        #     %S: Seconds
        #     %f: Microseconds

        ## TODO: 2. select category and contractor not by name, but ID
        
        if not ( isinstance(date, dt.date) ):
            return (False, "date is not datetime either date type parametr")
        if not ( isinstance(amount, float) or isinstance(amount, int) ):
            return (False, "Amount is not real either integer number")
        
        cur = self.database.cursor()
        sql= '''
                INSERT INTO transactions
                ( trans_date, trans_amount,
                  cat_id,
                  cont_id) VALUES 
                ( ?, ?,
                     (SELECT ct.cat_id FROM categories ct WHERE ct.cat_name = ? ),
                      (SELECT cont_id FROM contractors WHERE cont_name = ? )
                )
             '''   
        try:
            cur.executemany(sql, ( (date, amount, category, contractor,), ) )
            self.database.commit()
            ## print(type(date),  type(amount),  type(category),  type(contractor), sep='\t')
            return (True, "OK",)
        except sqlite3.Error:
            self.database.rollback()
            return (False, "SQL error",)
    
    def changeTransaction(self,id_value, date, amount, category, contractor):
        val = (date, amount, category, contractor, id_value)
        cur = self.database.cursor()
        sql='''UPDATE transactions
        SET
        trans_date=?, trans_amount=?,
        cont_id = (SELECT ct.cat_id FROM categories ct WHERE ct.cat_name = ? ), 
        cat_id=(SELECT cont_id FROM contractors WHERE cont_name = ? )
        WHERE trans_id = ?;
        '''
        cur.execute(sql,val)
        self.database.commit()
        
    def deleteTransaction(self,val):
        cur = self.database.cursor()
        sql= '''
            DELETE FROM transactions AS tr
            WHERE tr.trans_id = ?
            '''   
        cur.execute(sql,(val,))
        self.database.commit()
        

    def addContractor(self,  contractor):
        ## TODO: 1. data types checking
        
        cur = self.database.cursor()
        sql= '''
                INSERT INTO contractors
                ( cont_name ) VALUES 
                ( ? )
             '''   
        try:
            cur.execute(sql, ( contractor, ) )
            self.database.commit()
            return (True, "OK",)
        except sqlite3.Error:
            self.database.rollback()
            return (False, "SQL error",)


    def addCategory(self, category):
        ## TODO: 1. data types checking
        cur = self.database.cursor()
        sql= '''
                INSERT INTO categories
                (  cat_name ) VALUES 
                ( ? )
             '''   
        try:
            cur.execute(sql, ( category,) )
            self.database.commit()
            return (True, "OK",)
        except sqlite3.Error:
            self.database.rollback()
            return (False, "SQL error",)

#####
##### Some stuff for CSV import
##### DO NOT DELETE YET

"""

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
database.commit()



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
database.commit()



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
database.commit()

"""
'''
#
#================================================================
#================================================================
#  TESTING
badb = App_data()
date2 = dt.datetime.now()          
res = badb.addTransaction( 
    date2, 
    72.56,
    "Groceries",
    "K-Market")


val =[
      ("01-01-2020","Lidl","12.34","Lotto"),
      ("03-02-2020","S-Market","12.24","Rent"),
      ("05-03-2020","McDonald","10.65","Groceries"),
      ("08-04-2020","Obi","12.35","Subscribtions"),
      ("12-05-2020","S-Market","189.65","Travel"),
      ("15-06-2020","Lidl","156.32","Groceries"),
      ("19-07-2019","rent","1200.65","Rent"),
      ("20-08-2020","Lidl","126.68","Rent"),
      ("20-09-2020","K-Market","652.21","Food"),
      ("23-10-2019","S-Market","1200.65","Rent"),
      ("25-11-2020","electricity","126.68","Rent"),
      ("30-12-2020","Lidl","652.21","Rent")
      ]
 

print("\n\n\n Select all transactions and also names of category from other tables")

## Fill transactions from val list
ind_date = 0
ind_cont = 1
ind_amount = 2
ind_cat = 3
for a in val:
    res = "---"
    ## convert string date into object
    date =  dt.datetime.strptime( a[  ind_date  ] , '%d-%m-%Y')
    #data time lib - dt
    ## convert number into number
    amount = float( a[ ind_amount ] )
    res = badb.addTransaction( date , amount ,  a[ ind_cat  ] , a[ ind_cont ] )
    print(res)

   
#------------  

date2 = dt.datetime.now()          
res = badb.addTransaction( 
    date2, 
    72.56,
    "Groceries",
    "K-Market")
print(res)

    

badb.testPrintAllTables()

print("\n\n")
print("All transactions\n")
data = badb.getAllTransactions()
for row in data:
    print("A", row)

print("\n")
print("All transactions period\n")
data=badb.getAllTransactionsPeriod('2020-03-06', '2021-04-31')
for row in data:
    print("B", row)
print("\n")

print("\n")
print("All transactions period category\n")
data=badb.getTransactionsPeriod('2020-03-06', '2021-04-31', 'Groceries', 'K-Market')
for row in data:
    print("B", row)
print("\n")

data = badb.getCategoriesList()
for row in data:
    print(row)
print("\n")

data = badb.getContractorList()
for row in data:
    print(row)
 


#badb.saveDataBase()'
'''


