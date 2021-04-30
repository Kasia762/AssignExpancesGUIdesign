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
            
        self.ntb_login = ttk.Notebook(self.root_login)
        
        
        
        #LOG IN TAB
        self.frm_Login = ttk.Frame(self.ntb_login)
        self.lbfr_Login = ttk.Labelframe(self.frm_Login)
        
        #labels, entries and button in log in tab
        self.lbl_SelectUser = ttk.Label(self.lbfr_Login)
        self.lbl_SelectUser.configure(text='Select user')
        self.lbl_SelectUser.pack(pady='10',side='top')
        
        self.cmb_SelectUser = ttk.Combobox(self.lbfr_Login, state="readonly")
        self.cmb_SelectUser.pack(side='top')
        
        self.lbl_PasswordLogin = ttk.Label(self.lbfr_Login)
        self.lbl_PasswordLogin.configure(text='Enter password')
        self.lbl_PasswordLogin.pack(pady='10',side='top')
        
        self.txt_PasswordLogin = ttk.Entry(self.lbfr_Login, show="*" )
        self.txt_PasswordLogin.pack(side='top')
        
        self.btn_Login = ttk.Button(self.lbfr_Login, command = self.cb_Login)
        self.btn_Login.configure(text='LOG IN')
        self.btn_Login.pack(pady='20',padx='30',ipadx='20',ipady='5',side='top')
        
        self.lbfr_Login.configure(text='Please log in below')
        self.lbfr_Login.pack(ipadx='50', pady='50', side='top')
        self.frm_Login.pack(side='top')
        
        self.ntb_login.add(self.frm_Login, state='hidden', text='log in')
        
        
        
        # ADD USER TAB
        self.frm_AddUser = ttk.Frame(self.ntb_login)
        self.lbfr_addUser = ttk.Labelframe(self.frm_AddUser)
        
        #labels, entries and button in add user tab
        self.lbl_Username = ttk.Label(self.lbfr_addUser)
        self.lbl_Username.configure(text='Username')#, justify=tk.RIGHT)
        self.lbl_Username.grid(column='0', padx='10', pady='15', row='0', sticky='e')
        
        self.txt_Username = ttk.Entry(self.lbfr_addUser)
        self.txt_Username.grid(column='1', row='0',padx='10')
        
        self.lbl_PasswordCreate = ttk.Label(self.lbfr_addUser)
        self.lbl_PasswordCreate.configure(text='Password')
        self.lbl_PasswordCreate.grid(column='0', padx='10', pady='5', row='1', sticky='e')
        
        self.txt_PasswordCreate = ttk.Entry(self.lbfr_addUser, show="*" )
        self.txt_PasswordCreate.grid(column='1', row='1',padx='10')
        
        self.lbl_PasswordConfCreate = ttk.Label(self.lbfr_addUser)
        self.lbl_PasswordConfCreate.configure(text='Confirm password')
        self.lbl_PasswordConfCreate.grid(column='0', padx='10', pady='5', row='2', sticky='e')
        
        self.txt_PasswordConfCreate = ttk.Entry(self.lbfr_addUser, show="*" )
        self.txt_PasswordConfCreate.grid(column='1', row='2',padx='10')
        
        self.btn_Submit = ttk.Button(self.lbfr_addUser, command = self.cb_CreateUser)
        self.btn_Submit.configure(text='SUBMIT')
        self.btn_Submit.grid(column='0', row='3',
                                pady='20',ipadx='10',padx='10',ipady='5',columnspan='2')
        
        self.lbl_AdduserInfo = ttk.Label(self.lbfr_addUser)
        #TODO: add text into label: about adding new user
        self.lbl_AdduserInfo.configure(
            text='Enter username to create\n and type selected password two times.',
            justify=tk.CENTER)
        self.lbl_AdduserInfo.grid(column='0', row='4',pady='10',columnspan='2')
        
        self.lbfr_addUser.configure(height='200', text='Please enter the details below', width='200')
        self.lbfr_addUser.pack(ipadx='10',padx='50', pady='50', side='top')
        
        self.frm_AddUser.configure(height='300', width='300')
        self.frm_AddUser.pack(side='top')
        
        self.ntb_login.add(self.frm_AddUser, text='add user')
        self.ntb_login.pack(expand='true', fill='both', side='top')
        
        #self.root_login.configure(takefocus=False)
        self.root_login.resizable(width=False, height=False)
        
        ## Style correcting for tab's well-view
        style = ttk.Style()                     
        current_theme =style.theme_use()
        style.theme_settings(current_theme, 
                {"TNotebook.Tab": {"configure": {"padding": [95, 5]}}})
   
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

        if not self.txt_Username.get():
            self.lbl_Username.config(foreground="red")
            return False
        else:
            self.lbl_Username.configure(foreground="black")
        
        if not self.txt_PasswordCreate.get():
            self.lbl_PasswordCreate.config(foreground="red")
            return False
        else:
            self.lbl_PasswordCreate.configure(foreground="black")
        
        if not (self.txt_PasswordCreate.get() == self.txt_PasswordConfCreate.get()):
            self.lbl_PasswordCreate.config(foreground="red")
            self.lbl_PasswordConfCreate.config(foreground="red")
            return False
        else:
            self.lbl_PasswordCreate.configure(foreground="black")
            self.lbl_PasswordConfCreate.configure(foreground="black")
        
        ## TODO: call UserCreate()
        pass
    
    
    def cb_Login(self):
        """
        Create user callback

        Returns
        -------
        None.

        """
        if  self.cmb_SelectUser.current() < 0:
            self.lbl_SelectUser.config(foreground="red")
            return False
        else:
            self.lbl_SelectUser.configure(foreground="black")

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
        self.cal_tr_From = tkcal.DateEntry(self.lbfr_drTransactions, date_pattern=_cal_datefmt)
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
        self.cal_tr_To = tkcal.DateEntry(self.lbfr_drTransactions, date_pattern=_cal_datefmt)
        _text_ =  dt.date.today().strftime(_dt_datefmt)
        print("tpe:",type(_text_))
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
        self.button1 = ttk.Button(self.lbfr_Operations)
        self.button1.configure(text='Add', width='20')
        self.button1.grid(column='0', row='0')
        self.button1.master.rowconfigure('0', pad='10')
        self.button1.master.columnconfigure('0', pad='10')
        self.button2 = ttk.Button(self.lbfr_Operations)
        self.button2.configure(text='Change', width='20')
        self.button2.grid(column='0', row='1')
        self.button2.master.rowconfigure('1', pad='10')
        self.button2.master.columnconfigure('0', pad='10')
        self.button3 = ttk.Button(self.lbfr_Operations)
        self.button3.configure(text='Delete', width='20')
        self.button3.grid(column='0', row='2')
        self.button3.master.rowconfigure('2', pad='10')
        self.button3.master.columnconfigure('0', pad='10')
        self.button4 = ttk.Button(self.lbfr_Operations)
        self.button4.configure(text='Import CSV...', width='20')
        self.button4.grid(column='1', row='0')
        self.button4.master.rowconfigure('0', pad='10')
        self.button4.master.columnconfigure('1', pad='25')
        self.button5 = ttk.Button(self.lbfr_Operations)
        self.button5.configure(text='Export CSV...', width='20')
        self.button5.grid(column='1', row='1')
        self.button5.master.rowconfigure('1', pad='10')
        self.button5.master.columnconfigure('1', pad='25')
        self.button6 = ttk.Button(self.lbfr_Operations)
        self.button6.configure(cursor='no', text='Play lotto', width='15')
        self.button6.grid(column='1', row='2')
        self.lbfr_Operations.configure(height='0', text='Commands', width='200')
        self.lbfr_Operations.grid(column='1', padx='5', row='0', sticky='ns')
        self.lbfr_Operations.master.rowconfigure('0', pad='10', weight=0)
        self.lbfr_tableTransactions = ttk.Labelframe(self.frm_transactions)
        self.tbl_transactions = ttk.Treeview(self.lbfr_tableTransactions)
        self.tbl_transactions_cols = ['column1', 'column2', 'column3', 'column4']
        self.tbl_transactions_dcols = ['column1', 'column2', 'column3', 'column4']
        self.tbl_transactions.configure(columns=self.tbl_transactions_cols, displaycolumns=self.tbl_transactions_dcols)
        self.tbl_transactions.column('column1', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.column('column2', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.column('column3', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.column('column4', anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.heading('column1', anchor='w',text='column1')
        self.tbl_transactions.heading('column2', anchor='w',text='column2')
        self.tbl_transactions.heading('column3', anchor='w',text='column3')
        self.tbl_transactions.heading('column4', anchor='w',text='column4')
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
        self.labelframe3 = ttk.Labelframe(self.frm_categories)
        self.treeview1 = ttk.Treeview(self.labelframe3)
        self.treeview1_cols = ['column5', 'column6', 'column7', 'column8']
        self.treeview1_dcols = ['column5', 'column6', 'column7', 'column8']
        self.treeview1.configure(columns=self.treeview1_cols, displaycolumns=self.treeview1_dcols)
        self.treeview1.column('column5', anchor='w',stretch='true',width='200',minwidth='20')
        self.treeview1.column('column6', anchor='w',stretch='true',width='200',minwidth='20')
        self.treeview1.column('column7', anchor='w',stretch='true',width='200',minwidth='20')
        self.treeview1.column('column8', anchor='w',stretch='true',width='200',minwidth='20')
        self.treeview1.heading('column5', anchor='w',text='column1')
        self.treeview1.heading('column6', anchor='w',text='column2')
        self.treeview1.heading('column7', anchor='w',text='column3')
        self.treeview1.heading('column8', anchor='w',text='column4')
        self.treeview1.grid(column='0', padx='3', pady='3', row='0', sticky='nsew')
        self.treeview1.master.rowconfigure('0', weight=1)
        self.treeview1.master.columnconfigure('0', weight=1)
        self.labelframe3.grid(column='0', columnspan='2', padx='5', row='1', sticky='nsew')
        self.labelframe3.master.rowconfigure('1', weight=1)
        self.labelframe3.master.columnconfigure('0', pad='0', weight=1)
        self.lbfr_cat_Commands = ttk.Labelframe(self.frm_categories)
        self.button13 = ttk.Button(self.lbfr_cat_Commands)
        self.button13.configure(text='Add', width='20')
        self.button13.grid(column='0', row='0')
        self.button13.master.rowconfigure('0', pad='10')
        self.button13.master.columnconfigure('0', pad='10')
        self.button14 = ttk.Button(self.lbfr_cat_Commands)
        self.button14.configure(text='Change', width='20')
        self.button14.grid(column='0', row='1')
        self.button14.master.rowconfigure('1', pad='10')
        self.button14.master.columnconfigure('0', pad='10')
        self.button15 = ttk.Button(self.lbfr_cat_Commands)
        self.button15.configure(text='Delete', width='20')
        self.button15.grid(column='0', row='2')
        self.button15.master.rowconfigure('2', pad='10')
        self.button15.master.columnconfigure('0', pad='10')
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

        # Main widget
        self.mainwindow = self.root_app


    def run(self):
        self.display_time()
        self.mainwindow.mainloop()
        
        
        
    def display_time(self):
        self.var_CurrentTime.set( value= time.strftime('%H:%M:%S') )
        self.mainwindow.after(1000, self.display_time)     

        

if __name__ == '__main__':
    
    app = AppWin()
    app.run()
   


