# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:53:00 2021

@author: ilia
"""

import sqlite3
import bcrypt
from app_data import App_data
import tempfile
import os
import zlib
import base64

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
        
        ### Database filename
        self.__usersDatabaseFilename = 'users.database.db'
         
        
        ### Open connection immideally when running
        ### if no database exist, create it
        print("Loading users database..")
        self.usersDatabase = sqlite3.connect( self.__usersDatabaseFilename )
        if not self.__tableExists("users"):
            print("Creating tables in database...")
            self.__initCreateTables()
        else:
            print("Tables in database are exists.")
            
        ### Current user name
        self.__currentUser = ''
        
        ### Transaction database instance
        
        

    def __initCreateTables(self):        
        cur = self.usersDatabase.cursor()
        ## Creating tables
        try:
            cur.execute('''
                        CREATE TABLE users (
                            id INTEGER NOT NULL  PRIMARY KEY,
                            login TEXT NOT NULL COLLATE NOCASE,
                            passhash TEXT,
                            openkey TEXT,
                            data BLOB
                            );
                        ''')
            self.usersDatabase.commit()
        except sqlite3.OperationalError as err:
            print("error creating tables")
            print(err)
        finally:
            cur.close()



    def __tableExists(self, tablename):
        if ( tablename == None ):
            print("--- no name, tab:", tablename)
            return False
        
        sql = '''SELECT COUNT(*) FROM sqlite_master WHERE type = ? AND name = ?'''
        cur = self.usersDatabase.cursor()
        cur.execute(sql, ("table", tablename,) )
        data = cur.fetchone()
        cur.close()
        count = data[0]
        return ( count > 0 )
        


    def __parse_username(self, name):
        if pd.isnull( name ):
            return ''
        name = str(name)
        return name


    def __getUserPasshash(self, username):
        username = self.__parse_username(username)
        if ( username == '' ):
            return ''
        
        sql = '''
            SELECT  us.passhash
            FROM  users AS us
            WHERE us.login = ? ;
            '''
        cur = self.usersDatabase.cursor()
        cur.execute(sql, (username,) )
        data = cur.fetchone()[0]
        cur.close()
        return data
        
        


    def isExistsUser(self, name):
        name = self.__parse_username(name)
        if ( name == '' ):
            return None
        
        sql = '''SELECT COUNT(*) FROM users WHERE  login = ?'''
        cur = self.usersDatabase.cursor()
        cur.execute(sql, (name,) )
        data = cur.fetchone()
        cur.close()
        count = data[0]
        return ( count > 0 )
        
        

    def __testPrintTable(self, tablename):
        if self.__tableExists(tablename):
            # print out all tables
            hello = "DEBUG: Table: " + str(tablename)
            print("\n\n", hello)
            print("-" * len(hello) )
            
            sql = 'SELECT * FROM ' + str(tablename)
            cur = self.usersDatabase.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            for row in data:
                print(row)



    def testPrintAllTables(self):
        hello = "Debug: printing all tables in database:"
        print(hello)
        print("=" * len(hello) )
        sql = '''SELECT name FROM sqlite_master WHERE type = "table";'''
        cur = self.usersDatabase.cursor()
        cur.execute(sql )
        data = cur.fetchall()
        cur.close()
        print("Founded tables: ")
        print(data)
        # print out all tables
        for row in data:
            self.__testPrintTable(row[0] )



    def getUsersList(self):
        ## TODO: check database connection
        sql = '''
            SELECT  us.login , us.id
            FROM  users AS us
            ORDER BY us.login ASC ;
            '''
        cur = self.usersDatabase.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data


    def addUser(self, username, password):
        ## Check username
        username = self.__parse_username(username)
        if ( username == '' ):
            return (False, 'Empty user name')
        if self.isExistsUser(username) == True:
            return (False, 'User already exists')
        ## Check password
        if ( password == '' ):
            return (False, 'Empty password')
        ## Encrypt password
        passhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        sql= '''
                INSERT INTO users
                ( login, passhash ) VALUES
                ( ? , ? ) ;
             '''   
        try:
            cur = self.usersDatabase.cursor()
            cur.execute(sql, (username, passhash, ) )
            self.usersDatabase.commit()
            cur.close()
            return (True, "OK",)
        except sqlite3.Error as err:
            self.usersDatabase.rollback()
            cur.close()
            return (False, "UserSQL error: %s"% err,)


    def getCurrentUser(self):
        return self.__currentUser
        ### ======


    def __isPasswordCorrect(self, username, password):
        username = self.__parse_username(username)
        if ( username == '' ):
            return False
        if ( password == '' ):
            return False
        if self.isExistsUser(username) != True:
            return False
        hashAndSalt = self.__getUserPasshash(username)
        passvalid = bcrypt.checkpw(password.encode(), hashAndSalt)
        # print ("pwdcheck result:", passvalid)
        return passvalid

        

    def loginUser(self, username, password):
        self.logoutCurrentUser()

        username = self.__parse_username(username)
        print('Login attempt, username:"', username,'"', sep='')
        if ( username == '' ):
            return (False, 'Empty user name')
        if ( password == '' ):
            return (False, 'Empty password')
        if self.isExistsUser(username) != True:
            return (False, 'User do not exists')
        
        print("login: pass check...", end='')
        passcheck = self.__isPasswordCorrect(username, password)
        if passcheck == False:
            print("incorrect password!")
            return (False, 'Incorrect password')
        
        if passcheck == True:
            print("OK")
            self.__currentUser = username
            ### Do real stuff
            ### load transaction database and so on...
            pass
            return (True, 'OK')
        else:
            print("problem!!!")
            return (False, 'Some problem')



    def logoutCurrentUser(self):
        if self.__currentUser != '':
            ## ***
            # TODO: close transactions database
            pass
        self.__currentUser = ''



    def writeStuff(self, data):
        if self.__currentUser == '':
            return (False, 'No user logged in')
        
        sql= '''
                UPDATE  users
                SET openkey = ?
                WHERE login = ?;
             '''   
        try:
            cur = self.usersDatabase.cursor()
            cur.execute(sql, (data, self.__currentUser, ) )
            self.usersDatabase.commit()
            cur.close()
            return (True, "OK",)
        except sqlite3.Error as err:
            cur.close()
            return (False, "UserSQL stuff error: %s"% err,)

        
    def saveTransactionDB(self, db):
        if self.__currentUser == '':
            return (False, 'No user logged in')
        
        tempfn = os.path.join(tempfile.gettempdir(), os.urandom(32).hex())
        ## dump transaction DB
        try:
            databaseInFile = sqlite3.connect( tempfn )
            self.database.backup(databaseInFile)
            databaseInFile.commit()
            databaseInFile.close()
        except sqlite3.Error as err:
            ## error to create db
            print("SAVE DB ERROR")
            return (False, "UserSQL save error: %s"% err,)
            pass
        
        with open(tempfn, 'rb') as file:
            blobData = file.read()
        os.remove(tempfn)
        blobData = zlib.compress(blobData)
        
        sql= '''
                UPDATE  users
                SET data = ?
                WHERE login = ?;
             '''   
        try:
            cur = self.usersDatabase.cursor()
            cur.execute(sql, ( blobData, self.__currentUser, ) )
            self.usersDatabase.commit()
            cur.close()
            return (True, "OK",)
        except sqlite3.Error as err:
            cur.close()
            return (False, "UserSQL stuff error: %s"% err,)
        
        

    def loadTransactionDB(self):
        if self.__currentUser == '':
            return (False, 'No user logged in')
        
        sql= '''
                SELECT data
                FROM users
                WHERE login = ?;
             '''   
        try:
            cur = self.usersDatabase.cursor()
            cur.execute(sql, ( self.__currentUser, ) )
            blobData = cur.fetchone()[0]
            cur.close()
        except sqlite3.Error as err:
            cur.close()
            return (False, "UserSQL stuff error: %s"% err,)
        
        tempfn = os.path.join(tempfile.gettempdir(), os.urandom(32).hex())
        with open(tempfn, 'wb') as file:
             file.write(blobData)
        os.remove(tempfn)
        blobData = zlib.decompress(blobData)
        
        try:
            databaseInFile = sqlite3.connect(tempfn)
            databaseInFile.backup(self.database)
            databaseInFile.close()
        except:
            ## error to create db
            print("LOAD DB ERROR")
            return False
            pass



#
#================================================================
#================================================================
#  TESTING
userdb = UsersHandler()
emptydb = App_data()


val =[
      ("user_01","password_01","stuff_01"),
      ("user_03","password_03","stuff_03"),
      ("user_07","password_07","stuff_07"),
      ("","","")
      ]
 


## Fill values from val list
ind_user = 0
ind_pass = 1
ind_stuf = 2

# for a in val:
#     res = "---"
#     ## convert string date into object
#     print("trying to add", a[ ind_user ] , a[ ind_pass ])
#     res = userdb.addUser(   a[ ind_user ] , a[ ind_pass ] )
#     print(res)
#     userdb.loginUser(   a[ ind_user ] , a[ ind_pass ]  )
#     res = userdb.writeStuff( a[ ind_stuf ])
#     print("Write", res)

   
#------------  

res = userdb.loginUser("user_07", "password_07")
print (res)

userdb.saveTransactionDB(emptydb)    

userdb.testPrintAllTables()

print("\n\n")
print("User list\n")
data = userdb.getUsersList()
for row in data:
    print("Ul:", row)

# res = userdb.loginUser("user_07", "password_07")
# print (res)

userdb.saveDataBase()
