# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 13:15:25 2021

@author: kasia
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkcalendar as tkcal
import time




class AppWin:
    class LoginWin:
        def __init__(self, master=None):
            # self._cal_datefmt = "dd.mm.yyyy"
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


            
    ## App class
    def __init__(self, master=None):
        self._cal_datefmt = "dd.mm.yyyy"
        # build ui
        if master == None:
            self.root_app = tk.Tk()
        else:
            self.root_app = master
        

        self.app_windowframe = ttk.Frame(self.root_app, padding=(3,3,5,5))
        self.ntb_app = ttk.Notebook(self.app_windowframe)

        
        #################### #ACCOUNT TAB
        self.frm_account = ttk.Frame(self.ntb_app)
        self.lbfr_account = ttk.Labelframe(self.frm_account)
        
        self.lbl_balance = ttk.Label(self.lbfr_account)
        self.lbl_balance.configure(text='Your balance is: $$$$$')
        self.lbl_balance.pack(padx='40', pady='5', side='top')
        
        self.lbl_percentage = ttk.Label(self.lbfr_account)
        self.lbl_percentage.configure(text='You spend xx% of your money for this month')
        self.lbl_percentage.pack(pady='5', side='top')
        
        self.progressbar = ttk.Progressbar(self.lbfr_account)
        self.progressbar.configure(orient='horizontal')
        self.progressbar.pack(padx='50', pady='5', side='top',
                             fill=tk.X)
        
        self.lbfr_account.configure(height='200', text='Your account in summary', width='200')
        self.lbfr_account.pack(side=tk.TOP,
                             ipady='5', ipadx='20',
                               padx='3', pady='3',
                             fill=tk.X)

        self.lbfr_accChart = ttk.Labelframe(self.frm_account)
        self.frm_AccChart = ttk.Frame(self.lbfr_accChart)
        self.frm_AccChart.pack(padx='5', pady='3', side='top',
                             fill=tk.BOTH, expand=True)
        
        self.lbfr_accChart.pack(padx='3', pady='3', side='top',
                             fill=tk.BOTH, expand=True)
        
        
        self.frm_account.configure(height='200', width='200')
        self.frm_account.pack( fill=tk.BOTH, expand=True)
        
        self.ntb_app.add(self.frm_account, text='Account')
        
        
        ########################## #TRANSACTION
        self.frm_transactions = ttk.Frame(self.ntb_app)
        self.lbfr_trControls = ttk.Frame(self.frm_transactions)
        self.lbfr_drTransactions = ttk.Labelframe(self.lbfr_trControls)
        
        #change names!!!
        self.lbl_dfTran = ttk.Label(self.lbfr_drTransactions)
        self.lbl_dfTran.configure(text='From')
        self.lbl_dfTran.grid(column='0', row='0', padx='3', pady='3',
                             sticky=tk.E)
        
        self.cal3 = tkcal.DateEntry(self.lbfr_drTransactions, date_pattern=self._cal_datefmt)
        self.cal3.grid(column='1', row='0', padx='3', pady='3',
                             sticky=tk.NSEW)
        
        self.lbl_dtTran = ttk.Label(self.lbfr_drTransactions)
        self.lbl_dtTran.configure(text='To')
        self.lbl_dtTran.grid(column='0', row='1', padx='3', pady='3',
                             sticky=tk.E)
        
        self.cal13 = tkcal.DateEntry(self.lbfr_drTransactions, date_pattern=self._cal_datefmt)
        self.cal13.grid(column='1', row='1', padx='3', pady='3',
                             sticky=tk.NSEW)
        # TODO: grid expand for dateEntry
        self.lbfr_drTransactions.columnconfigure( 1, weight=1)
        
        #change names!!!
        self.lbfr_trButtons = ttk.Labelframe(self.lbfr_trControls)
        
        self.btn_trAdd = ttk.Button(self.lbfr_trButtons)
        self.btn_trAdd.configure(text='Add')        
        self.btn_trAdd.pack(side='top')
        self.btn_trChange = ttk.Button(self.lbfr_trButtons)
        self.btn_trChange.configure(text='Change')        
        self.btn_trChange.pack(side='top')
        self.btn_trDelete = ttk.Button(self.lbfr_trButtons)
        self.btn_trDelete.configure(text='Delete')        
        self.btn_trDelete.pack(side='top')
        self.btn_export = ttk.Button(self.lbfr_trButtons)
        self.btn_export.configure(text='Export')
        self.btn_export.pack(pady='10', side='top')
        
        self.lbfr_drTransactions.configure(height='200', text='Choose date range', width='300')
        self.lbfr_drTransactions.pack(side=tk.LEFT,
                             ipady='5', ipadx='20',
                               padx='3', pady='3',
                             fill=tk.BOTH, expand=True)
        self.lbfr_trButtons.pack(side=tk.RIGHT,
                             ipady='5', ipadx='20',
                               padx='3', pady='3')
        self.lbfr_trControls.pack(side=tk.TOP,
                             ipady='5', ipadx='20',
                               padx='3', pady='3',
                             fill=tk.X)

        self.lbfr_tableTransactions = ttk.Labelframe(self.frm_transactions)
        self.tbl_trTable = ttk.Treeview(self.lbfr_tableTransactions)
        self.tbl_trTable_cols = ['column1', 'column2', 'column3']
        self.tbl_trTable_dcols = ['column1', 'column2', 'column3']
        self.tbl_trTable.configure(columns=self.tbl_trTable_cols, displaycolumns=self.tbl_trTable_dcols)
        self.tbl_trTable.column('column1', anchor='w',stretch='true',width='200',minwidth='100')
        self.tbl_trTable.column('column2', anchor='w',stretch='true',width='100',minwidth='50')
        self.tbl_trTable.column('column3', anchor='w',stretch='true',width='100',minwidth='50')
        self.tbl_trTable.heading('column1', anchor='w',text='column1')
        self.tbl_trTable.heading('column2', anchor='w',text='column2')
        self.tbl_trTable.heading('column3', anchor='w',text='column3')
        self.tbl_trTable['show'] = 'headings'
        self.tbl_trTable.pack(side='top',
                             fill=tk.BOTH, expand=True)
        
        self.lbfr_tableTransactions.configure(height='200', text='', width='200')
        self.lbfr_tableTransactions.pack(side=tk.BOTTOM,
                             ipady='5', ipadx='20',
                               padx='3', pady='3',
                             fill=tk.BOTH, expand=True)
        
        self.frm_transactions.configure(height='200', width='200')
        self.frm_transactions.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.ntb_app.add(self.frm_transactions, text='Trancations')

                    
                    ######################### #OVERVIEW
                # self.frm_overview = tk.Frame(self.ntb_app, background="bisque")
                # self.lbfr_drOverview = ttk.Labelframe(self.frm_overview)
                
                # self.fromDate = ttk.Label(self.lbfr_drOverview)
                # self.fromDate.configure(text='From')
                # self.fromDate.grid(column='0', row='0')
                
                # #CALENDAR - i dont like the name
                # self.cal_from = tkcal.DateEntry(self.lbfr_drOverview, date_pattern=self._cal_datefmt)
                # self.cal_from.grid(column='1', row='0')
                      
                # self.cal_to = tkcal.DateEntry(self.lbfr_drOverview, date_pattern=self._cal_datefmt)
                # self.cal_to.grid(column='3', row='0')   
                
                # self.toDate = ttk.Label(self.lbfr_drOverview)
                # self.toDate.configure(text='to')
                # self.toDate.grid(column='2', row='0')
                                
                # self.btn_loadTable = ttk.Button(self.lbfr_drOverview)
                # self.btn_loadTable.configure(text='Load')        
                # self.btn_loadTable.grid(column='4', row='0')
                
                # self.lbfr_drOverview.configure(height='200', text='Data range', width='200')
                # self.lbfr_drOverview.pack(side='top')
                
                # self.lbfr_tableOverview = ttk.Labelframe(self.frm_overview)
                # self.cnv_tableOverview = tk.Canvas(self.lbfr_tableOverview)
                # self.cnv_tableOverview.grid(column='0', columnspan='2', row='0')
                
                # self.btn_export = ttk.Button(self.lbfr_tableOverview)
                # self.btn_export.configure(text='export to csv')
                # self.btn_export.grid(column='0', row='1')
                
                # self.btn_modify = ttk.Button(self.lbfr_tableOverview)
                # self.btn_modify.configure(text='modify')
                # self.btn_modify.grid(column='1', row='1')
                
                # self.lbfr_tableOverview.configure(height='200', text='Table view', width='200')
                # self.lbfr_tableOverview.pack(side='top')
                
                # self.frm_overview.configure(height='200', width='200')
                # self.frm_overview.pack(side='top')
                
                # self.ntb_app.add(self.frm_overview, text='Overview')


                    
                    ##################### #LOTTO- WEATHER, LOCATION TAB
        self.frm_lotto = ttk.Frame(self.ntb_app)
        self.lbfr_weather = ttk.Labelframe(self.frm_lotto)
        
        self.lbl_weather = ttk.Label(self.lbfr_weather)
        self.lbl_weather.configure(text='weather, icon, location')
        self.lbl_weather.pack(side='top')
        
        self.varTime = tk.StringVar()                   
        self.lbl_time = ttk.Label(self.lbfr_weather)
        self.lbl_time.configure(textvariable=self.varTime)
        self.lbl_time.pack(side='top')
        
        #self.calendar = CalendarFrame(self.lbfr_weather)
        # TODO - self.calendar: code for custom option 'firstweekday' not implemented.
        # TODO - self.calendar: code for custom option 'month' not implemented.
        #self.calendar.pack(side='top')
        self.calendar = tkcal.Calendar(self.lbfr_weather, selectmode='day', date_pattern=self._cal_datefmt)
        self.calendar.pack(side='top', fill="both",expand=True)
        
        
        self.lbfr_weather.configure(height='200', text='weather', width='200')
        self.lbfr_weather.pack(side='top')
        
        self.lbfr_lotto = ttk.Labelframe(self.frm_lotto)
        self.lbl_lotto = ttk.Label(self.lbfr_lotto)
        
        self.lbl_lotto.configure(text='disclaimer: 5 euro will be subtracted from your account')
        self.lbl_lotto.pack(side='top')
        
        self.btn_lotto = ttk.Button(self.lbfr_lotto)
        self.btn_lotto.configure(text='I agree, play lotto')
        self.btn_lotto.pack(side='top')
        
        self.lbfr_lotto.configure(height='200', text='lotto', width='200')
        self.lbfr_lotto.pack(side='top')
        
        self.frm_lotto.configure(height='200', width='200')
        self.frm_lotto.pack(side='top')
        
        self.ntb_app.add(self.frm_lotto, text='Bells and whistlers')


        self.ntb_app.configure(style='Toolbutton', takefocus=True)
        self.ntb_app.pack( fill=tk.BOTH, expand=True)
        
        # self.mnbtn_account = ttk.Menubutton(self.app_windowframe)
        # self.mnbtn_account.configure(text='myAcount')
        # self.mnbtn_account.place(anchor='nw', x='500', y='40')
        
        self.app_windowframe.pack(  fill=tk.BOTH, expand=True)
        
        self.root_app.configure(height='700', relief='flat', width='800')
        self.root_app.resizable(True, True)

        # ## Style correcting for tab's well-view
        # style = ttk.Style()                     
        # current_theme =style.theme_use()
        # style.theme_settings(current_theme, 
        #         {"TNotebook.Tab": {"configure": {"padding": [20, 15]}}})


        # Main widget
        self.mainwindow = self.root_app
        
    def display_time(self):
        # self.varTime.set( time.strftime('%H:%M:%S') )
        self.mainwindow.after(1000, self.display_time)     
        # self.lbfr_weather.after(1000,self.display_time)     

    def run(self):
        # login_app = self.LoginWin(self.mainwindow )
        # login_app.run()
        # self.mainwindow.wait_window(login_app)
        
        self.display_time()
        self.mainwindow.mainloop() 
        

if __name__ == '__main__':
    
    app = AppWin()
    app.run()
   


