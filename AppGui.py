# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 13:15:25 2021

@author: kasia
"""

import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.calendarframe import CalendarFrame
import tkinter as tk
import tkinter.ttk as ttk


#frame for login part
import tkinter as tk
import tkinter.ttk as ttk


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
        
        self.addUser_frame.configure(height='200', width='200')
        self.addUser_frame.pack(side='top')
        
        self.login_notebook.add(self.addUser_frame, text='add user')
        self.login_notebook.pack(expand='true', fill='both', side='top')
        
        self.login_window.configure(takefocus=False)

        # Main widget
        self.loginWindow = self.login_window
        self.loginWindow.title("Login")


    def run(self):
        self.loginWindow.mainloop()

#if __name__ == '__main__':
login_app = LoginWin()
login_app.run()





class AppLayoutApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel4 = tk.Tk() if master is None else tk.Toplevel(master)
        self.frame9 = tk.Frame(self.toplevel4)
        self.notebook14 = ttk.Notebook(self.frame9)
        self.frame23 = ttk.Frame(self.notebook14)
        self.labelframe31 = ttk.Labelframe(self.frame23)
        self.label11 = ttk.Label(self.labelframe31)
        self.label11.configure(text='weather, location')
        self.label11.pack(pady='10', side='top')
        self.label16 = ttk.Label(self.labelframe31)
        self.label16.configure(text='location')
        self.label16.pack(padx='10', side='top')
        self.calendarframe3 = CalendarFrame(self.labelframe31)
        # TODO - self.calendarframe3: code for custom option 'firstweekday' not implemented.
        # TODO - self.calendarframe3: code for custom option 'month' not implemented.
        self.calendarframe3.pack(ipadx='20', ipady='20', padx='20', pady='20', side='top')
        self.label4 = ttk.Label(self.labelframe31)
        self.label4.configure(text='label4')
        self.label4.pack(padx='10', side='top')
        self.labelframe31.configure(height='200', text='labelframe31', width='200')
        self.labelframe31.grid(column='0', ipady='40', padx='20', pady='40', row='0')
        self.labelframe34 = ttk.Labelframe(self.frame23)
        self.label17 = ttk.Label(self.labelframe34)
        self.label17.configure(text='euros in bank?/balance')
        self.label17.pack(padx='40', pady='10', side='top')
        self.canvas1 = tk.Canvas(self.labelframe34)
        self.canvas1.pack(padx='50', pady='10', side='top')
        self.label18 = ttk.Label(self.labelframe34)
        self.label18.configure(text='spendings in %? - progess bar?')
        self.label18.pack(pady='10', side='top')
        self.progressbar1 = ttk.Progressbar(self.labelframe34)
        self.progressbar1.configure(orient='horizontal')
        self.progressbar1.pack(ipadx='100', pady='10', side='top')
        self.labelframe34.configure(height='200', text='labelframe34', width='200')
        self.labelframe34.grid(column='1', ipady='10', padx='20', pady='40', row='0')
        self.frame23.configure(height='200', width='200')
        self.frame23.grid(column='0', row='0')
        self.notebook14.add(self.frame23, text='main/graph')
        self.frame6 = ttk.Frame(self.notebook14)
        self.labelframe1 = ttk.Labelframe(self.frame6)
        self.label19 = ttk.Label(self.labelframe1)
        self.label19.configure(text='label19')
        self.label19.pack(side='top')
        self.label20 = ttk.Label(self.labelframe1)
        self.label20.configure(text='label20')
        self.label20.pack(side='top')
        self.calendarframe4 = CalendarFrame(self.labelframe1)
        # TODO - self.calendarframe4: code for custom option 'firstweekday' not implemented.
        # TODO - self.calendarframe4: code for custom option 'month' not implemented.
        self.calendarframe4.pack(side='top')
        self.labelframe1.configure(text='calendar', width='200')
        self.labelframe1.grid(column='0', row='0', rowspan='2')
        self.labelframe6 = ttk.Labelframe(self.frame6)
        self.label21 = ttk.Label(self.labelframe6)
        self.label21.configure(text='label21')
        self.label21.grid(column='0', row='0')
        self.combobox2 = ttk.Combobox(self.labelframe6)
        self.combobox2.grid(column='1', row='0')
        self.label22 = ttk.Label(self.labelframe6)
        self.label22.configure(text='label22')
        self.label22.grid(column='0', row='1')
        self.entry4 = ttk.Entry(self.labelframe6)
        _text_ = '''entry4'''
        self.entry4.delete('0', 'end')
        self.entry4.insert('0', _text_)
        self.entry4.grid(column='1', row='1')
        self.label23 = ttk.Label(self.labelframe6)
        self.label23.configure(text='label23')
        self.label23.grid(column='0', row='2')
        self.entry5 = ttk.Entry(self.labelframe6)
        _text_ = '''entry5'''
        self.entry5.delete('0', 'end')
        self.entry5.insert('0', _text_)
        self.entry5.grid(column='1', row='2')
        self.label24 = ttk.Label(self.labelframe6)
        self.label24.configure(text='label24')
        self.label24.grid(column='0', row='3')
        self.entry6 = ttk.Entry(self.labelframe6)
        _text_ = '''entry6'''
        self.entry6.delete('0', 'end')
        self.entry6.insert('0', _text_)
        self.entry6.grid(column='1', row='3')
        self.label25 = ttk.Label(self.labelframe6)
        self.label25.configure(text='label25')
        self.label25.grid(column='0', row='4')
        self.checkbutton1 = ttk.Checkbutton(self.labelframe6)
        self.checkbutton1.configure(text='checkbutton1')
        self.checkbutton1.grid(column='1', row='4')
        self.button5 = ttk.Button(self.labelframe6)
        self.button5.configure(text='submit/add')
        self.button5.grid(column='0', row='5')
        self.button6 = ttk.Button(self.labelframe6)
        self.button6.configure(text='cancel')
        self.button6.grid(column='1', row='5')
        self.button9 = ttk.Button(self.labelframe6)
        self.button9.configure(text='det date')
        self.button9.grid(column='2', row='2')
        self.labelframe6.configure(height='200', text='enter data', width='200')
        self.labelframe6.grid(column='1', row='0')
        self.labelframe14 = ttk.Labelframe(self.frame6)
        self.button12 = ttk.Button(self.labelframe14)
        self.button12.configure(text='button12')
        self.button12.pack(side='top')
        self.labelframe14.configure(height='200', text='lotto', width='200')
        self.labelframe14.grid(column='1', row='1')
        self.frame6.configure(height='200', width='200')
        self.frame6.pack(side='top')
        self.notebook14.add(self.frame6, text='add spendings')
        self.frame8 = ttk.Frame(self.notebook14)
        self.labelframe11 = ttk.Labelframe(self.frame8)
        self.label26 = ttk.Label(self.labelframe11)
        self.label26.configure(text='label26')
        self.label26.grid(column='0', row='0')
        self.combobox3 = ttk.Combobox(self.labelframe11)
        self.combobox3.grid(column='1', row='0')
        self.label28 = ttk.Label(self.labelframe11)
        self.label28.configure(text='label28')
        self.label28.grid(column='2', row='0')
        self.combobox4 = ttk.Combobox(self.labelframe11)
        self.combobox4.grid(column='3', row='0')
        self.button7 = ttk.Button(self.labelframe11)
        self.button7.configure(text='view/load')
        self.button7.grid(column='4', row='0')
        self.labelframe11.configure(height='200', text='labelframe11', width='200')
        self.labelframe11.pack(side='top')
        self.labelframe12 = ttk.Labelframe(self.frame8)
        self.canvas3 = tk.Canvas(self.labelframe12)
        self.canvas3.grid(column='0', columnspan='2', row='0')
        self.button10 = ttk.Button(self.labelframe12)
        self.button10.configure(text='export to csv')
        self.button10.grid(column='0', row='1')
        self.button11 = ttk.Button(self.labelframe12)
        self.button11.configure(text='accept changes')
        self.button11.grid(column='1', row='1')
        self.labelframe12.configure(height='200', text='labelframe12', width='200')
        self.labelframe12.pack(side='top')
        self.frame8.configure(height='200', width='200')
        self.frame8.pack(side='top')
        self.notebook14.add(self.frame8, text='edit/table')
        self.frame1 = tk.Frame(self.notebook14)
        self.labelframe2 = tk.LabelFrame(self.frame1)
        self.label1 = tk.Label(self.labelframe2)
        self.label1.configure(text='label1')
        self.label1.pack(side='top')
        self.entry7 = tk.Entry(self.labelframe2)
        _text_ = '''entry7t'''
        self.entry7.delete('0', 'end')
        self.entry7.insert('0', _text_)
        self.entry7.pack(side='top')
        self.label2 = tk.Label(self.labelframe2)
        self.label2.configure(text='label2')
        self.label2.pack(side='top')
        self.entry10 = tk.Entry(self.labelframe2)
        _text_ = '''entry10'''
        self.entry10.delete('0', 'end')
        self.entry10.insert('0', _text_)
        self.entry10.pack(side='top')
        self.label3 = tk.Label(self.labelframe2)
        self.label3.configure(text='label3')
        self.label3.pack(side='top')
        self.entry11 = tk.Entry(self.labelframe2)
        _text_ = '''entry11'''
        self.entry11.delete('0', 'end')
        self.entry11.insert('0', _text_)
        self.entry11.pack(side='top')
        self.button1 = tk.Button(self.labelframe2)
        self.button1.configure(text='button1')
        self.button1.pack(side='top')
        self.button8 = tk.Button(self.labelframe2)
        self.button8.configure(text='button8')
        self.button8.pack(side='top')
        self.labelframe2.configure(height='200', text='labelframe2', width='200')
        self.labelframe2.pack(side='top')
        self.frame1.configure(height='200', width='200')
        self.frame1.grid(column='0', row='0')
        self.notebook14.add(self.frame1, text='set up')
        self.frame11 = ttk.Frame(self.notebook14)
        self.labelframe13 = ttk.Labelframe(self.frame11)
        self.label29 = ttk.Label(self.labelframe13)
        self.label29.configure(text='label29')
        self.label29.grid(column='0', row='0')
        self.combobox5 = ttk.Combobox(self.labelframe13)
        self.combobox5.grid(column='1', row='0')
        self.canvas4 = tk.Canvas(self.labelframe13)
        self.canvas4.grid(column='0', columnspan='2', row='1')
        self.label30 = ttk.Label(self.labelframe13)
        self.label30.configure(text='label30')
        self.label30.grid(column='0', row='2')
        self.entry12 = ttk.Entry(self.labelframe13)
        _text_ = '''entry12'''
        self.entry12.delete('0', 'end')
        self.entry12.insert('0', _text_)
        self.entry12.grid(column='0', row='3')
        self.label31 = ttk.Label(self.labelframe13)
        self.label31.configure(text='label31')
        self.label31.grid(column='0', row='4')
        self.entry13 = ttk.Entry(self.labelframe13)
        _text_ = '''entry13'''
        self.entry13.delete('0', 'end')
        self.entry13.insert('0', _text_)
        self.entry13.grid(column='0', row='5')
        self.label32 = ttk.Label(self.labelframe13)
        self.label32.configure(text='label32')
        self.label32.grid(column='0', row='6')
        self.entry14 = ttk.Entry(self.labelframe13)
        _text_ = '''entry14'''
        self.entry14.delete('0', 'end')
        self.entry14.insert('0', _text_)
        self.entry14.grid(column='0', row='7')
        self.labelframe13.configure(height='200', text='labelframe13', width='200')
        self.labelframe13.pack(side='top')
        self.frame11.configure(height='200', width='200')
        self.frame11.pack(side='top')
        self.notebook14.add(self.frame11, text='account summary')
        self.notebook14.configure(style='Toolbutton', takefocus=True)
        self.notebook14.pack(pady='40', side='top')
        self.menubutton2 = ttk.Menubutton(self.frame9)
        self.menubutton2.configure(text='menubutton2')
        self.menubutton2.place(anchor='nw', x='500', y='40')
        self.frame9.grid(column='0', row='0')
        self.toplevel4.configure(height='600', relief='flat', width='700')

        # Main widget
        self.mainwindow = self.toplevel4


    def run(self):
        self.mainwindow.mainloop()

#if __name__ == '__main__':
#    app = AppLayoutApp()
#    app.run()

