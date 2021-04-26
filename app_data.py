# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:53:00 2021

@author: ilia
"""

import sqlite3
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
        self.database = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
        print("Loading db")
        self.__loadDB(self.database, self.databaseFilename)
        if not self.__tableExists(self.database, "transactions"):
            print("Creating tables in database...")
            self.__initCreateTables()

        
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
                            trans_date DATETIME NOT NULL,
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
        # sql = '''
        #     SELECT tr.trans_date , tr.trans_amount , ct.cat_name, cr.cont_name
        #     FROM transactions AS tr 
        #         NATURAL JOIN contractors AS cr
        #         NATURAL JOIN categories AS ct
        #     ORDER BY tr.trans_amount DESC ;
        #     '''
        sql = '''
            SELECT tr.trans_date , tr.trans_amount, ct.cat_name , cr.cont_name
            FROM transactions AS tr 
            LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
            LEFT OUTER JOIN contractors AS cr
                ON tr.cont_id = cr.cont_id
            ORDER BY tr.trans_amount DESC 
            ;
            '''
            
        cur.execute(sql)
        data = cur.fetchall()
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
        ## TODO: 2. select category and contractor not by name, but ID
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
    # try:
        print( (date, amount, category, contractor,)  )
        cur.executemany(sql, ( (date, amount, category, contractor,), ) )
        self.database.commit()
        ## print(type(date),  type(amount),  type(category),  type(contractor), sep='\t')
        return (True, "OK",)
    # except sqlite3.Error:
        # self.database.rollback()
        # return (False, "SQL error",)
        

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
##### Some stuff
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

#
#================================================================
#================================================================
#  TESTING

val =[
      ("12-03-2019","Lidl","12.34","food"),
      ("07-03-2019","Hesburger","12.24","Rent"),
      ("12-04-2019","McDonald","10.65","food"),
      ("12-03-2019","Obi","12.35","home"),
      ("12-06-2019","Hesburger","189.65","restaurant"),
      ("12-03-2020","Lidl","156.32","food"),
      ("10-05-2019","rent","1200.65","Rent"),
      ("12-03-2020","electricity","126.68","Rent"),
      ("15-09-2019","water","652.21","Rent")
     ]


print("\n\n\n Select all transactions and also names of category from other tables")
badb = App_data()

## Fill transactions from val list
ind_date = 0
ind_cont = 1
ind_amount = 2
ind_cat = 3
for a in val:
    res = badb.addTransaction( a[  ind_date  ], a[ ind_amount ] ,
                         a[ ind_cat  ] , a[ ind_cont ] )
    print(res)
#------------            


badb.testPrintAllTables()
print("\n\n")
data = badb.getAllTransactions()
for row in data:
    print("A", row)
print("\n")

data = badb.getCategoriesList()
for row in data:
    print(row)
print("\n")

data = badb.getContractorList()
for row in data:
    print(row)
