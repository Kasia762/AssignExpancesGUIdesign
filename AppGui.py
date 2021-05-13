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
import pandas as pd
from app_data import App_data 
from addTransaction import AddTransaction
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import app_import
### ***
#import lotto

## both format should match
_dt_datefmt = "%d.%m.%Y"
_cal_datefmt = "dd.mm.yyyy"

#######################################3


class AppWin:
    def __init__(self, master=None):
        
        # DataHandler instance
        self.badb = App_data()
        
        # TODO: user manager handle
        
        # TODO: check user and call loginDialog ???
        
        # Main widget, build GUI
        self.mainwindow = self.GUI(master)
        ### BINDs
        self.cal_tr_To.bind('<<DateEntrySelected>>', lambda x: self.updateTransactionTable() )
        self.cal_tr_From.bind('<<DateEntrySelected>>', lambda x: self.updateTransactionTable() )
        self.tbl_transactions.bind("<Double-1>", self.h_tblTr_OnDoubleClick)
        


        
    def chartSpendingsMonth(self):
        mon = self.spn_month.get()
        
        def getmonth():
            if mon == "January": return "01"
            elif mon =="February": return "02"
            elif mon == "March": return "03"
            elif mon == "April": return "04"
            elif mon == "May": return "05"
            elif mon == "June": return "06"
            elif mon == "July": return "07"
            elif mon == "August": return "08"
            elif mon == "September": return "09"
            elif mon == "October": return "10"
            elif mon == "December": return "12"
            elif mon == "November": return "11"
            else: 
              tk.messagebox.showwarning("Spinbox!!!!","put correct month",
                                      parent=self.mainwindow)
               
        monthname = str(mon)
        month=str(getmonth())
        amount = 0
        category = 1
        
        am = [-i[amount] for i in self.badb.chartMonth(month)]
        cat=[i[category] for i in self.badb.chartMonth(month)]
        print(i for i in self.badb.chartMonth(month))
    
        #fig = plt.figure(dpi=dpi)
        fig = plt.figure(dpi=100)
        ax = fig.add_subplot(111)
        chart = FigureCanvasTkAgg(fig, self.lbfr_Acc_Chart)
        chart.get_tk_widget().grid(padx=5, pady=5,
                                         column="0",row="1",columnspan="2")
        ax.bar(cat,height=am)
        ax.set_title('Spendings in '+ monthname)
        ax.set_xlabel("Categories");ax.set_ylabel("Spendings [Euros]")


        
    def updateTransactionTable(self):
        # self.display_balance()
        #first clear the treeview
        for i in self.tbl_transactions.get_children():
            self.tbl_transactions.delete(i)
             
        #then display data
        datefr = self.cal_tr_From.get_date()
        dateto = self.cal_tr_To.get_date()
        
        data = self.badb.getAllTransactionsPeriod(datefr, dateto)
        for row in data:
            idvalue = row[0]
            date = row[1].strftime(_dt_datefmt)
            cat = row[3] if row[3] else ""
            con = row[4] if row[4] else ""
            values = (idvalue, date, row[2], cat, con)
            self.tbl_transactions.insert('','end', values = values)



    def updateCategoriesTable(self):
        #first clear the treeview
        for item in  self.tbl_categories.get_children():
             self.tbl_categories.delete(item)
        #then display data
        data = self.badb.getCategoriesList()
        for row in data:
            cat = row[0] if row[0] else ""
            _id = row[1] if row[1] else ""
            values = (_id, cat)
            self.tbl_categories.insert('','end', values = values)
        


    def h_btnTrAdd(self):
        addTransactionWindow = AddTransaction(self.mainwindow, self)
        #self.mainwindow.wait_window(addTransactionWindow)
        self.updateTransactionTable()


    def h_btnLogout(self):
        pass


    
    def h_tblTr_OnDoubleClick(self, event):
        ### Detect only item, on which was double clicked
        print("Double-clicked in table ", end='')
        clicked = self.tbl_transactions.identify('item',event.x,event.y)
        selected = self.tbl_transactions.selection()
        if len(selected) == 1:
            print("element.")
            id_value = str( self.tbl_transactions.item(clicked, 'values')[0] )
            print('Opening addTransaction window in "change" mode, id: ', id_value)
            AddTransaction(self.mainwindow, self, id_value)
            self.updateTransactionTable()
        else:
                print("somewhere. Not olnly one element selected or other area clicked.")

        
    def h_btnTrChange(self):
        selected = self.tbl_transactions.selection()
        if len(selected) > 1:
            print("Multi selection in table. Cannot change several transactions yet.")
            tk.messagebox.showwarning("Change transaction",
                                   "Multi selection in table.\n\n Cannot change several transactions at once yet.",
                                      parent=self.mainwindow)
            return
        elif len(selected) == 1:
            print("One-line selection.")
            id_value = str(self.tbl_transactions.item(selected, 'values')[0])
            print('Opening addTransaction window in "change" mode, id: ', id_value)
            AddTransaction(self.mainwindow, self, id_value)
            self.updateTransactionTable()
        else:
            print("Nothing selected in table. Cannot change.")
            tk.messagebox.showwarning("Change transaction","Select transaction in table to change.",
                                      parent=self.mainwindow)

        

    def h_btnTrDelete(self):
        selected = self.tbl_transactions.selection()
        
        if len(selected) > 0:
            print("Some selection in table...")
            reply =  tk.messagebox.askyesno(title="Delete...", 
                           message=f"You going to delete {len(selected)} transactions.\n\n" + 
                                   "Are you sure?")
            if reply == True:
                for sel in selected:
                    id_value = self.tbl_transactions.item(sel, 'values')[0]
                    self.badb.deleteTransaction(id_value)
                self.updateTransactionTable()
            
        else:
            print("Nothing selected. Cannot delete.")
            tk.messagebox.showwarning("Delete transaction","Select transaction in table to delete.",
                                      parent=self.mainwindow)

        


    def h_btnTrImport(self):
        importWindow = app_import.ImportTransactionDialog(self.mainwindow, self)
        importWindow.run()
        print("Import dialog is opened...")
        self.mainwindow.wait_window(importWindow.mainwindow)
        print("... Import dialog closed.")
        self.updateTransactionTable()
        pass


    def h_btnTrExport(self):
        filetypes = (
            ('CSV files', '*.csv'),
#            ('Excel files', '*.xlsx'),
            ('All files', '*.*'))
        exportFileName = "_".join(
                        ("Export",
                        self.cal_tr_From.get_date().strftime(_dt_datefmt),
                        self.cal_tr_To.get_date().strftime(_dt_datefmt) ))
                        
        exportFileName = tk.filedialog.asksaveasfile(
                        title="Export current table view as...",
                        initialdir='./',
                        filetypes=filetypes,
                        defaultextension='.csv',
                        initialfile=exportFileName,
                        parent=self.mainwindow  )
        print("Selected filename for export: ", exportFileName.name )
        try:
            export_df = pd.DataFrame(None, columns=self.tbl_transactions_cols)
            for row in self.tbl_transactions.get_children():
                ## each row will come as a list under name "values" 
                rowvals = pd.DataFrame([self.tbl_transactions.item(row)['values']], 
                            columns=self.tbl_transactions_cols)
                export_df = export_df.append(rowvals)
            ## shrink dataframe to visible columns (no id of transaction)
            export_df = export_df[self.tbl_transactions_dcols]
        except:
            print("Unexpected error: cannot retrieve data from table.")
            tk.messagebox.showwarning("CSV export","Could not export: internal error",
                                      parent=self.mainwindow)
            return
        try:
            ## apply datetime format
            export_df.loc[:,'date'] = export_df.loc[:,'date'].apply(lambda x: dt.datetime.strptime(x, _dt_datefmt))
            export_df.to_csv(exportFileName, index = False)
        except:
            print("Unexpected error: cannot save data to csv.")
            tk.messagebox.showwarning("CSV export","Could not export: file writing error.\n\nPlease check filename...",
                                      parent=self.mainwindow)
            return
        tk.messagebox.showinfo("CSV export","Export complete.",
                                  parent=self.mainwindow)
        pass


    def h_btnTrLotto(self):
        date = dt.date.today()
        #amount = lotto.check()
        amount = -5.00
        self.badb.addTransaction(date, amount, "Lotto", None)
        self.updateTransactionTable()
        if amount < 0:
            tk.messagebox.showwarning("LOTTO RESULTS!!!!","You have bad luck",
                                      parent=self.mainwindow)
        else:
            tk.messagebox.showwarning("LOTTO RESULTS!!!!","You won "+str(amount)+", yeay",
                                      parent=self.mainwindow)


    def h_btnCatAdd(self):
        pass


    def h_btnCatChange(self):
        pass


    def h_btnCatDelete(self):
        pass

               
        
    def display_time(self):
        self.var_CurrentTime.set( value= time.strftime('%H:%M:%S') )
        self.mainwindow.after(1000, self.display_time)     

    def display_balance(self):
        ## TODO: not by after
        val = self.badb.getBalance()
        self.var_CurrentBalance.set( value= f"{val:.2f}" )
    

    def run(self):
        self.updateTransactionTable()
        self.updateCategoriesTable()
        self.display_time()
        self.display_balance()
        self.mainwindow.mainloop()    


    def GUI(self, master):
        # build ui
        if master == None:
            self.root_app = tk.Tk()
        else:
            self.root_app = tk.Toplevel(master)
        
        ## Hide window 
        ## DO NOT forget to show at the end of init!!!
        self.root_app.withdraw()     
        
        ### Notebook 
        self.ntb_app = ttk.Notebook(self.root_app)
        
        ### ACCOUNT TAB
        self.frm_account = ttk.Frame(self.ntb_app)
        self.lbfr_account = ttk.Labelframe(self.frm_account)
        self.lbl_balance = ttk.Label(self.lbfr_account)
        self.lbl_balance.configure(text='Balance:')
        self.lbl_balance.grid(column='0', padx='10', pady='5', row='0')
        self.lbl_percentage = ttk.Label(self.lbfr_account)
        self.var_CurrentBalance = tk.StringVar(value="...")
        self.lbl_percentage.configure(font='{Arial} 12 {bold}', textvariable=self.var_CurrentBalance)
        self.lbl_percentage.grid(column='1', row='0')
        self.progressbar = ttk.Progressbar(self.lbfr_account)
        self.progressbar.configure(orient='horizontal')
        self.progressbar.grid(column='2', padx='10', row='0', sticky='ew')
        self.progressbar.master.columnconfigure('2', weight=1)
        # logout button
        self.btn_Logout = ttk.Button(self.lbfr_account)
        self.btn_Logout.configure(text='Logout', width='15')
        self.btn_Logout.configure(command=self.h_btnLogout)
        self.btn_Logout.grid(padx=10, column='3', row='0')
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
        
        #GET TODAYS MONTH NAME
        monthname=dt.datetime.now().strftime("%B")
        self.spn_month = ttk.Spinbox(self.lbfr_Acc_Chart,
                                     values =("January","February","March",
                                              "April","May", "June",
                                              "July","August","September",
                                              "October","November","December"))
        
        self.spn_month.delete('0','end')
        self.spn_month.insert('0',monthname)
        self.spn_month.grid(column='0',row='0')
        
        self.btn_Update = ttk.Button(self.lbfr_Acc_Chart)
        self.btn_Update.configure(text='Update', width='15')
        self.btn_Update.configure(command=self.chartSpendingsMonth)
        self.btn_Update.grid(column='1',row='0')
        
        ### TRANSACTIONS TAB
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
        self.label1.master.rowconfigure('2', pad='5')
        self.label1.master.columnconfigure('0', pad='10')
        self.cmb_tr_Category = ttk.Combobox(self.lbfr_drTransactions)
        self.cmb_tr_Category.grid(column='1', row='2', sticky='ew')
        self.lbfr_drTransactions.configure(height='0', padding='0 0 20 0', text='Choose date range')  #
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
        
        self.tbl_transactions_cols = [ 'id', 'date', 'amount', 'cat', 'cont' ]
        self.tbl_transactions_dcols = [      'date', 'amount', 'cat', 'cont' ]
        self.tbl_transactions.configure(columns=self.tbl_transactions_cols, 
                                        displaycolumns=self.tbl_transactions_dcols,
                                        yscrollcommand=self.scrb_trTableVert.set)
        self.tbl_transactions.column('id',      anchor='w',stretch='true',width='50',minwidth='20')
        self.tbl_transactions.column('date',    anchor='w',stretch='true',width='180',minwidth='20')
        self.tbl_transactions.column('amount',  anchor='w',stretch='true',width='180',minwidth='20')
        self.tbl_transactions.column('cat',     anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.column('cont',    anchor='w',stretch='true',width='200',minwidth='20')
        self.tbl_transactions.heading('id',       anchor='w',text='ID')
        self.tbl_transactions.heading('date',     anchor='w',text='Date')
        self.tbl_transactions.heading('amount',   anchor='w',text='Amount')
        self.tbl_transactions.heading('cat',      anchor='w',text='Category')
        self.tbl_transactions.heading('cont',     anchor='w',text='Contractor')
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
        
        
        ### CATEGORIES TAB
        self.frm_categories = ttk.Frame(self.ntb_app)
        self.lbfr_tableCategories = ttk.Labelframe(self.frm_categories)
        # table
        self.tbl_categories = ttk.Treeview(self.lbfr_tableCategories)
        self.scrb_catTableVert = ttk.Scrollbar(self.lbfr_tableCategories)
        self.scrb_catTableVert.configure(orient='vertical', takefocus=False)
        self.scrb_catTableVert.grid(column='1', row='0', sticky='ns')
        self.scrb_catTableVert.configure(command=self.tbl_categories.yview)
        self.tbl_categories_cols = ['id', 'name']
        self.tbl_categories_dcols = [     'name']
        self.tbl_categories.configure(columns=self.tbl_categories_cols, 
                                      displaycolumns=self.tbl_categories_dcols,
                                      yscrollcommand=self.scrb_catTableVert.set)
        self.tbl_categories.column('id', anchor='w',stretch='false',width='40',minwidth='40')
        self.tbl_categories.column('name', anchor='w',stretch='true',width='200',minwidth='200')
        self.tbl_categories.heading('id', anchor='w',text='ID')
        self.tbl_categories.heading('name', anchor='w',text='Name')
        self.tbl_categories['show'] = 'headings'
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
        
        self.lbfr_cat_data.configure(height='0', text='Data for operations')
        self.lbfr_cat_data.grid(column='0', ipadx='0', ipady='0', padx='5', pady='0', row='0', sticky='nsew')
        self.lbfr_cat_data.master.rowconfigure('0', pad='10', weight=0)
        self.lbfr_cat_data.master.columnconfigure('0', pad='0', weight=1)
        self.frm_categories.grid(column='0', padx='3', pady='10', row='0', sticky='nsew')
        self.frm_categories.master.rowconfigure('0', weight=1)
        self.frm_categories.master.columnconfigure('0', weight=1)
        self.ntb_app.add(self.frm_categories, text='Categories	')
        
        
        ### LOTTO TAB
        self.frm_lotto = ttk.Frame(self.ntb_app)
        self.lbfr_weather = ttk.Labelframe(self.frm_lotto)
        self.var_Calendar = tk.StringVar(value='--.--.----')
        self.calendar = tkcal.Calendar(self.lbfr_weather, 
                                       selectmode='day', date_pattern=_cal_datefmt,
                                       textvariable=self.var_Calendar)
        self.calendar.grid(column='0', padx='10', pady='10', row='2')
        self.lbfr_weather.configure(text='Calendar')
        self.lbfr_weather.grid(column='0', row='0', sticky='nsew')
        self.labelframe5 = ttk.Labelframe(self.frm_lotto)
        self.label6 = ttk.Label(self.labelframe5)
        self.label6.configure(justify='center', text='weather, icon, location')
        self.label6.grid(column='0', row='0', 
                         columnspan='2', sticky='',
                         pady=20)
        # time
        self.lbl_lt_time = ttk.Label(self.labelframe5)
        self.lbl_lt_time.configure(justify='center', text='Current time:')
        self.lbl_lt_time.grid(column='0', row='1', sticky='e')
        self.label7 = ttk.Label(self.labelframe5)
        self.var_CurrentTime = tk.StringVar(value='eeef')
        self.label7.configure( font='{Arial} 16 {}', foreground='black', justify='center')
        self.label7.configure(textvariable=self.var_CurrentTime, width='20')
        self.label7.grid(column='1', row='1', pady=10)
        # date
        self.lbl_lt_date = ttk.Label(self.labelframe5)
        self.lbl_lt_date.configure(justify='center', text='Selected date:')
        self.lbl_lt_date.grid(column='0', row='2', sticky='e')
        self.lbl_lt_cal = ttk.Label(self.labelframe5)
        self.lbl_lt_cal.configure(font='{Arial} 16 {}', foreground='black', justify='center')
        self.lbl_lt_cal.configure(textvariable=self.var_Calendar, width='20')
        self.lbl_lt_cal.grid(column='1', row='2')
        #
        self.labelframe5.configure(text='Weather')
        self.labelframe5.grid(column='1', row='0', sticky='nsew')
        self.labelframe5.master.columnconfigure('1', weight=1)
        self.frm_lotto.grid(column='0', row='0', sticky='nsew')
        self.frm_lotto.master.rowconfigure('0', weight=1)
        self.frm_lotto.master.columnconfigure('0', weight=1)
        self.ntb_app.add(self.frm_lotto, text='Bells and whistlers')
        
        
        ### NOTEBOOK GRID ...
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
        ### 
        return self.root_app


if __name__ == '__main__':
    
    app = AppWin()
    app.run()
   


