# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:53:00 2021

@author: ilia
"""

import sqlite3
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class UsersHandler:
    _class_counter = 0
    
            
    def __init__(self):
        self.__debug = True
        if type(self)._class_counter > 0:
            print("One instance of class",type(self), " already exist.")
            print("Only one instance is allowed.")
            raise ValueError
            
        type(self)._class_counter += 1
        self.usersDatabaseFilename = "users.database.db"
         
        
        ### Open connection immideally when running
        ### if no database exist, create it
        self.usersDatabase = sqlite3.connect(":memory:")
        # self.usersDatabase = sqlite3.connect(self.usersDatabaseFilename, 
        #                 detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        print("Loading db")
        self.__loadDB(self.usersDatabase, self.usersDatabaseFilename)
        if not self.__tableExists("users"):
            print("Creating tables in database...")
            self.__initCreateTables()
        else:
            print("Tables are exists. Skip")

        
    def __loadDB(self, db, dbfn):
        try:
            databaseInFile = sqlite3.connect(dbfn)
            databaseInFile.backup(db)
            databaseInFile.close()
        except:
            ## error to create db
            return False
            pass

    
    def __saveDB(self, db, dbfn):
    ### DO NOT DELETE, 
    ### DO NOT MERGE into saveDataBase()
        """
        usage:
            __saveDB(self.usersDatabase, self.usersDatabaseFilename)

        """
        try:
            databaseInFile = sqlite3.connect(dbfn)
            db.backup(databaseInFile)
            databaseInFile.commit()
            databaseInFile.close()
        except:
            ## error to create db
            return False
            pass


    def saveDataBase(self):
        return self.__saveDB(self.usersDatabase, self.usersDatabaseFilename)


    def __tableExists(self, tablename):
        if ( tablename == None ):
            print("--- no name, tab:", tablename)
            return False
        cur = self.usersDatabase.cursor()
        sql = 'SELECT COUNT(*) FROM sqlite_master WHERE type = ? AND name = ?'
        cur.execute(sql, ("table", tablename,) )
        data = cur.fetchone()
        count = data[0]
        return ( count > 0 )
        
        
        
        

    def __initCreateTables(self):        
        self.cur = self.usersDatabase.cursor()
        ## Creating tables
        try:
            self.cur.execute('''
                        CREATE TABLE databases (
                            db_id INTEGER NOT NULL  PRIMARY KEY,
                            data BLOB
                            );
                        ''')
            self.cur.execute('''
                        CREATE TABLE users (
                            id INTEGER NOT NULL  PRIMARY KEY,
                            login TEXT NOT NULL COLLATE NOCASE,
                            passhash TEXT,
                            db_id INTEGER,
                            CONSTRAINT databases_id_fk
                                FOREIGN KEY (db_id)
                                REFERENCES databases (db_id)
                            );
                        ''')
            self.usersDatabase.commit()
        except sqlite3.OperationalError as err:
            print("error creating tables")
            print(err)
        



    def isExistsUser(self, name):
        print('us exsts 1:  "', name, '"', sep='')
        name = self.__parse_name(name)
        print('us exsts 2:  "', name, '"', sep='')
        if ( name == '' ):
            print('us exsts 3:  none')
            return None
        cur = self.usersDatabase.cursor()
        sql = 'SELECT COUNT(*) FROM users WHERE  login = ?'
        cur.execute(sql, (name,) )
        data = cur.fetchone()
        count = data[0]
        return ( count > 0 )
        
        

    def __testPrintTable(self, tablename):
        if self.__tableExists(tablename):
            cur = self.usersDatabase.cursor()
            # print out all tables
            hello = "DEBUG: Table: " + str(tablename)
            print("\n\n", hello)
            print("-" * len(hello) )
            sql = 'SELECT * FROM ' + str(tablename)
            cur.execute(sql)
            data = cur.fetchall()
            for row in data:
                print(row)


    def __parse_name(self, name):
        if pd.isnull( name ):
            return ''
        name = str(name)
        # Remove all spaces
        return "".join(name.split())

                
    def testPrintAllTables(self):
        hello = "Debug: printing all tables in database:"
        print(hello)
        print("=" * len(hello) )
        cur = self.usersDatabase.cursor()
        sql = 'SELECT name FROM sqlite_master WHERE type = "table";'
        cur.execute(sql )
        data = cur.fetchall()
        print("Founded tables: ")
        print(data)
        # print out all tables
        for row in data:
            self.__testPrintTable(row[0] )
            


    def getUsersList(self):
        ## TODO: check database connection
        cur = self.usersDatabase.cursor()
        sql = '''
            SELECT  us.login , us.id
            FROM  users AS us
            ORDER BY us.login ASC ;
            '''
        cur.execute(sql)
        data = cur.fetchall()
        return data
        
        
    
    def addUser(self, userName, password):
        userName = self.__parse_name(userName)
        if ( userName == '' ):
            return (False, 'Empty user name')
        if self.isExistsUser(userName) == True:
            return (False, 'User already exists')
        cur = self.usersDatabase.cursor()
        sql= '''
                INSERT INTO users
                ( login, passhash ) VALUES
                ( ? , ? ) ;
             '''   
        try:
            cur.execute(sql, (userName, password, ) )
            self.usersDatabase.commit()
            return (True, "OK",)
        except sqlite3.Error as err:
            self.usersDatabase.rollback()
            return (False, "SQL error: %s"% err,)



#
#================================================================
#================================================================
#  TESTING
userdb = UsersHandler()


val =[
      ("user_01","password_01"),
      ("",""),
      ("user_03","password_03"),
      ("",""),
      ("",""),
      ("",""),
      ("user_07","password_07"),
      ("",""),
      ("",""),
      ("",""),
      ("",""),
      ("","")
      ]
 

print("\n\n\n Select all transactions and also names of category from other tables")

## Fill transactions from val list
ind_user = 0
ind_pass = 1

for a in val:
    res = "---"
    ## convert string date into object
    print("trying to add", a[ ind_user ] , a[ ind_pass ])
    res = userdb.addUser(   a[ ind_user ] , a[ ind_pass ] )
    print(res)

   
#------------  

    

userdb.testPrintAllTables()

print("\n\n")
print("User list\n")
data = userdb.getUsersList()
for row in data:
    print("Ul:", row)


userdb.saveDataBase()