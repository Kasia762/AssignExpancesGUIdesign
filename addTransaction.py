# -*- coding: utf-8 -*-
"""
Created on Sat May  1 00:14:00 2021

@author: kasia
"""

import tkinter.ttk as ttk
import tkcalendar as tkcal
import time
import datetime as dt
import tkinter as tk
from app_data import App_data 


## both format should match
_dt_datefmt = "%d.%m.%Y"
_cal_datefmt = "dd.mm.yyyy"


class AddTransaction:
    def __init__(self,dbconn, master=None,):
        # build ui
        #self.win_addtr = tk.Tk() if master is None else tk.Toplevel(master)
        self.win_addtr = tk.Toplevel(master)
        #apparently radiobuttons are not compatibile with tk.Tk
        
        self.fr_addtr = ttk.Frame(self.win_addtr)
        
        self.lbfr_atdate = ttk.Labelframe(self.fr_addtr)
        self.lbl_atdate = ttk.Label(self.lbfr_atdate)
        self.lbl_atdate.configure(text='Date:')
        self.lbl_atdate.grid(column='0', padx='40', pady='10', row='0')
        
        self.cal_tr = tkcal.DateEntry(self.lbfr_atdate, date_pattern=_cal_datefmt)
        _text_ = dt.date.today().strftime(_dt_datefmt)
        self.cal_tr.delete('0', 'end')
        self.cal_tr.insert('0', _text_)
        self.cal_tr.grid(column='1', pady='0', row='0')
        
        #TODO: make nicer gui?? calendar?? seems too on the left?
        '''
        self.cal_tr.master.rowconfigure('0', pad='10')
        self.cal_tr.master.columnconfigure('1', pad='10', weight=1)
                
        '''
        
        self.lbfr_atdate.configure(height='200', text='Select date', width='200')
        self.lbfr_atdate.pack(anchor='center', expand='true', fill='x', padx='20', side='top')
        self.lbfr_atinfo = ttk.Labelframe(self.fr_addtr)
        self.lbl_atcat = ttk.Label(self.lbfr_atinfo)
        self.lbl_atcat.configure(text='Category')
        self.lbl_atcat.grid(column='0', padx='20', pady='10', row='0')
        
        self.cmb_atcat = ttk.Combobox(self.lbfr_atinfo)
        self.cmb_atcat.grid(column='1', pady='10', row='0')
        
        self.cmb_atcontr = ttk.Label(self.lbfr_atinfo)
        self.cmb_atcontr.configure(text='Contractor')
        self.cmb_atcontr.grid(column='0', padx='20', pady='10', row='1')
        self.combobox2 = ttk.Combobox(self.lbfr_atinfo)
        self.combobox2.grid(column='1', pady='10', row='1')
        self.lbfr_atinfo.configure(height='200', text='Add information', width='200')
        self.lbfr_atinfo.pack(anchor='center', expand='true', fill='x', padx='20', side='top')
        self.lbfr_attype = ttk.Labelframe(self.fr_addtr)
        
        #radiobox stuff
        #TODO: add option to control wheter amount is positive or negative
        self.var = tk.IntVar()
        #self.var.set("2")
        self.rbt_with = ttk.Radiobutton(self.lbfr_attype,
                                        variable=self.var,
                                        value=1,
                                        command=self.radioButtonSelection)
        self.rbt_with.configure(text='Withdrawal')
        self.rbt_with.grid(column='0', padx='40', pady='10', row='0')
        
        
        self.rbt_depo = ttk.Radiobutton(self.lbfr_attype,
                                        variable=self.var,
                                        value=2,
                                        command=self.radioButtonSelection)
        self.rbt_depo.configure(text='Deposit')
        self.rbt_depo.grid(column='1', pady='10', row='0')
        self.rbt_depo.invoke()
                       
        self.lbfr_attype.configure(height='200', text='Select transaction type', width='200')
        self.lbfr_attype.pack(anchor='center', expand='true', fill='x', padx='20', side='top')
        self.lbfr_atamount = ttk.Labelframe(self.fr_addtr)
        self.ent_atamount = ttk.Entry(self.lbfr_atamount)
        #_text_ = '''entry2'''
        #self.ent_atamount.delete('0', 'end')
        #self.ent_atamount.insert('0', _text_)
        self.ent_atamount.grid(column='1', pady='10', row='0')
        self.lbl_atamount = ttk.Label(self.lbfr_atamount)
        self.lbl_atamount.configure(text='Amount')
        self.lbl_atamount.grid(column='0', padx='40', pady='10', row='0')
        self.lbfr_atamount.configure(height='200', text='Type amount', width='200')
        self.lbfr_atamount.pack(anchor='center', expand='true', fill='both', padx='20', side='top')
        
        #exit add window with button self.btn_exit - OK,EXIT
        self.btn_exit = ttk.Button(self.fr_addtr, command =self.win_addtr.destroy)
        self.btn_exit.configure(text='ok, exit')
        self.btn_exit.pack(anchor='center', padx='20', pady='15', side='right')
        
        #ADD BUTTON
        self.btn_add = ttk.Button(self.fr_addtr, command = self.collectInput)
        self.btn_add.configure(text='Add')
        self.btn_add.pack(anchor='center', padx='5', pady='15', side='right')
        
        self.fr_addtr.configure(height='200', width='200')
        self.fr_addtr.pack(expand='true', fill='both', padx='10', pady='10', side='top')
        
        self.win_addtr.configure(height='200', width='200')
        self.win_addtr.geometry('350x400')
        self.win_addtr.resizable(False, False)
        self.win_addtr.title('Add transaction')
         
        self.radioButtonSelection()    
        self.badb=dbconn
        self.run()
    
    def radioButtonSelection(self):
        self.selection = self.var.get()

    def collectInput(self):
        #AMOUNT
        amountABS = abs(float(self.ent_atamount.get()))
             
        if self.selection == 2:
            #self.amount = float("-"+ self.ent_atamount.get())
            self.amount= float(-amountABS)
           
        else:#self.selection == 1:
            #self.amount = float(self.ent_atamount.get())
            self.amount = amountABS
        
        #TODO: add if else statements to check if values are correct
        date = self.cal_tr.get_date()
        category = self.cmb_atcat.get()
        contractor = self.combobox2.get()
        amount = self.amount  
        
        #listTransaction = list[date,amount,category,contractor]  
        
        #else print put correct values???
        self.ent_atamount.delete(0,len(str(amount)))
        return 5
     
    def viewCatergories(self):
        data = self.badb.getCategoriesList()
        ind_cat = 0
        tr=[i[ind_cat]for i in data]
        self.cmb_atcat['values']= tr
          
    def viewContractors(self):
        data = self.badb.getContractorList()
        ind_contr = 0
        tr=[i[ind_contr]for i in data]
        self.combobox2['values']= tr   
       
            
        # Main widget
        self.mainwindow = self.win_addtr
        
#amount no 0

    def run(self):
        #self.convertToNegative()
        #self.radioButtonSelection()
        self.viewContractors()
        self.viewCatergories()
        self.mainwindow.mainloop()
