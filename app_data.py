# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:53:00 2021

@author: ilia
"""

import sqlite3
import datetime as dt
import numpy as np
import pandas as pd


class DataBaseHandler:
    _class_counter = 0

    
    def __del__(self):
        type(self)._class_counter -= 1


    def __init__(self):
        ### self.__debug = True
        ### if type(self)._class_counter > 0:
        ###     print("One instance of class",type(self), " already exist.")
        ###     print("Only one instance is allowed.")
        ###     raise ValueError
        type(self)._class_counter += 1
        print("DataBaseHandler OBJECT #", type(self)._class_counter)

        ### self.databaseFilename = "app.database.db"
         
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
        self.database = sqlite3.connect(':memory:', 
                        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        # self.database = sqlite3.connect(self.databaseFilename, 
        #                 detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        print("Loading db")
       # self.__loadDB(self.database, self.databaseFilename)
        if not self.__tableExists("transactions"):
            print("Creating tables in db...", end='')
            self.__initCreateTables()
            print("done.")
        else:
            print("Tables are exists. Skip")



    def __tableExists(self, tablename):
        if ( tablename == None ):
            print("--- no name, tab:", tablename)
            return False
        cur = self.database.cursor()
        sql = 'SELECT COUNT(*) FROM sqlite_master WHERE type = ? AND name = ?'
        cur.execute(sql, ("table", tablename,) )
        data = cur.fetchone()
        count = data[0]
        return ( count > 0 )



    def isExistsCategory(self, name):
        name = self.__parse_name(name)
        if ( name == "" ):
            return None
        sql = 'SELECT COUNT(*) FROM categories WHERE  cat_name = ?'
        cur = self.database.cursor()
        cur.execute(sql, (name,) )
        data = cur.fetchone()
        count = data[0]
        return ( count > 0 )



    def isExistsContractor(self, name):
        name = self.__parse_name(name)
        if ( name == "" ):
            return None
        cur = self.database.cursor()
        sql = 'SELECT COUNT(*) FROM contractors WHERE  cont_name = ?'
        cur.execute(sql, (name,) )
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
                            cat_name TEXT NOT NULL COLLATE NOCASE,
                            cat_limit FLOAT,
                            cat_comment TEXT
                            );
                        ''')
            self.cur.execute('''
                        CREATE TABLE contractors (
                            cont_id INTEGER NOT NULL  PRIMARY KEY,
                            cont_name TEXT NOT NULL COLLATE NOCASE,
                            cont_limit FLOAT,
                            cont_comment TEXT
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
        ## categories
        for i in self.default_categories:
            self.addCategory( i[0] )
        ## contractors
        for i in self.default_contractors:
            self.addContractor( i[0] )
        self.database.commit()



    def __testPrintTable(self, tablename):
        if self.__tableExists(tablename):
            cur = self.database.cursor()
            # print out all tables
            hello = "DEBUG: Table: " + str(tablename)
            print("\n\n", hello)
            print("-" * len(hello) )
            sql = 'SELECT * FROM ' + str(tablename)
            cur.execute(sql)
            data = cur.fetchall()
            for row in data:
                print(row)



    def __is_date(self, dtchck):
        import datetime
        """
        Returns True if is date
        Returns False if is datetime
        Returns None if it is neither of these things
        """
        try:
            dtchck.date()
            return False
        except:
            if isinstance(dtchck, datetime.date):
                return True
        return None



    def __parse_date(self, date):
        if  self.__is_date(date) == True:
            return date
        if  self.__is_date(date) == False:
            date = date.date()
        if  self.__is_date(date) == True:
            return date
        else:            
            return None


    def __parse_name(self, name):
        if pd.isnull( name ):
            return ''
        # Remove all extra spaces
        name = " ".join(name.split())
        if name == " ":
            return ''
        else:
            return name



    def testPrintAllTables(self):
        hello = "Debug: printing all tables in database:"
        print(hello)
        print("=" * len(hello) )
        sql = 'SELECT name FROM sqlite_master WHERE type = "table";'
        cur = self.database.cursor()
        cur.execute(sql )
        data = cur.fetchall()
        print("Founded tables: ")
        print(data)
        # print out all tables
        for row in data:
            self.__testPrintTable( row[0] )



    def getAllTransactions(self):
        ## TODO: check database connection
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
        cur = self.database.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data



    def getTransaction_byid(self, id_value):
        ## TODO: check database connection
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
        cur = self.database.cursor()
        cur.execute(sql,(id_value,))
        data = cur.fetchone()
        return data



    def data_chartCategories(self,startDate,endDate):
        sql ='''
        SELECT COALESCE(SUM(tr.trans_amount),0) , 
                COALESCE(ct.cat_name,"Undefined") , 
                COALESCE(ct.cat_limit,0)
        FROM  transactions AS tr
        LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
        WHERE tr.trans_date BETWEEN ? AND ?
        AND tr.trans_amount < 0 
        GROUP BY ct.cat_name;
        '''
        cur = self.database.cursor()
        cur.execute(sql,(startDate,endDate,))
        data = cur.fetchall()
        return data



    def data_chartIncome(self,startDate,endDate):
        sql = '''
        SELECT COALESCE(SUM(tr.trans_amount),0) , tr.trans_date
        FROM transactions AS tr
        WHERE tr.trans_date BETWEEN ? AND ? 
        AND tr.trans_amount > 0
        GROUP BY tr.trans_date
        '''
        cur = self.database.cursor()
        cur.execute(sql,(startDate,endDate,))
        data = cur.fetchall()
        return data



    def data_chartOutcome(self,startDate,endDate):
        sql = '''
        SELECT COALESCE(SUM(tr.trans_amount),0) , tr.trans_date
        FROM transactions AS tr
        WHERE tr.trans_date BETWEEN ? AND ? 
        AND tr.trans_amount < 0
        GROUP BY tr.trans_date
        '''
        cur = self.database.cursor()
        cur.execute(sql,(startDate,endDate,))
        data = cur.fetchall()
        return data



    def data_chartBalance(self,startDate,endDate):
        sql = '''
        SELECT COALESCE(SUM(tr.trans_amount),0) , tr.trans_date
        FROM transactions AS tr
        WHERE tr.trans_date BETWEEN ? AND ?
        GROUP BY tr.trans_date
        '''
        cur = self.database.cursor()
        cur.execute(sql,(startDate,endDate,))
        data = cur.fetchall()
        return data



    def getAllTransactionsPeriod(self,startDate, endDate):
                
        ## TODO: check database connection
        sql = '''
        SELECT tr.trans_id, tr.trans_date, tr.trans_amount, ct.cat_name , cr.cont_name
        FROM transactions AS tr
        LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
            LEFT OUTER JOIN contractors AS cr
                ON tr.cont_id = cr.cont_id
        WHERE tr.trans_date BETWEEN ? AND ?
        ORDER BY tr.trans_date DESC , tr.trans_id DESC
        '''
        cur = self.database.cursor()
        period = (startDate, endDate,)
        cur.execute(sql,period)
        data = cur.fetchall()
        return data



    def getTransactionsPeriod(self, startDate, endDate, category, contractor):
    
        ## TODO: check database connection
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
        
        cur = self.database.cursor()
        cur.execute(sql, (startDate, endDate, category, contractor))
        data = cur.fetchall()
        return data


    def getBalance(self, start,end):
        ## TODO: check database connection
        sql = '''
            SELECT  COALESCE(SUM(tr.trans_amount),0)
            FROM  transactions AS tr
            WHERE tr.trans_date BETWEEN ? AND ?;
            '''

        cur = self.database.cursor()
        cur.execute(sql,(start, end,))
        data = cur.fetchone()[0]
        data = data if data else 0.0
        return data


    def getAmountIn(self, start, end):
        cur = self.database.cursor()
        sql = '''
            SELECT  COALESCE(SUM(tr.trans_amount),0)
            FROM  transactions AS tr 
            WHERE tr.trans_amount > 0
            AND tr.trans_date BETWEEN ? AND ?;
            '''
        cur.execute(sql, (start,end,))
        data = cur.fetchone()[0]
        data = data if data else 0.0
        return data
    
    
    def getAmountOut(self, start, end):
        cur = self.database.cursor()
        sql = '''
            SELECT  COALESCE(SUM(tr.trans_amount),0)
            FROM  transactions AS tr 
            WHERE tr.trans_amount < 0
            AND tr.trans_date BETWEEN ? AND ?;
            '''
        cur.execute(sql, (start,end,))
        data = cur.fetchone()[0]
        data = data if data else 0.0
        return data


    def getContractorList(self):
        ## TODO: check database connection
        sql = '''
            SELECT  cr.cont_name , cr.cont_id, cr.cont_limit, cr.cont_comment
            FROM  contractors AS cr
            ORDER BY cr.cont_name ASC ;
            '''
        cur = self.database.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data



    def getCategoriesList(self):
        ## TODO: check database connection
        sql = '''
            SELECT  ct.cat_name , ct.cat_id, ct.cat_limit, cat_comment
            FROM categories AS ct
            ORDER BY  ct.cat_name  ASC ;
            '''
        cur = self.database.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data

    
    def getCategoriesLimit(self, start, end):
        ## TODO: check database connection
        sql = '''
        SELECT  ct.cat_name , ct.cat_limit
        FROM transactions AS tr
        LEFT OUTER JOIN categories AS ct
                ON tr.cat_id = ct.cat_id
        WHERE tr.trans_date BETWEEN ? AND ?
        AND ct.cat_limit > 0
        GROUP BY ct.cat_name ;
        '''
        cur = self.database.cursor()
        cur.execute(sql, (start, end,))
        data = cur.fetchall()
        return data


    def addTransaction(self, date, amount, category, contractor):
        date = self.__parse_date(date)
        category = self.__parse_name(category)
        contractor = self.__parse_name(contractor)
        if  self.__is_date(date) != True:
            return (False, "date is not datetime either date type parametr")
        if not ( isinstance(amount, float) or isinstance(amount, int) ):
            return (False, "Amount is not real either integer number")
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
            cur = self.database.cursor()
            cur.executemany(sql, ( (date, amount, category, contractor,), ) )
            self.database.commit()
            ## print(type(date),  type(amount),  type(category),  type(contractor), sep='\t')
            return (True, "OK",)
        except sqlite3.Error as err:
            self.database.rollback()
            return (False, "SQL error: %s"% err,)



    def changeTransaction(self, id_value, date, amount, category, contractor):
        date = self.__parse_date(date)
        category = self.__parse_name(category)
        contractor = self.__parse_name(contractor)
        if  self.__is_date(date) != True:
            return (False, "date is not datetime either date type parametr")
        if not ( isinstance(amount, float) or isinstance(amount, int) ):
            return (False, "Amount is not real either integer number")
        
        sql='''UPDATE transactions
        SET
        trans_date=?, trans_amount=?,
        cont_id = (SELECT contractors.cont_id 
                   FROM contractors WHERE contractors.cont_name = ? ), 
        cat_id= (SELECT categories.cat_id
                 FROM categories WHERE categories.cat_name = ? )
        WHERE trans_id = ?;
        '''
        val = (date, amount, contractor, category, id_value)
        try:
            cur = self.database.cursor()
            cur.execute(sql,val)
            self.database.commit()
            return (True, "OK",)
        except sqlite3.Error as err:
            self.database.rollback()
            return (False, "SQL error: %s"% err,)



    def deleteTransaction(self, id_value):
        sql= '''
            DELETE FROM transactions AS tr
            WHERE tr.trans_id = ?
            '''   
        cur = self.database.cursor()
        cur.execute(sql, (id_value,))
        self.database.commit()



    def addContractor(self,  contractor, limit=0.0, comment=''):
        ## TODO: 1. data types checking
        contractor = self.__parse_name(contractor)
        if contractor == '':
            return (False, 'Empty contractor name')
        sql= '''
                INSERT INTO contractors
                ( cont_name, cont_limit, cont_comment ) VALUES 
                ( ? ,? , ? )
             '''   
        val = ( contractor, limit, comment )
        try:
            cur = self.database.cursor()
            cur.execute(sql, val )
            self.database.commit()
            return (True, "OK",)
        except sqlite3.Error:
            self.database.rollback()
            return (False, "SQL error",)


    def getContractor_byId(self, id_contractor):
        ## TODO: check database connection
        sql = '''
            SELECT cn.cont_name, cn.cont_id, cn.cont_limit, cn.cont_comment
            FROM contractors AS cn
            WHERE cn.cont_id = ?;
            '''
        cur = self.database.cursor()
        cur.execute(sql,(id_contractor,))
        data = cur.fetchone()
        return data 



    def changeContractor(self, id_value, contractor, limit=0.0, comment=''):
        contractor = self.__parse_name(contractor)
        if contractor == '':
            return (False, 'Empty contractor name')
        sql='''
        UPDATE contractors
        SET cont_name = ?,
            cont_limit = ?,
            cont_comment = ?
        WHERE cont_id = ?;
        '''
        val = (contractor, limit, comment,    id_value)
        try:
            cur = self.database.cursor()
            cur.execute(sql,val)
            self.database.commit()
            return (True, "OK",)
        except sqlite3.Error as err:
            self.database.rollback()
            return (False, "SQL error: %s"% err,)



    def addCategory(self, category, limit=0.0, comment=''):
        category = self.__parse_name(category)
        if category == '':
            return (False, 'Empty category name')
        ## TODO: 1. data types checking
        sql= '''
                INSERT INTO categories
                (  cat_name, cat_limit, cat_comment ) VALUES 
                ( ? ,? , ? )
             '''
        val = ( category, limit, comment, )
        try:
            cur = self.database.cursor()
            cur.execute(sql, val )
            self.database.commit()
            return (True, "OK",)
        except sqlite3.Error:
            self.database.rollback()
            return (False, "SQL error",)



    def getCategory_byId(self, id_category):
        ## TODO: check database connection
        sql = '''
            SELECT ct.cat_name, ct.cat_id, ct.cat_limit, ct.cat_comment
            FROM categories AS ct
            WHERE ct.cat_id = ?;
            '''
        cur = self.database.cursor()
        cur.execute(sql,(id_category,))
        data = cur.fetchone()
        return data 



    def changeCategory(self, id_value, category, limit=0.0, comment=''):
        category = self.__parse_name(category)
        if category == '':
            return (False, 'Empty category name')

        sql='''
        UPDATE categories
        SET cat_name = ?,
            cat_limit = ?,
            cat_comment = ?
        WHERE cat_id = ?;
        '''
        val = (category, limit, comment,   id_value)
        try:
            cur = self.database.cursor()
            cur.execute(sql,val)
            self.database.commit()
            return (True, "OK",)
        except sqlite3.Error as err:
            self.database.rollback()
            return (False, "SQL error: %s"% err,)

