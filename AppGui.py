# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 13:15:25 2021

@author: kasia
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkcalendar as tkcal
import time
import datetime as dt
from app_data import App_data 
from addTransaction import AddTransaction 

## both format should match
_dt_datefmt = "%d.%m.%Y"
_cal_datefmt = "dd.mm.yyyy"

#######################################3

class LoginWin:
    def __init__(self, master=None):
        
        # build ui
        if master == None:
            self.root_login = tk.Tk()
        else:
            self.root_login = tk.Toplevel(master)
            
        ## Hide window 
        ## DO NOT forget to show at the end of init!!!
        self.root_login.withdraw()     
            
        self.ntb_Login = ttk.Notebook(self.root_login)
        
        #LOG IN TAB
        self.frm_login = ttk.Frame(self.ntb_Login)
        self.lbfr_login = ttk.Labelframe(self.frm_login)
        self.lbl_selectUser = ttk.Label(self.lbfr_login)
        self.lbl_selectUser.configure(text='Select user')
        self.lbl_selectUser.grid(column='0', row='0', sticky='s')
        self.lbl_selectUser.master.rowconfigure('0', pad='20', weight='0')
        self.lbl_selectUser.master.columnconfigure('0', pad='0', weight='1')
        self.cmb_UserLogin = ttk.Combobox(self.lbfr_login, 
                                          state="readonly")
        self.cmb_UserLogin.configure(width='20')
        self.cmb_UserLogin.grid(column='0', pady='10', row='1')
        self.cmb_UserLogin.master.columnconfigure('0', pad='0', weight='1')
        self.lbl_PasswordLogin = ttk.Label(self.lbfr_login)
        self.lbl_PasswordLogin.configure(text='Enter password')
        self.lbl_PasswordLogin.grid(column='0', row='2', sticky='s')
        self.lbl_PasswordLogin.master.rowconfigure('2', pad='15')
        self.lbl_PasswordLogin.master.columnconfigure('0', pad='0', weight='1')
        self.txt_PasswordLogin = ttk.Entry(self.lbfr_login)
        self.txt_PasswordLogin.configure(show='*', width='20')
        self.txt_PasswordLogin.grid(column='0', pady='10', row='3')
        self.txt_PasswordLogin.master.columnconfigure('0', pad='0', weight='1')
        self.btn_Login = ttk.Button(self.lbfr_login, 
                                    command = self.cb_Login)
        self.btn_Login.configure(text='LOG IN', width='15')
        self.btn_Login.grid(column='0', pady='20', row='4')
        self.btn_Login.master.columnconfigure('0', pad='0', weight='1')
        self.lbfr_login.configure(height='0', text='Please log in below', width='0')
        self.lbfr_login.grid(column='0', ipady='30', padx='40', pady='40', row='0', sticky='nsew')
        self.lbfr_login.master.rowconfigure('0', pad='10', weight='1')
        self.lbfr_login.master.columnconfigure('0', pad='20', weight='1')
        self.frm_login.configure(height='0', width='0')
        self.frm_login.grid(column='0', row='0', sticky='nsew')
        self.frm_login.master.rowconfigure('0', weight='1')
        self.frm_login.master.columnconfigure('0', weight='1')
        self.ntb_Login.add(self.frm_login, state='hidden', sticky='nsew', text='log in')        
        
        
        # ADD USER TAB
        self.frm_addUser = ttk.Frame(self.ntb_Login)
        self.lbfr_addUser = ttk.Labelframe(self.frm_addUser)
        self.lbl_InfoAddUser = ttk.Label(self.lbfr_addUser)
        self.lbl_InfoAddUser.configure(justify='center', text='Please, enter new user name\n and type your password two times')
        self.lbl_InfoAddUser.grid(column='0', columnspan='2', pady='15', row='0')
        self.lbl_InfoAddUser.master.rowconfigure('0', pad='0')
        self.lbl_InfoAddUser.master.columnconfigure('0', pad='10')
        self.lbl_usernameAddUser = ttk.Label(self.lbfr_addUser)
        self.lbl_usernameAddUser.configure(text='Username')
        self.lbl_usernameAddUser.grid(column='0', padx='11', pady='10', row='1', sticky='e')
        self.lbl_usernameAddUser.master.rowconfigure('1', pad='10')
        self.lbl_usernameAddUser.master.columnconfigure('0', pad='10')
        self.txt_usernameAddUser = ttk.Entry(self.lbfr_addUser)
        self.txt_usernameAddUser.grid(column='1', row='1', sticky='w')
        self.txt_usernameAddUser.master.rowconfigure('1', pad='10')
        self.txt_usernameAddUser.master.columnconfigure('1', pad='11', weight='1')
        self.lbl_PasswordAdd = ttk.Label(self.lbfr_addUser)
        self.lbl_PasswordAdd.configure(text='Password')
        self.lbl_PasswordAdd.grid(column='0', padx='11', pady='5', row='2', sticky='e')
        self.lbl_PasswordAdd.master.rowconfigure('2', pad='5')
        self.lbl_PasswordAdd.master.columnconfigure('0', pad='10')
        self.txt_passwordAdd = ttk.Entry(self.lbfr_addUser)
        self.txt_passwordAdd.configure(show='*')
        self.txt_passwordAdd.grid(column='1', row='2', sticky='w')
        self.txt_passwordAdd.master.rowconfigure('2', pad='5')
        self.txt_passwordAdd.master.columnconfigure('1', pad='11', weight='1')
        self.lbl_PasswordConfAdd = ttk.Label(self.lbfr_addUser)
        self.lbl_PasswordConfAdd.configure(text='Confirm password')
        self.lbl_PasswordConfAdd.grid(column='0', padx='11', pady='5', row='3', sticky='e')
        self.lbl_PasswordConfAdd.master.rowconfigure('3', pad='5')
        self.lbl_PasswordConfAdd.master.columnconfigure('0', pad='10')
        self.txt_passwordConfAdd = ttk.Entry(self.lbfr_addUser)
        self.txt_passwordConfAdd.configure(show='*')
        self.txt_passwordConfAdd.grid(column='1', row='3', sticky='w')
        self.txt_passwordConfAdd.master.rowconfigure('3', pad='5')
        self.txt_passwordConfAdd.master.columnconfigure('1', pad='11', weight='1')
        self.btn_submitAdd = ttk.Button(self.lbfr_addUser, 
                                        command = self.cb_CreateUser)
        self.btn_submitAdd.configure(text='SUBMIT', width='15')
        self.btn_submitAdd.grid(column='0', columnspan='2', ipadx='10', ipady='5', padx='10', pady='15', row='4')
        self.btn_submitAdd.master.columnconfigure('0', pad='10')
        self.lbl_resultAdduser = ttk.Label(self.lbfr_addUser)
        self.var_AddUserResult = tk.StringVar(value='Enter username, password and press Submit button')
        self.lbl_resultAdduser.configure(textvariable=self.var_AddUserResult)
        self.lbl_resultAdduser.grid(column='0', columnspan='2', row='5')
        self.lbl_resultAdduser.master.columnconfigure('0', pad='10')
        self.lbfr_addUser.configure(height='0', text='Please enter the details below', width='0')
        self.lbfr_addUser.grid(column='0', ipady='30', padx='40', pady='40', row='0', sticky='nsew')
        self.lbfr_addUser.master.rowconfigure('0', weight='1')
        self.lbfr_addUser.master.columnconfigure('0', weight='1')
        self.frm_addUser.configure(height='0', width='0')
        self.frm_addUser.grid(column='0', row='0', sticky='nsew')
        self.frm_addUser.master.rowconfigure('0', weight='1')
        self.frm_addUser.master.columnconfigure('0', weight='1')
        self.ntb_Login.add(self.frm_addUser, sticky='nsew', text='add user')
        
        ## Window settings
        self.ntb_Login.configure(width='400')
        self.ntb_Login.grid(column='0', padx='3', pady='3', row='0', sticky='nsew')
        self.ntb_Login.master.rowconfigure('0', minsize='0', weight='1')
        self.ntb_Login.master.columnconfigure('0', minsize='0', weight='1')
        self.root_login.configure(height='150', takefocus=False, width='400')
        self.root_login.resizable(False, False)

        ## Style correcting for tab's well-view
        style = ttk.Style()                     
        current_theme =style.theme_use()
        style.theme_settings(current_theme, 
                {"TNotebook.Tab": {"configure": {"padding": [95, 5]}}})

        # SHOW window, fully constructed
        self.root_login.deiconify()
    
        # Main widget
        self.loginWindow = self.root_login
        self.loginWindow.title("Login")

    def run(self):
        self.loginWindow.grab_set()
        self.loginWindow.mainloop()


    def cb_CreateUser(self):
        """
        Create user callback

        Returns
        -------
        None.

        """

        if not self.txt_usernameAddUser.get():
            self.lbl_usernameAddUser.config(foreground="red")
            self.var_AddUserResult.set(value="User name cannot be empty")
            return False
        else:
            self.lbl_usernameAddUser.configure(foreground="black")
        
        if not self.txt_passwordAdd.get():
            self.lbl_PasswordAdd.config(foreground="red")
            self.var_AddUserResult.set(value="Password cannot be empty")
            return False
        else:
            self.lbl_PasswordAdd.configure(foreground="black")
        
        if not (self.txt_passwordAdd.get() == self.txt_passwordConfAdd.get()):
            self.lbl_PasswordAdd.config(foreground="red")
            self.lbl_PasswordConfAdd.config(foreground="red")
            self.var_AddUserResult.set(value="Passwords are not match")
            return False
        else:
            self.lbl_PasswordAdd.configure(foreground="black")
            self.lbl_PasswordConfAdd.configure(foreground="black")
        ## TODO: call UserCreate()
        self.var_AddUserResult.set(value="Creating user...")
        pass
    
    
    def cb_Login(self):
        """
        Create user callback

        Returns
        -------
        None.

        """
        if  self.cmb_UserLogin.current() < 0:
            self.lbl_selectUser.config(foreground="red")
            return False
        else:
            self.lbl_selectUser.configure(foreground="black")

        if not self.txt_PasswordLogin.get():
            self.lbl_PasswordLogin.config(foreground="red")
            return False
        else:
            self.lbl_PasswordLogin.configure(foreground="black")
        
        ## TODO: call UserLogin() 
        pass

class AppWin:
    def __init__(self, master=None):
        # build ui
        self.root_app = tk.Tk() if master is None else tk.Toplevel(master)
        ## Hide window 
        ## DO NOT forget to show at the end of init!!!
        self.root_app.withdraw()     
        
        ### Notebook 
        self.ntb_app = ttk.Notebook(self.root_app)
        
        ### Account tab
        self.frm_account = ttk.Frame(self.ntb_app)
        self.lbfr_account = ttk.Labelframe(self.frm_account)
        self.lbl_balance = ttk.Label(self.lbfr_account)
        self.lbl_balance.configure(text='Balance:')
        self.lbl_balance.grid(column='0', padx='10', pady='5', row='0')
        self.lbl_percentage = ttk.Label(self.lbfr_account)
        self.var_CurrentBalance = tk.StringVar(value="...")
        self.lbl_percentage.configure(textvariable=self.var_CurrentBalance)
        self.lbl_percentage.grid(column='1', row='0')
        self.progressbar = ttk.Progressbar(self.lbfr_account)
        self.progressbar.configure(orient='horizontal')
        self.progressbar.grid(column='2', padx='30', row='0', sticky='ew')
        self.progressbar.master.columnconfigure('2', weight=1)
        self.lbfr_account.configure( text='Your account in summary')
        self.lbfr_account.grid(column='0', ipady='5', padx='10', pady='0', row='0', sticky='sew')
        self.lbfr_account.master.rowconfigure('0', pad='10', weight=0)
        self.lbfr_account.master.columnconfigure('0', weight=1)
        self.lbfr_account.master.columnconfigure('1', weight=0)
        self.lbfr_Acc_Chart = ttk.Labelframe(self.frm_account)
        #self.lbfr_Acc_Chart.configure(height='200', width='200')
        self.lbfr_Acc_Chart.grid(column='0', ipadx='10', ipady='10', row='1', sticky='nsew')
        self.lbfr_Acc_Chart.master.rowconfigure('1', weight=1)
        self.lbfr_Acc_Chart.master.columnconfigure('0', weight=1)
        self.lbfr_Acc_Chart.master.columnconfigure('1', weight=0)
        #self.frm_account.configure(height='200', width='200')
        self.frm_account.grid(column='0', row='0', sticky='nsew')
        self.frm_account.master.rowconfigure('0', weight=1)
        self.frm_account.master.columnconfigure('0', weight=1)
        self.ntb_app.add(self.frm_account, sticky='nsew', text='Account')
        
        
        ### Transactions tab
        self.frm_transactions = ttk.Frame(self.ntb_app)
        self.lbfr_drTransactions = ttk.Labelframe(self.frm_transactions)
        self.lbl_trFrom = ttk.Label(self.lbfr_drTransactions)
        self.lbl_trFrom.configure(text='From:')
        self.lbl_trFrom.grid(column='0', padx='10', row='0', sticky='e')
        self.lbl_trFrom.master.rowconfigure('0', pad='10')
        self.lbl_trFrom.master.columnconfigure('0', pad='10')
        self.cal_tr_From = tkcal.DateEntry(self.lbfr_drTransactions, 
                                           date_pattern=_cal_datefmt,
                                           state="readonly")
        _text_ = dt.date.today().strftime(_dt_datefmt)
        self.cal_tr_From.delete('0', 'end')
        self.cal_tr_From.insert('0', _text_)
        self.cal_tr_From.grid(column='1', padx='0', row='0', sticky='w')
        self.cal_tr_From.master.rowconfigure('0', pad='10')
        self.cal_tr_From.master.columnconfigure('1', pad='10', weight=1)
        self.label2 = ttk.Label(self.lbfr_drTransactions)
        self.label2.configure(text='To:')
        self.label2.grid(column='0', padx='10', row='1', sticky='e')
        self.label2.master.rowconfigure('1', pad='10')
        self.label2.master.columnconfigure('0', pad='10')
        self.cal_tr_To = tkcal.DateEntry(self.lbfr_drTransactions, 
                                         date_pattern=_cal_datefmt,
                                         state='readonly')
        _text_ =  dt.date.today().strftime(_dt_datefmt)
        self.cal_tr_To.delete('0', 'end')
        self.cal_tr_To.insert('0', _text_)
        self.cal_tr_To.grid(column='1', row='1', sticky='w')
        self.cal_tr_To.master.rowconfigure('1', pad='10')
        self.cal_tr_To.master.columnconfigure('1', pad='10', weight=1)
        self.label1 = ttk.Label(self.lbfr_drTransactions)
        self.label1.configure(text='Category:')
        self.label1.grid(column='0', padx='10', pady='10', row='2', sticky='e')
        self.label1.master.rowconfigure('1', pad='10')
        self.label1.master.rowconfigure('2', pad='10')
        self.label1.master.columnconfigure('0', pad='10')
        self.cmb_tr_Category = ttk.Combobox(self.lbfr_drTransactions)
        self.cmb_tr_Category.grid(column='1', row='2', sticky='ew')
        self.lbfr_drTransactions.configure(height='0', text='Choose date range')
        self.lbfr_drTransactions.grid(column='0', ipadx='0', ipady='0', padx='5', pady='0', row='0', sticky='nsew')
        self.lbfr_drTransactions.master.rowconfigure('0', pad='10', weight=0)
        self.lbfr_drTransactions.master.columnconfigure('0', pad='0', weight=1)
        self.lbfr_Operations = ttk.Labelframe(self.frm_transactions)
        self.btn_trAdd = ttk.Button(self.lbfr_Operations)
        self.btn_trAdd.configure(text='Add', width='20')
        self.btn_trAdd.grid(column='0', row='0')
        self.btn_trAdd.master.rowconfigure('0', pad='10')
        self.btn_trAdd.master.columnconfigure('0', pad='10')
        self.btn_trAdd.configure(command=self.h_btnTrAdd)
        self.btn_trChange = ttk.Button(self.lbfr_Operations)
        self.btn_trChange.configure(text='Change', width='20')
        self.btn_trChange.grid(column='0', row='1')
        self.btn_trChange.master.rowconfigure('1', pad='10')
        self.btn_trChange.master.columnconfigure('0', pad='10')
        self.btn_trChange.configure(command=self.h_btnTrChange)
        self.btn_trDelete = ttk.Button(self.lbfr_Operations)
        self.btn_trDelete.configure(text='Delete', width='20')
        self.btn_trDelete.grid(column='0', row='2')
        self.btn_trDelete.master.rowconfigure('2', pad='10')
        self.btn_trDelete.master.columnconfigure('0', pad='10')
        self.btn_trDelete.configure(command=self.h_btnTrDelete)
        self.btn_trImport = ttk.Button(self.lbfr_Operations)
        self.btn_trImport.configure(text='Import CSV...', width='20')
        self.btn_trImport.grid(column='1', row='0')
        self.btn_trImport.master.rowconfigure('0', pad='10')
        self.btn_trImport.master.columnconfigure('1', pad='25')
        self.btn_trImport.configure(command=self.h_btnTrImport)
        self.btn_trExport = ttk.Button(self.lbfr_Operations)
        self.btn_trExport.configure(text='Export CSV...', width='20')
        self.btn_trExport.grid(column='1', row='1')
        self.btn_trExport.master.rowconfigure('1', pad='10')
        self.btn_trExport.master.columnconfigure('1', pad='25')
        self.btn_trExport.configure(command=self.h_btnTrExport)
        self.btn_trLotto = ttk.Button(self.lbfr_Operations)
        self.btn_trLotto.configure(cursor='no', text='Play lotto', width='15')
        self.btn_trLotto.grid(column='1', row='2')
        self.btn_trLotto.configure(command=self.h_btnTrLotto)
        self.lbfr_Operations.configure(height='0', text='Commands', width='200')
        self.lbfr_Operations.grid(column='1', padx='5', row='0', sticky='ns')
        self.lbfr_Operations.master.rowconfigure('0', pad='10', weight=0)
        
        self.lbfr_tableTransactions = ttk.Labelframe(self.frm_transactions)
        
        self.tbl_transactions = ttk.Treeview(self.lbfr_tableTransactions)
        self.scrb_trTableVert = ttk.Scrollbar(self.lbfr_tableTransactions)
        self.scrb_trTableVert.configure(orient='vertical')
        self.scrb_trTableVert.grid(column='1', row='0', sticky='ns')
        self.scrb_trTableVert.configure(command=self.tbl_transactions.yview)
        
        self.tbl_transactions_cols = ['column1', 'column2', 'column3', 'column4']
        self.tbl_transactions_dcols = ['column1', 'column2', 'column3', 'column4']
        self.tbl_transactions.configure(columns=self.tbl_transactions_cols, 
                                        displaycolumns=self.tbl_transactions_dcols,
                                        yscrollcommand=self.scrb_trTableVert.set)
        self.tbl_transactions.column('column1', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.column('column2', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.column('column3', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.column('column4', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.heading('column1', anchor='w',text='Date')
        self.tbl_transactions.heading('column2', anchor='w',text='Amount')
        self.tbl_transactions.heading('column3', anchor='w',text='Category')
        self.tbl_transactions.heading('column4', anchor='w',text='Contractor')
        self.tbl_transactions['show'] = 'headings'
        self.tbl_transactions.grid(column='0', padx='3', pady='3', row='0', sticky='nsew')
        self.tbl_transactions.master.rowconfigure('0', weight=1)
        self.tbl_transactions.master.columnconfigure('0', weight=1)
        
        self.lbfr_tableTransactions.grid(column='0', columnspan='2', padx='5', row='1', sticky='nsew')
        self.lbfr_tableTransactions.master.rowconfigure('1', weight=1)
        self.lbfr_tableTransactions.master.columnconfigure('0', pad='0', weight=1)
        self.frm_transactions.grid(column='0', padx='3', pady='10', row='0', sticky='nsew')
        self.frm_transactions.master.rowconfigure('0', weight=1)
        self.frm_transactions.master.columnconfigure('0', weight=1)
        self.ntb_app.add(self.frm_transactions, text='Trancations')
        
        
        ### Categories tab
        self.frm_categories = ttk.Frame(self.ntb_app)
        self.lbfr_tableCategories = ttk.Labelframe(self.frm_categories)
        # table
        self.tbl_categories = ttk.Treeview(self.lbfr_tableCategories)
        self.scrb_catTableVert = ttk.Scrollbar(self.lbfr_tableCategories)
        self.scrb_catTableVert.configure(orient='vertical', takefocus=False)
        self.scrb_catTableVert.grid(column='1', row='0', sticky='ns')
        self.scrb_catTableVert.configure(command=self.tbl_categories.yview)
        self.tbl_categories_cols = ['column5', 'column6', 'column7', 'column8']
        self.tbl_categories_dcols = ['column5', 'column6', 'column7', 'column8']
        self.tbl_categories.configure(columns=self.tbl_categories_cols, 
                                      displaycolumns=self.tbl_categories_dcols,
                                        yscrollcommand=self.scrb_catTableVert.set)
        self.tbl_categories.column('column5', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_categories.column('column6', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_categories.column('column7', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_categories.column('column8', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_categories.heading('column5', anchor='w',text='column1')
        self.tbl_categories.heading('column6', anchor='w',text='column2')
        self.tbl_categories.heading('column7', anchor='w',text='column3')
        self.tbl_categories.heading('column8', anchor='w',text='column4')
        self.tbl_categories.grid(column='0', padx='3', pady='3', row='0', sticky='nsew')
        self.tbl_categories.master.rowconfigure('0', weight='1')
        self.tbl_categories.master.columnconfigure('0', weight='1')
        self.lbfr_tableCategories.grid(column='0', columnspan='2', padx='5', row='1', sticky='nsew')
        self.lbfr_tableCategories.master.rowconfigure('1', weight='1')
        self.lbfr_tableCategories.master.columnconfigure('0', pad='0', weight='1')
        self.lbfr_cat_Commands = ttk.Labelframe(self.frm_categories)
        self.btn_catAdd = ttk.Button(self.lbfr_cat_Commands)
        self.btn_catAdd.configure(text='Add', width='20')
        self.btn_catAdd.grid(column='0', row='0')
        self.btn_catAdd.master.rowconfigure('0', pad='10')
        self.btn_catAdd.master.columnconfigure('0', pad='10')
        self.btn_catAdd.configure(command=self.h_btnCatAdd)
        self.btn_catChange = ttk.Button(self.lbfr_cat_Commands)
        self.btn_catChange.configure(text='Change', width='20')
        self.btn_catChange.grid(column='0', row='1')
        self.btn_catChange.master.rowconfigure('1', pad='10')
        self.btn_catChange.master.columnconfigure('0', pad='10')
        self.btn_catChange.configure(command=self.h_btnCatChange)
        self.btn_catDelete = ttk.Button(self.lbfr_cat_Commands)
        self.btn_catDelete.configure(text='Delete', width='20')
        self.btn_catDelete.grid(column='0', row='2')
        self.btn_catDelete.master.rowconfigure('2', pad='10')
        self.btn_catDelete.master.columnconfigure('0', pad='10')
        self.btn_catDelete.configure(command=self.h_btnCatDelete)
        self.lbfr_cat_Commands.configure(height='0', text='Commands', width='200')
        self.lbfr_cat_Commands.grid(column='1', padx='5', row='0', sticky='ns')
        self.lbfr_cat_Commands.master.rowconfigure('0', pad='10', weight=0)
        self.lbfr_cat_data = ttk.Labelframe(self.frm_categories)
        self.label8 = ttk.Label(self.lbfr_cat_data)
        self.label8.configure(text='Name:')
        self.label8.grid(column='0', padx='10', pady='10', row='0', sticky='e')
        self.label8.master.rowconfigure('0', pad='10')
        self.label8.master.columnconfigure('0', pad='10')
        self.txt_cat_Name = ttk.Entry(self.lbfr_cat_data)
        _text_ = ''
        self.txt_cat_Name.delete('0', 'end')
        self.txt_cat_Name.insert('0', _text_)
        self.txt_cat_Name.grid(column='1', padx='0', row='0', sticky='w')
        self.txt_cat_Name.master.rowconfigure('0', pad='10')
        self.txt_cat_Name.master.columnconfigure('1', pad='20', weight=1)
        self.label9 = ttk.Label(self.lbfr_cat_data)
        self.label9.configure(text='To:')
        self.label9.grid(column='0', padx='10', row='1', sticky='e')
        self.label9.master.rowconfigure('1', pad='10')
        self.label9.master.columnconfigure('0', pad='10')
        self.entry7 = ttk.Entry(self.lbfr_cat_data)
        _text_ = ''
        self.entry7.delete('0', 'end')
        self.entry7.insert('0', _text_)
        self.entry7.grid(column='1', row='1', sticky='w')
        self.entry7.master.rowconfigure('1', pad='10')
        self.entry7.master.columnconfigure('1', pad='20', weight=1)
        self.label10 = ttk.Label(self.lbfr_cat_data)
        self.label10.configure(text='To:')
        self.label10.grid(column='0', padx='10', row='2', sticky='e')
        self.label10.master.rowconfigure('1', pad='10')
        self.label10.master.columnconfigure('0', pad='10')
        self.entry8 = ttk.Entry(self.lbfr_cat_data)
        _text_ = ''
        self.entry8.delete('0', 'end')
        self.entry8.insert('0', _text_)
        self.entry8.grid(column='1', row='2', sticky='w')
        self.entry8.master.rowconfigure('1', pad='10')
        self.entry8.master.columnconfigure('1', pad='20', weight=1)
        self.lbfr_cat_data.configure(height='0', text='Data for operations')
        self.lbfr_cat_data.grid(column='0', ipadx='0', ipady='0', padx='5', pady='0', row='0', sticky='nsew')
        self.lbfr_cat_data.master.rowconfigure('0', pad='10', weight=0)
        self.lbfr_cat_data.master.columnconfigure('0', pad='0', weight=1)
        self.frm_categories.grid(column='0', padx='3', pady='10', row='0', sticky='nsew')
        self.frm_categories.master.rowconfigure('0', weight=1)
        self.frm_categories.master.columnconfigure('0', weight=1)
        self.ntb_app.add(self.frm_categories, text='Categories	')
        
        
        ### Lotto tab
        self.frm_lotto = ttk.Frame(self.ntb_app)
        self.lbfr_weather = ttk.Labelframe(self.frm_lotto)
        self.calendar = tkcal.Calendar(self.lbfr_weather)
        self.calendar.grid(column='0', padx='10', pady='10', row='2')
        self.lbfr_weather.configure(text='Calendar')
        self.lbfr_weather.grid(column='0', row='0', sticky='nsew')
        self.labelframe5 = ttk.Labelframe(self.frm_lotto)
        self.label6 = ttk.Label(self.labelframe5)
        self.label6.configure(justify='center', text='weather, icon, location')
        self.label6.grid(column='0', row='0', sticky='e')
        self.label7 = ttk.Label(self.labelframe5)
        self.var_CurrentTime = tk.StringVar(value='eeef')
        self.label7.configure(background='lightgreen', font='{Arial} 16 {}', foreground='black', justify='center')
        self.label7.configure(textvariable=self.var_CurrentTime, width='20')
        self.label7.grid(column='0', row='1')
        self.labelframe5.configure(text='Weather')
        self.labelframe5.grid(column='1', row='0', sticky='nsew')
        self.labelframe5.master.columnconfigure('1', weight=1)
        self.frm_lotto.grid(column='0', row='0', sticky='nsew')
        self.frm_lotto.master.rowconfigure('0', weight=1)
        self.frm_lotto.master.columnconfigure('0', weight=1)
        self.ntb_app.add(self.frm_lotto, text='Bells and whistlers')
        
        
        ### NOTEBOOK grid ...
        self.ntb_app.configure(style='Toolbutton', takefocus=True)
        self.ntb_app.grid(column='0', padx='5', pady='5', row='0', sticky='nsew')
        self.ntb_app.master.rowconfigure('0', weight=1)
        self.ntb_app.master.columnconfigure('0', weight=1)
        self.root_app.configure(relief='flat')
        self.root_app.geometry('800x500')
        self.root_app.minsize(700, 400)
        self.root_app.resizable(True, True)
        self.root_app.title('Python cash')

        # SHOW window, fully constructed
        self.root_app.deiconify()

        # Main widget
        self.mainwindow = self.root_app
        
        # DataHandler instance
        self.badb = App_data()
                   
            
    def updateTransactionTable(self):
        #first clear the treeview
        for item in  self.tbl_transactions.get_children():
             self.tbl_transactions.delete(item)
        #then display data
        count = 0
        data = self.badb.getAllTransactions()
        for row in data:
            date = row[1].strftime(_dt_datefmt)
            values = (date,row[2], row[3], row[4])
            self.tbl_transactions.insert('','end', values = values)
            count+=1
     #tree view 

    def h_btnTrAdd(self):
        addTransactionWindow = AddTransaction(self.mainwindow, self.badb)
        
        pass


    def h_btnTrChange(self):
        pass

    def h_btnTrDelete(self):
        pass        

    def h_btnTrImport(self):
        pass

    def h_btnTrExport(self):
        pass

    def h_btnTrLotto(self):
        date = dt.datetime.now()
        amount = -21.32
        self.badb.addTransaction(date,amount,"Lotto",None)
        self.updateTransactionTable()
        
        pass

    def tbl_transactions(self, mode=None, value=None, units=None):
        pass

    def h_btnCatAdd(self):
        pass

    def h_btnCatChange(self):
        pass

    def h_btnCatDelete(self):
        pass


                
        
    def display_time(self):
        self.var_CurrentTime.set( value= time.strftime('%H:%M:%S') )
        self.mainwindow.after(200, self.display_time)     

    def run(self):
        self.display_time()
        self.updateTransactionTable()
        self.mainwindow.mainloop()    

if __name__ == '__main__':
    #app = LoginWin()
    #app.run()
    
    app = AppWin()
    app.run()
   


