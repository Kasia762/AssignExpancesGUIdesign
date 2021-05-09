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
    def __init__(self, master, dbconn,id_value=None):
        self.id_transaction = id_value
        # build ui
        if master == None:
            print("Cannot run independently. Pass master attribute")
            return
        
        self.win_addtr = tk.Toplevel(master)
        ## Hide window 
        ## DO NOT forget to show at the end of init!!!
        self.win_addtr.withdraw()     
        
        #apparently radiobuttons are not compatibile with tk.Tk
        self.win_addtr.grab_set()
        self.fr_addtr = ttk.Frame(self.win_addtr)
        
        self.lbfr_atdate = ttk.Labelframe(self.fr_addtr)
        self.lbl_atdate = ttk.Label(self.lbfr_atdate)
        self.lbl_atdate.configure(text='Date:')
        self.lbl_atdate.grid(column='0', padx='40', pady='10', row='0')
        
        self.cal_tr = tkcal.DateEntry(self.lbfr_atdate, 
                                      date_pattern=_cal_datefmt)
        #state="readonly"   
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
        
        self.lbl_atcontr = ttk.Label(self.lbfr_atinfo)
        self.lbl_atcontr.configure(text='Contractor')
        self.lbl_atcontr.grid(column='0', padx='20', pady='10', row='1')
        self.cmb_atcontr = ttk.Combobox(self.lbfr_atinfo)
        self.cmb_atcontr.grid(column='1', pady='10', row='1')
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
        # ADD BUTTON
        self.btn_add = ttk.Button(self.fr_addtr, command = self.h_btnAdd)
       
        self.btn_add.pack(anchor='center', padx='5', pady='15', side='right')
        # Cancel button
        self.btn_exit = ttk.Button(self.fr_addtr, command =self.h_btnCancel)
        self.btn_exit.configure(text='Cancel')
        self.btn_exit.pack(anchor='center', padx='20', pady='15', side='right')
        
        
        self.fr_addtr.configure(height='200', width='200')
        self.fr_addtr.pack(expand='true', fill='both', padx='10', pady='10', side='top')
        
        self.win_addtr.configure(height='200', width='200')
        self.win_addtr.resizable(False, False)
        
        ## Center window
        x_modal = 350
        y_modal = 400
        x_parent = master.winfo_width()
        y_parent = master.winfo_height()
        x = master.winfo_rootx() + (x_parent - x_modal) // 2
        y = master.winfo_rooty() + (y_parent - y_modal) // 2
        self.win_addtr.geometry('{}x{}+{}+{}'.format(x_modal, y_modal, x, y))
        
        # SHOW window, fully constructed
        self.win_addtr.deiconify()
        # Main widget
        self.mainwindow = self.win_addtr
        
        ### Bindings
        self.btn_add.bind('<Return>', lambda x: self.h_btnAdd() )
        self.mainwindow.bind('<Escape>', lambda x: self.h_btnCancel() )
        self.ent_atamount.bind('<Return>', lambda x: self.__evaluateAmountEntry() )

        self.radioButtonSelection()    
        self.badb=dbconn
    #    self.run()
    
        if self.id_transaction == None:
            self.win_addtr.title('Add transaction')
            self.btn_add.configure(text='Add')
            today = dt.date.today().strftime(_dt_datefmt)
            self.cal_tr.delete('0','end')
            self.cal_tr.insert('0', today)
            self.cal_tr.configure(state="readonly")
            #pass
        else:
            self.win_addtr.title('Change transaction')
            self.btn_add.configure(text='Accept')
            row=self.badb.getTransaction_byid(self.id_transaction)[0]
            date = row[1].strftime(_dt_datefmt)
            self.cal_tr.delete('0','end')
            self.cal_tr.insert('0', date)
            self.cal_tr.configure(state="readonly")
            
            self.amount = abs(row[2])
            
            cat = row[3]
            if not cat == None:
                self.cmb_atcat.set(cat)
            else:
                pass
            
            cont = row[4]
            if not cont == None:
                self.cmb_atcontr.set(cont)
            else:
                pass
            
        

    def __setAmountEntryToDefault(self):
        if self.id_transaction == None:
        # Delete all and set to zero.
            self.__setAmountEntry('0.0')
            self.ent_atamount.focus()
            self.ent_atamount.select_range(0, tk.END)
        else:
            self.__setAmountEntry(self.amount)
        
    def __setAmountEntry(self, value):
        # Delete all and set to zero.
        self.ent_atamount.delete(0, tk.END)
        self.ent_atamount.insert(0, value)
        
    def __evaluateAmountEntry(self):
        # Try to evaluate string in Entry as python:
        try:
            s = self.ent_atamount.get()
            news = str( eval(s) )
            self.__setAmountEntry(news)
            self.ent_atamount.tk_focusNext().focus()
            return True
        except:
            print("Amoun cannot be calculated...")
            self.ent_atamount.focus()
            self.ent_atamount.select_range(0, tk.END)
            return False
        
    def h_btnCancel(self):
        self.mainwindow.destroy()
    
    def radioButtonSelection(self):
        self.selection = self.var.get()

    def h_btnAdd(self):
    #update fields to selected row    
        
        #AMOUNT
        if not self.__evaluateAmountEntry() :
            return
        try:
            amountABS = float(self.ent_atamount.get())
        except:
            print("No number or whatever")
            tk.messagebox.showwarning("Enter valid data",
                                      "Amount cannot be calculated.\n\nPlease, enter correct amount.",
                                      parent=self.mainwindow)
            return
        amountABS = abs(amountABS)
        if amountABS == 0:
            print("Entered amount is equal to zero.")
            tk.messagebox.showwarning("Enter valid data",
                                      "Amount cannot be  equal zero.\n\nPlease, enter positive amount.",
                                      parent=self.mainwindow)
            return
             
        if self.selection == 2:
            self.amount= float(-amountABS)
        elif self.selection == 1:
            self.amount = amountABS
        else:
            print("Some internal error: radiobutton not selected.")
            raise("Radiobutton not selected")
            return
        
        #TODO: add if else statements to check if values are correct
        date = self.cal_tr.get_date()
        category = self.cmb_atcat.get()
        contractor = self.cmb_atcontr.get()
        amount = self.amount 
            
        if self.id_transaction == None:
            self.badb.addTransaction(date, amount, category, contractor)
            
        else:
            self.badb.changeTransaction(self.id_transaction,date,amount, category, contractor)
            #self.id_transaction = None
            self.mainwindow.destroy()
            #if not destoyed - next option -add
            
        self.__setAmountEntryToDefault()
            
  
     
    def viewCatergories(self):
        data = self.badb.getCategoriesList()
        ind_cat = 0
        tr=[i[ind_cat]for i in data]
        self.cmb_atcat['values']= tr
          
    def viewContractors(self):
        data = self.badb.getContractorList()
        ind_contr = 0
        tr=[i[ind_contr]for i in data]
        self.cmb_atcontr['values']= tr   
       
            
        
#amount no 0

    def run(self):
        #self.convertToNegative()
        #self.radioButtonSelection()
        self.__setAmountEntryToDefault()
        self.viewContractors()
        self.viewCatergories()
        self.mainwindow.mainloop()
