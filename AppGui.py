# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 13:15:25 2021

@author: kasia
"""

import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.calendarframe import CalendarFrame
from tkcalendar import Calendar, DateEntry
import time as tm



class LoginWin():
    def __init__(self, master=None):
        # build ui
        self.login_window = tk.Tk()
        self.login_notebook = ttk.Notebook(self.login_window)
        
        #LOG IN TAB
        self.login_frame = ttk.Frame(self.login_notebook)
        self.login_labelframe = ttk.Labelframe(self.login_frame)
        
        #labels, entries and button in log in tab
        self.selectUser_label = ttk.Label(self.login_labelframe)
        self.selectUser_label.configure(text='Select user')
        self.selectUser_label.pack(pady='10',side='top')
        
        self.selectUser_combo = ttk.Combobox(self.login_labelframe)
        self.selectUser_combo.pack(side='top')
        
        self.enterPassword_label = ttk.Label(self.login_labelframe)
        self.enterPassword_label.configure(text='Enter password')
        self.enterPassword_label.pack(pady='10',side='top')
        
        self.enterPassword_entry = ttk.Entry(self.login_labelframe)
        self.enterPassword_entry.pack(side='top')
        
        self.login_buttton = ttk.Button(self.login_labelframe)
        self.login_buttton.configure(text='LOG IN')
        self.login_buttton.pack(pady='20',ipadx='10',ipady='5',side='top')
        
        self.login_labelframe.configure(text='Please log in below')
        self.login_labelframe.pack(ipadx='50', pady='50', side='top')
        self.login_frame.pack(side='top')
        
        self.login_notebook.add(self.login_frame, state='hidden', text='log in')
        
        #ADD USER TAB
        self.addUser_frame = ttk.Frame(self.login_notebook)
        self.addUser_labelframe = ttk.Labelframe(self.addUser_frame)
        
        #labels, entries and button in add user tab
        self.username_label = ttk.Label(self.addUser_labelframe)
        self.username_label.configure(text='Username')
        self.username_label.grid(column='0', row='0',pady='10',padx='50',ipady='10')
        
        self.username_entry = ttk.Entry(self.addUser_labelframe)
        self.username_entry.grid(column='1', row='0',padx='10')
        
        self.password_label = ttk.Label(self.addUser_labelframe)
        self.password_label.configure(text='Password')
        self.password_label.grid(column='0', row='1',pady='10',padx='10')
        
        self.password_entry = ttk.Entry(self.addUser_labelframe)
        self.password_entry.grid(column='1', row='1',padx='10')
        
        self.confirmPassword_label = ttk.Label(self.addUser_labelframe)
        self.confirmPassword_label.configure(text='Confirm password')
        self.confirmPassword_label.grid(column='0', row='2',pady='10',padx='10')
        
        self.confirmPassword_entry = ttk.Entry(self.addUser_labelframe)
        self.confirmPassword_entry.grid(column='1', row='2',padx='10')
        
        self.submit_button = ttk.Button(self.addUser_labelframe)
        self.submit_button.configure(text='SUBMIT')
        self.submit_button.grid(column='0', row='3',pady='20',ipadx='10',ipady='5',columnspan='2')
        
        self.adduserInfo_label = ttk.Label(self.addUser_labelframe)
        #TODO: add text into label: about adding new user
        self.adduserInfo_label.configure(text='user added')
        self.adduserInfo_label.grid(column='0', row='4',pady='10',columnspan='2')
        
        self.addUser_labelframe.configure(height='200', text='Please enter the details below', width='200')
        self.addUser_labelframe.pack(ipadx='10',padx='50', pady='50', side='top')
        
        self.addUser_frame.configure(height='300', width='300')
        self.addUser_frame.pack(side='top')
        
        self.login_notebook.add(self.addUser_frame, text='add user')
        self.login_notebook.pack(expand='true', fill='both', side='top')
        
        self.login_window.configure(takefocus=False)

        # Main widget
        self.loginWindow = self.login_window
        self.loginWindow.title("Login")

    def run(self):
        self.loginWindow.mainloop()

if __name__ == '__main__':
    login_app = LoginWin()
    login_app.run()


class AppWin:
    def __init__(self, master=None):
        # build ui
                
        self.app_window = tk.Tk() if master is None else tk.Toplevel(master)
        self.app_windowframe = tk.Frame(self.app_window)
        self.app_notebook = ttk.Notebook(self.app_windowframe)
        
        #ACCOUNT TAB
        self.account_frame = ttk.Frame(self.app_notebook)
        self.account_labelframe = ttk.Labelframe(self.account_frame)
        
        self.balance_label = ttk.Label(self.account_labelframe)
        self.balance_label.configure(text='Your balance is: $$$$$')
        self.balance_label.pack(padx='40', pady='10', side='top')
        
        self.account_canvas = tk.Canvas(self.account_labelframe)
        self.account_canvas.pack(padx='50', pady='10', side='top')
        
        self.percentage_label = ttk.Label(self.account_labelframe)
        self.percentage_label.configure(text='You spend xx% of your money for this month')
        self.percentage_label.pack(pady='10', side='top')
        
        self.progressbar = ttk.Progressbar(self.account_labelframe)
        self.progressbar.configure(orient='horizontal')
        self.progressbar.pack(ipadx='100', pady='10', side='top')
        
        self.account_labelframe.configure(height='200', text='Your account in summary', width='200')
        self.account_labelframe.grid(column='1', ipady='10', padx='20', pady='40', row='0')
        
        self.account_frame.configure(height='200', width='200')
        self.account_frame.grid(column='0', row='0')
        
        self.app_notebook.add(self.account_frame, text='Account')
        
        #TRANSACTION
        self.transactions_frame = ttk.Frame(self.app_notebook)
        self.tableTransactions_labelframe = ttk.Labelframe(self.transactions_frame)
        
        self.tableTransactions_canvas = tk.Canvas(self.tableTransactions_labelframe)
        self.tableTransactions_canvas.pack(side='top')
        
        self.tableTransactions_labelframe.configure(height='200', text='table view', width='200')
        self.tableTransactions_labelframe.grid(column='0', columnspan='2', row='1')
        
        self.drTransactions_labelframe = ttk.Labelframe(self.transactions_frame)
        
        #change names!!!
        self.dfTran_label = ttk.Label(self.drTransactions_labelframe)
        self.dfTran_label.configure(text='Date from')
        self.dfTran_label.grid(column='0',row='0')
        #DATE PATTERN
        self.cal3 = DateEntry(self.drTransactions_labelframe,date_pattern='dd-mm-y')
        self.cal3.grid(column='1', row='0')
        
        self.dtTran_label = ttk.Label(self.drTransactions_labelframe)
        self.dtTran_label.configure(text='to')
        self.dtTran_label.grid(column='2',row='0')
        
        self.cal13 = DateEntry(self.drTransactions_labelframe)
        self.cal13.grid(column='3', row='0')
        #change names!!!
        
        self.drTransactions_labelframe.configure(height='200', text='Choose date range', width='300')
        self.drTransactions_labelframe.grid(column='0', row='0')
        
        self.transactions_frame.configure(height='200', width='200')
        self.transactions_frame.pack(side='top')
        
        self.app_notebook.add(self.transactions_frame, text='Trancations')
        
        #OVERVIEW
        self.overview_frame = ttk.Frame(self.app_notebook)
        self.drOverview_labelframe = ttk.Labelframe(self.overview_frame)
        
        self.fromDate = ttk.Label(self.drOverview_labelframe)
        self.fromDate.configure(text='From')
        self.fromDate.grid(column='0', row='0')
        
        #CALENDAR - i dont like the name
        self.cal_from = DateEntry(self.drOverview_labelframe)
        self.cal_from.grid(column='1', row='0')
              
        self.cal_to = DateEntry(self.drOverview_labelframe)
        self.cal_to.grid(column='3', row='0')   
        
        self.toDate = ttk.Label(self.drOverview_labelframe)
        self.toDate.configure(text='to')
        self.toDate.grid(column='2', row='0')
                        
        self.loadTable_button = ttk.Button(self.drOverview_labelframe)
        self.loadTable_button.configure(text='Load')        
        self.loadTable_button.grid(column='4', row='0')
        
        self.drOverview_labelframe.configure(height='200', text='Data range', width='200')
        self.drOverview_labelframe.pack(side='top')
        
        self.tableOverview_labelframe = ttk.Labelframe(self.overview_frame)
        self.tableOverview_canvas = tk.Canvas(self.tableOverview_labelframe)
        self.tableOverview_canvas.grid(column='0', columnspan='2', row='0')
        
        self.export_button = ttk.Button(self.tableOverview_labelframe)
        self.export_button.configure(text='export to csv')
        self.export_button.grid(column='0', row='1')
        
        self.modify_button = ttk.Button(self.tableOverview_labelframe)
        self.modify_button.configure(text='modify')
        self.modify_button.grid(column='1', row='1')
        
        self.tableOverview_labelframe.configure(height='200', text='Table view', width='200')
        self.tableOverview_labelframe.pack(side='top')
        
        self.overview_frame.configure(height='200', width='200')
        self.overview_frame.pack(side='top')
        
        self.app_notebook.add(self.overview_frame, text='Overview')
        
        #LOTTO- WEATHER, LOCATION TAB
        self.lotto_frame = ttk.Frame(self.app_notebook)
        self.weather_labelframe = ttk.Labelframe(self.lotto_frame)
        
        self.weather_label = ttk.Label(self.weather_labelframe)
        self.weather_label.configure(text='weather, icon, location')
        self.weather_label.pack(side='top')
        
                           
        self.time_label = ttk.Label(self.weather_labelframe)
        self.time_label.configure(text='time')
        self.time_label.pack(side='top')
        
        #self.calendar = CalendarFrame(self.weather_labelframe)
        # TODO - self.calendar: code for custom option 'firstweekday' not implemented.
        # TODO - self.calendar: code for custom option 'month' not implemented.
        #self.calendar.pack(side='top')
        self.calendar = Calendar(self.weather_labelframe, selectmode='day')
        self.calendar.pack(side='top', fill="both",expand=True)
        
        
        self.weather_labelframe.configure(height='200', text='weather', width='200')
        self.weather_labelframe.pack(side='top')
        
        self.lotto_labelframe = ttk.Labelframe(self.lotto_frame)
        self.lotto_label = ttk.Label(self.lotto_labelframe)
        
        self.lotto_label.configure(text='disclaimer: 5 euro will be subtracted from your account')
        self.lotto_label.pack(side='top')
        
        self.lotto_button = ttk.Button(self.lotto_labelframe)
        self.lotto_button.configure(text='i accept, click to play lotto')
        self.lotto_button.pack(side='top')
        
        self.lotto_labelframe.configure(height='200', text='lotto', width='200')
        self.lotto_labelframe.pack(side='top')
        
        self.lotto_frame.configure(height='200', width='200')
        self.lotto_frame.pack(side='top')
        
        self.app_notebook.add(self.lotto_frame, text='here we have lotto/weather')
        self.app_notebook.configure(style='Toolbutton', takefocus=True)
        self.app_notebook.pack(pady='40', side='top')
        
        self.account_menubutton = ttk.Menubutton(self.app_windowframe)
        self.account_menubutton.configure(text='myAcount')
        self.account_menubutton.place(anchor='nw', x='500', y='40')
        
        self.app_windowframe.grid(column='0', row='0')
        
        self.app_window.configure(height='700', relief='flat', width='800')
        self.app_window.resizable(True, True)

        # Main widget
        self.mainwindow = self.app_window
        self.display_time()
        
    def display_time(self):
        self.current_time=tm.strftime('%H:%M:%S')
        self.time_label['text']=self.current_time
        self.weather_labelframe.after(1000,self.display_time)     

    def run(self):
        self.mainwindow.mainloop() 
        

if __name__ == '__main__':
    app = AppWin()
    app.run()
   


