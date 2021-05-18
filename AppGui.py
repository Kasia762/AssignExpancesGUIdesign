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
from addCategory import AddCategory
from addContractors import AddContractor
import ChoosePeriod
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import app_import
from weather import Weather
import lotto
import matplotlib.dates as mdates

import base64
import tkinter as tk
from urllib.request import urlopen
from PIL import ImageTk,Image

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
        
        self.dpi = self.mainwindow.winfo_fpixels('1i')
        print(f"Current dpi is set to {self.dpi}")
        
        
        fig = plt.figure(dpi=self.dpi)
        self.ax1 = fig.add_subplot(111)
        self.chart1 = FigureCanvasTkAgg(fig, self.lbfr_Acc_Chart)
        self.chart1.get_tk_widget().grid(padx='0',pady='10',
                column="0", row="0", sticky = 'nsew')
    
        fig = plt.figure(dpi=self.dpi)
        self.ax2 = fig.add_subplot(111)
        self.chart2 = FigureCanvasTkAgg(fig, self.frm_cat_chart)
        self.chart2.get_tk_widget().grid(sticky='nsew', column="0",row="0")
        
        
        
    def getWeatherInfo(self):
        city = self.ent_ch_city.get()
        try:
            x = Weather(city)
            self.var_wt_location.set("Location : "+x.Location())
            self.var_wt_tempNum.set(x.Temperature())
            self.var_wt_type.set(x.Type())
            self.var_wt_windVal.set(x.WindSpeed())
            self.var_wt_pressureVal.set(x.Pressure())
            self.var_wt_tMinVal.set(x.TempMin())
            self.var_wt_tMaxVal.set(x.TempMax())
            self.var_wt_humidityVal.set(x.Humidity())
            
            img = tk.PhotoImage(data=x.Icon())
            self.lbl_wt_icon.configure(image=img)
            self.lbl_wt_icon.image= img
        except:
             tk.messagebox.showwarning("Wrong input city name!!",
                                      "This city name is incorrect.\n\nPlease, give correct city name.",
                                      parent=self.mainwindow)    
        
        
    def cat_spn_chooseMonth(self):
        mon =self.spn_month.get()
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
        today = dt.date.today().replace(month=int(getmonth()))
        start = today.replace(day=1)
        end=today.replace(day=28)+dt.timedelta(days=4)
        end = end - dt.timedelta(days = end.day)
        self.chartCategorySpendings(start, end)
        

    
    def chartCategorySpendings(self, start, end):
        amount = 0
        category = 1
        data = self.badb.data_chartCategories(start, end)
        am = [abs(i[amount]) for i in data]
        cat=[i[category] for i in data]

        try: 
            cat[cat.index(None)] = "Undefined"
        except: 
            print("no none categories")
            
        start = start.strftime(_dt_datefmt)
        end = end.strftime(_dt_datefmt)
        self.ax2.clear()
        self.ax2.bar(cat,height=am)
        self.ax2.set_title("Spendings from: "+start+" to: "+ end)
        self.ax2.set_xlabel("Categories")
        self.ax2.set_ylabel("Spendings [Euros]")
        self.chart2.draw()
        
        
    def chartOverallSpendings(self):
        today = dt.date.today()
        start = today.replace(day=1)
        end=today.replace(day=28)+dt.timedelta(days=4)
        end = end - dt.timedelta(days = end.day)
        
        self.display_balance(start, end)
        self.display_amountIn(start, end)
        self.display_amountOut(start, end)
        
        income = self.badb.data_chartIncome(start,end)
        outcome = self.badb.data_chartOutcome(start,end)
        balance = self.badb.data_chartBalance(start,end)
        #print(i[0] for i in amount)
        am_income = [i[0] for i in income] 
        am_outcome = [abs(i[0]) for i in outcome ]
        am_balance = [i[0] for i in balance]
        
        date_income = [(i[1].strftime(_dt_datefmt)) for i in income]
        date_outcome = [(i[1].strftime(_dt_datefmt)) for i in outcome]
        date_balance = [(i[1].strftime(_dt_datefmt)) for i in balance]
        
        date_income = [str(i[1]) for i in income]
        date_outcome = [str(i[1]) for i in outcome]
        date_balance = [str(i[1]) for i in balance]
    
        date_income = mdates.datestr2num(date_income)
        date_outcome = mdates.datestr2num(date_outcome)
        date_balance = mdates.datestr2num(date_balance)
    
        self.ax1.clear()
        self.ax1.plot(date_income, am_income, 
                      color='green', label='income', marker = '*')
        self.ax1.plot(date_outcome, am_outcome, 
                      color = 'red',label='outcome', marker = '.')
        
        self.ax1b = self.ax1.twinx()
        self.ax1b.clear()
        self.ax1b.bar(date_balance, am_balance, 
                       color = 'PaleGreen', label="balance", alpha = 0.4)
    
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter(_dt_datefmt))
        self.ax1b.xaxis.set_major_formatter(mdates.DateFormatter(_dt_datefmt))
        
        start = start.strftime(_dt_datefmt)
        end = end.strftime(_dt_datefmt)
        self.ax1.set_title("Overall spendings for period: "+\
                  str(start)+" ---> "+str(end),
                  y=1.04, loc="center")
        self.ax1.set_xlabel("Dates")
        self.ax1.set_ylabel("Balance [Euros]")
        self.ax1b.set_ylabel("Income/outcome [Euros]")
        
        self.ax1.legend( bbox_to_anchor=(0,1.08), 
                   loc="center")
        self.ax1b.legend( bbox_to_anchor=(1,1.05), 
                   loc="center")
        
        self.ax1b.grid(b=True, which='major', color='#999999', 
                       linestyle='--', linewidth = 0.8, alpha=0.2)
        self.ax1.grid(axis='x', linestyle='--', linewidth = 0.8)
        plt.gcf().autofmt_xdate()
        
        self.ax1.tick_params(axis='x', labelrotation=10)
        plt.tight_layout(pad=5, w_pad=5 , h_pad=5)
        
        self.chart1.draw()
    
        
    def updateTransactionTable(self):
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
        # ***  
        self.chartOverallSpendings()


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
            
            
    def updateContractorsTable(self):
        #first clear the treeview
        for item in  self.tbl_contractors.get_children():
             self.tbl_contractors.delete(item)
        #then display data
        data = self.badb.getContractorList()
        for row in data:
            contr = row[0] if row[0] else ""
            _id = row[1] if row[1] else ""
            values = (_id, contr)
            self.tbl_contractors.insert('','end', values = values)      
            

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
        exportingitems = self.tbl_transactions.get_children()
        ## Export choose: selected or all
        selected = self.tbl_transactions.selection()
        if len(selected) > 1:
            print("Multi selection in table. Choose dialog pop-up.")
            reply =  tk.messagebox.askyesno(title="Export...", 
                           message=f"There are {len(selected)} transactions selected in table." + 
                           "Choose what should be exported:\n\n" + 
                           "\tPress YES to export only selected.\n"
                           "\tPress NO to export whole table.")
            if reply == True:
                exportingitems = selected
        else:
            print("Nothing selected or only one line. Intend to export whole table.")
        
        filetypes = (
            ('CSV files', '*.csv'),
            #('Excel files', '*.xlsx'),
            ('All files', '*.*'))
        exportFileName = "_".join(
                        ("Export",
                        self.cal_tr_From.get_date().strftime(_dt_datefmt),
                        self.cal_tr_To.get_date().strftime(_dt_datefmt) ))
        try:
            exportFileName = tk.filedialog.asksaveasfile(
                            title="Export current table view as...",
                            initialdir='./',
                            filetypes=filetypes,
                            defaultextension='.csv',
                            initialfile=exportFileName,
                            parent=self.mainwindow  )
        except PermissionError as err:
            print("Error: %s" %err)
            tk.messagebox.showerror("CSV export",
                        "Could not export: file writing error.\n\nPlease check file not used in other program.",
                        parent=self.mainwindow)
            return
        except:
            print("Some problem selecting file.")
            return
        print("Selected filename for export: ", exportFileName.name )
        try:
            export_df = pd.DataFrame(None, columns=self.tbl_transactions_cols)
            for row in exportingitems:
                ## each row will come as a list under name "values" 
                rowvals = pd.DataFrame([self.tbl_transactions.item(row)['values']], 
                            columns=self.tbl_transactions_cols)
                export_df = export_df.append(rowvals)
            ## shrink dataframe to visible columns (no id of transaction)
            export_df = export_df[self.tbl_transactions_dcols]
        except:
            print("Unexpected error: cannot retrieve data from table.")
            tk.messagebox.showerror("CSV export",
                                    "Could not export: internal error",
                                    parent=self.mainwindow)
            return
        try:
            ## apply datetime format
            export_df.loc[:,'date'] = export_df.loc[:,'date'].apply(lambda x: dt.datetime.strptime(x, _dt_datefmt))
            export_df.to_csv(exportFileName, index = False)
        except:
            print("Unexpected error: cannot save data to csv.")
            tk.messagebox.showerror("CSV export",
                        "Could not export: file writing error.\n\nPlease check file not used in other program",
                        parent=self.mainwindow)
            return
        tk.messagebox.showinfo("CSV export",
                               "Export complete.",
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
        AddCategory(self.mainwindow, self)        


    def h_btnCatChange(self):
        selected = self.tbl_categories.selection()
        print(selected)
        if len(selected) > 1:
            print("Multi selection in table. Cannot change several transactions yet.")
            tk.messagebox.showwarning("Change transaction",
                                   "Multi selection in table.\n\n Cannot change several transactions at once yet.",
                                      parent=self.mainwindow)
            return
        elif len(selected) == 1:
            print("One-line selection.")
            id_value = str(self.tbl_categories.item(selected, 'values')[0])
            print('Opening addTransaction window in "change" mode, id: ', id_value)
            AddCategory(self.mainwindow, self, id_value)
            self.updateCategoriesTable()
        else:
            print("Nothing selected in table. Cannot change.")
            tk.messagebox.showwarning("Change transaction","Select transaction in table to change.",
                                      parent=self.mainwindow)


    def h_btnContractorsAdd(self):
        AddContractor(self.mainwindow, self)
    
    
    def h_btnContractorsChange(self):
        selected = self.tbl_contractors.selection()
        print(selected)
        if len(selected) > 1:
            print("Multi selection in table. Cannot change several transactions yet.")
            tk.messagebox.showwarning("Change transaction",
                                   "Multi selection in table.\n\n Cannot change several transactions at once yet.",
                                      parent=self.mainwindow)
            return
        elif len(selected) == 1:
            print("One-line selection.")
            id_value = str(self.tbl_contractors.item(selected, 'values')[0])
            print('Opening addTransaction window in "change" mode, id: ', id_value)
            AddContractor(self.mainwindow, self, id_value)
            self.updateContractorsTable()
        else:
            print("Nothing selected in table. Cannot change.")
            tk.messagebox.showwarning("Change transaction","Select transaction in table to change.",
                                      parent=self.mainwindow)

               
    def display_time(self):
        self.var_wt_CurrentTime.set( value= time.strftime('%H:%M:%S') )
        self.mainwindow.after(1000, self.display_time)     


    def display_balance(self, start, end):
        ## TODO: not by after
        val = self.badb.getBalance(start,end)
        self.var_CurrentBalance.set( value= f"{val:.2f}" )
        
        
    def display_amountIn(self, start, end):
        ## TODO: not by after
        val = self.badb.getAmountIn(start, end)
        self.var_perAmountIn.set( value= f"{val:.2f}" )
        
        
    def display_amountOut(self, start, end):
        val = self.badb.getAmountOut(start, end)
        self.var_perAmountOut.set( value= f"{val:.2f}" )
    

    def run(self):
        self.updateTransactionTable()
        self.updateCategoriesTable()
        self.updateContractorsTable()
        self.display_time()
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
        self.lbl_balance.configure(text='Balance/Savings:')
        self.lbl_balance.grid(column='0', padx='10', pady='5', row='0')
        self.lbl_percentage = ttk.Label(self.lbfr_account)
        self.var_CurrentBalance = tk.StringVar(value="...")
        self.lbl_percentage.configure(font='{Arial} 12 {bold}', textvariable=self.var_CurrentBalance)
        self.lbl_percentage.grid(column='1', row='0')
        self.progressbar = ttk.Progressbar(self.lbfr_account)
        self.progressbar.configure(orient='horizontal')
        self.progressbar.grid(column='2', padx='10', row='0', sticky='ew')
        self.progressbar.master.columnconfigure('2', weight=1)
        self.lbl_amountIn = ttk.Label(self.lbfr_account)
        self.lbl_amountIn.configure(text='Amount in:')
        self.lbl_amountIn.grid(column='0', padx='10', pady='5', row='1')
        self.lbl_perAmountIn = ttk.Label(self.lbfr_account)
        self.var_perAmountIn = tk.StringVar(value="...")
        self.lbl_perAmountIn.configure(font='{Arial} 12 {bold}', textvariable=self.var_perAmountIn)
        self.lbl_perAmountIn.grid(column='1', row='1')
        self.lbl_amountOut = ttk.Label(self.lbfr_account)
        self.lbl_amountOut.configure(text='Amount Out:')
        self.lbl_amountOut.grid(column='2', padx='10', pady='5', row='1')
        self.lbl_perAmountOut = ttk.Label(self.lbfr_account)
        self.var_perAmountOut = tk.StringVar(value="...")
        self.lbl_perAmountOut.configure(font='{Arial} 12 {bold}', textvariable=self.var_perAmountOut)
        self.lbl_perAmountOut.grid(column='3', row='1')
        
        
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
        self.lbfr_Acc_Chart.grid(column='0', ipadx='10', ipady='10', 
                                 row='1', sticky='nsew')
        self.lbfr_Acc_Chart.rowconfigure('0', weight=1)
        self.lbfr_Acc_Chart.columnconfigure('0', weight=1)
    
        self.frm_account.grid(column='0', row='0', sticky='nsew')
        self.frm_account.rowconfigure('0', weight=0)
        self.frm_account.rowconfigure('1', weight=1)
        self.frm_account.columnconfigure('0', weight=1)
        
        self.ntb_app.add(self.frm_account, sticky='nsew', text='Account')
    
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
        #_text_ = dt.date.today().replace(day=1).strftime(_dt_datefmt)
        firstDay = dt.date.today().replace(day=1)
        date = firstDay.strftime(_dt_datefmt)
        # self.cal_tr_From.delete('0', 'end')
        # self.cal_tr_From.insert('0', date)
        self.cal_tr_From.set_date(date)
        
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
        today =  dt.date.today().strftime(_dt_datefmt)
        self.cal_tr_To.delete('0', 'end')
        self.cal_tr_To.insert('0', today)
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
        self.lbfr_tableContractors = ttk.Labelframe(self.frm_categories)
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
        self.tbl_categories.column('name', anchor='w',stretch='true',width='200',minwidth='150')
        self.tbl_categories.heading('id', anchor='w',text='ID')
        self.tbl_categories.heading('name', anchor='w',text='Name')
        self.tbl_categories['show'] = 'headings'
        self.tbl_categories.grid(column='0', padx='3', pady='3', row='0', sticky='nsew')
        self.tbl_categories.master.rowconfigure('0', weight='1')
        self.tbl_categories.master.columnconfigure('0', weight='0')
        self.lbfr_tableCategories.configure(text='Categories')
        self.lbfr_tableCategories.grid(column='0', 
                                       #columnspan='2', 
                                       padx='5', row='1', sticky='nsw')
        self.lbfr_tableCategories.master.rowconfigure('1', weight='1')
        self.lbfr_tableCategories.master.columnconfigure('0', pad='0', weight='1')
        
        ########CONTRACTORS
        self.tbl_contractors = ttk.Treeview(self.lbfr_tableContractors)
        self.scrb_contrTableVert = ttk.Scrollbar(self.lbfr_tableContractors)
        self.scrb_contrTableVert.configure(orient='vertical', takefocus=False)
        self.scrb_contrTableVert.grid(column='1', row='0', sticky='ns')
        self.scrb_contrTableVert.configure(command=self.tbl_contractors.yview)
        self.tbl_contractors_cols = ['id', 'name']
        self.tbl_contractors_dcols = [     'name']
        self.tbl_contractors.configure(columns=self.tbl_contractors_cols, 
                                      displaycolumns=self.tbl_contractors_dcols,
                                      yscrollcommand=self.scrb_contrTableVert.set)
        self.tbl_contractors.column('id', anchor='w',stretch='false',width='40',minwidth='40')
        self.tbl_contractors.column('name', anchor='w',stretch='true',width='200',minwidth='150')
        self.tbl_contractors.heading('id', anchor='w',text='ID')
        self.tbl_contractors.heading('name', anchor='w',text='Name')
        self.tbl_contractors['show'] = 'headings'
        self.tbl_contractors.grid(column='0', padx='3', pady='3', row='0', sticky='nsew')
        #self.tbl_categories.master.rowconfigure('0', weight='1')
        #self.tbl_categories.master.columnconfigure('0', weight='0')
        self.lbfr_tableContractors.configure(text="Contractors")
        self.lbfr_tableContractors.grid(column='0', 
                                       #columnspan='2', 
                                       padx='5', row='2', sticky='nsw')
        #self.lbfr_tableContractors.master.rowconfigure('1', weight='1')
        self.lbfr_tableContractors.master.columnconfigure('0', pad='0', weight='1')
        ########CONTRACTORS 
        
        self.lbfr_cat_Commands = ttk.Labelframe(self.frm_categories)
        self.btn_catAdd = ttk.Button(self.lbfr_cat_Commands)
        self.btn_catAdd.configure(text='Add category', width='20')
        self.btn_catAdd.grid(column='0', row='0')
        self.btn_catAdd.master.rowconfigure('0', pad='10')
        self.btn_catAdd.master.columnconfigure('0', pad='10')
        self.btn_catAdd.configure(command=self.h_btnCatAdd)
        self.btn_catChange = ttk.Button(self.lbfr_cat_Commands)
        self.btn_catChange.configure(text='Change category', width='20')
        self.btn_catChange.grid(column='0', row='1')
        # self.btn_catChange.master.rowconfigure('1', pad='10')
        # self.btn_catChange.master.columnconfigure('0', pad='10')
        self.btn_catChange.configure(command=self.h_btnCatChange)
        
        self.btn_addContractors = ttk.Button(self.lbfr_cat_Commands)
        self.btn_addContractors.configure(text='Add contractors', width='20')
        self.btn_addContractors.grid(column='0', row='2')
        self.btn_addContractors.master.rowconfigure('2', pad='10')
        self.btn_addContractors.master.columnconfigure('0', pad='10')
        self.btn_addContractors.configure(command=self.h_btnContractorsAdd)
        
        self.btn_changeContractors = ttk.Button(self.lbfr_cat_Commands)
        self.btn_changeContractors.configure(text='Change contractors', width='20')
        self.btn_changeContractors.grid(column='0', row='3')
        self.btn_changeContractors.master.rowconfigure('2', pad='10')
        self.btn_changeContractors.master.columnconfigure('0', pad='10')
        self.btn_changeContractors.configure(command=self.h_btnContractorsChange)
        
        self.lbfr_cat_Commands.configure(height='0', text='Commands', width='200')
        self.lbfr_cat_Commands.grid(column='0', padx='5', row='0', sticky='nsew')
        #self.lbfr_cat_Commands.master.rowconfigure('0', pad='10', weight=0)
        self.lbfr_cat_Commands.columnconfigure('0', weight = 1)
        # self.lbfr_cat_Commands.rowconfigure('0', weight = 1)
        # self.lbfr_cat_Commands.rowconfigure('1', weight = 1)
        
        
        ########FRAME FOR PERIOD CHOSER
        
        self.frm_chooseDate = ttk.Frame(self.frm_categories)
        self.choosePeriod = ChoosePeriod.PeriodChooserWidget(self.frm_chooseDate)
        self.choosePeriod.grid(column = '1', row = '0')
        # self.cat_monthname=dt.datetime.now().strftime("%B")
        # self.spn_month = ttk.Spinbox(self.lbfr_cat_data,
        #                               values =("January","February","March",
        #                                       "April","May", "June",
        #                                       "July","August","September",
        #                                       "October","November","December"),
        #                               command=self.cat_spn_chooseMonth)
        # self.spn_month.delete('0','end')
        # self.spn_month.insert('0',self.cat_monthname)
        # self.spn_month.grid(column='0',row='0', columnspan = "4",ipady='7')
        # self.btn_prevMonth = ttk.Button(self.lbfr_cat_data)
        # self.btn_prevMonth.configure(text='<< Previous Month', width='15')
        # self.btn_prevMonth.configure(command=self.cat_btn_previousMonth)
        # self.btn_prevMonth.grid(column='0',row='1', sticky='we')
        # self.btn_currentMonth = ttk.Button(self.lbfr_cat_data)
        # self.btn_currentMonth.configure(text='Current Month', width='15')
        # self.btn_currentMonth.configure(command=self.cat_btn_currentMonth)
        # self.btn_currentMonth.grid(column='1',row='1', sticky='we')
        # self.btn_currentWeek = ttk.Button(self.lbfr_cat_data)
        # self.btn_currentWeek.configure(text='Current Week', width='15')
        # self.btn_currentWeek.configure(command=self.cat_btn_currentWeek)
        # self.btn_currentWeek.grid(column='3',row='1', sticky='we')
        # self.btn_previousWeek = ttk.Button(self.lbfr_cat_data)
        # self.btn_previousWeek.configure(text='<<Previous Week', width='15')
        # self.btn_previousWeek.configure(command=self.cat_btn_previousWeek)
        # self.btn_previousWeek.grid(column='2',row='1', sticky='we')
        self.frm_chooseDate.grid(column='1',padx='5',row='0', sticky='nsew')
            
    
        self.frm_cat_chart = ttk.Frame(self.frm_categories)
        self.frm_cat_chart.grid(column = '1', row = '1', sticky = 'nsew',
                                padx=10, pady=10, rowspan='3')
        self.frm_cat_chart.columnconfigure('0', weight=1)
        self.frm_cat_chart.rowconfigure('0', weight=1)
    
        
        self.frm_categories.grid(column='0', padx='5', pady='10', row='0', sticky='nsew')
        
        self.frm_categories.rowconfigure('0', weight=0, pad="10")
        self.frm_categories.columnconfigure('0', weight=0)
        #self.frm_categories.rowconfigure('1', weight = 1)
        self.frm_categories.columnconfigure('1', weight=1)
        
        self.ntb_app.add(self.frm_categories, text='Categories and contractors')
        
        ### LOTTO TAB
        self.frm_bells = ttk.Frame(self.ntb_app)
        
        self.lbfr_bells_choose = ttk.Labelframe(self.frm_bells)
        
        self.lbl_ch_city = ttk.Label(self.lbfr_bells_choose)
        self.lbl_ch_city.configure(text='Please, write the city name in the box')
        self.lbl_ch_city.grid(column='0', padx='5', pady='10', row='0', sticky='e')
        self.lbl_ch_city.rowconfigure('0', pad='0', weight='0')
        self.lbl_ch_city.columnconfigure('0', pad='0')
        
        self.ent_ch_city = ttk.Entry(self.lbfr_bells_choose)
        self.ent_ch_city.grid(column='1', ipadx='20', row='0', sticky='ew')
        self.ent_ch_city.rowconfigure('0', pad='0', weight='0')
        self.ent_ch_city.columnconfigure('1', weight='1')
        
        self.btn_ch_city = ttk.Button(self.lbfr_bells_choose)
        self.btn_ch_city.configure(takefocus=False, text='Confirm', width='15')
        self.btn_ch_city.grid(column='2', row='0')
        self.btn_ch_city.rowconfigure('0', pad='0', weight='0')
        self.btn_ch_city.columnconfigure('2', pad='20', weight='0')
        self.btn_ch_city.configure(command=self.getWeatherInfo)
        
        self.lbfr_bells_choose.configure(height='200', padding='30 0', text='Choose city for which you want to have information displayed', width='200')
        self.lbfr_bells_choose.grid(column='0', padx='5', pady='0', row='0', sticky='n')
        self.lbfr_bells_choose.rowconfigure('0', pad='0', weight='1')
        self.lbfr_bells_choose.columnconfigure('0', pad='0', weight='1')
        
        self.lblfr_bells_weather = ttk.Labelframe(self.frm_bells)
        
        self.frm_wt_location = ttk.Frame(self.lblfr_bells_weather)
        self.lbl_wt_location = ttk.Label(self.frm_wt_location)
        self.var_wt_location = tk.StringVar(value='Please, enter the city name above')
        self.lbl_wt_location.configure(font='{Arial} 16 {}', text='Please, enter the city name above', textvariable=self.var_wt_location)
        self.lbl_wt_location.grid(column='0', pady='20', row='0', sticky='ew')
        self.lbl_wt_location.columnconfigure('0', weight='0')
        self.frm_wt_location.configure(height='200', width='200')
        self.frm_wt_location.grid(column='0', columnspan='2', row='0', sticky='n')
        self.frm_wt_location.columnconfigure('0', weight='1')
        
        self.frm_wt_values = ttk.Frame(self.lblfr_bells_weather)
        
        self.lbl_wt_type = ttk.Label(self.frm_wt_values)
        self.var_wt_type = tk.StringVar(value='UNKNOWN')
        self.lbl_wt_type.configure(text='UNKNOWN', textvariable=self.var_wt_type)
        self.lbl_wt_type.grid(column='0', padx='20', pady='5', row='1')
        self.lbl_wt_type.columnconfigure('0', weight='0')
        
        self.lbl_wt_temperature = ttk.Label(self.frm_wt_values)
        self.lbl_wt_temperature.configure(text='Temperature')
        self.lbl_wt_temperature.grid(column='1', padx='10', pady='5', row='1', sticky='sew')
        
        self.lbl_wt_icon = ttk.Label(self.frm_wt_values)
        img = Image.open('pig1.ico')
        img = img.resize((50, 50), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.lbl_wt_icon.configure(image = img)
        self.lbl_wt_icon.image = img
        self.lbl_wt_icon.grid(column='0', ipady = '10', padx='20', row='2', sticky='nsew')
                
        self.lbl_wt_tempNum = ttk.Label(self.frm_wt_values)
        
        self.var_wt_tempNum = tk.StringVar(value='???')
        img = Image.open('temp.ico')
        img = img.resize((50, 50), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.lbl_wt_tempNum.configure(image = img)
        self.lbl_wt_tempNum.image = img
        self.lbl_wt_tempNum.configure(font='{Arial} 16 {}', textvariable=self.var_wt_tempNum)
        self.lbl_wt_tempNum.grid(column='1', row='2')
        
        self.lbl_wt_wind = ttk.Label(self.frm_wt_values)
        self.lbl_wt_wind.configure(text='Wind')
        self.lbl_wt_wind.grid(column='0', padx='20', pady='5', row='3', sticky='se')
        self.lbl_wt_wind.rowconfigure('3', minsize='0', pad='40')
        self.lbl_wt_wind.columnconfigure('0', weight='0')
        
        self.lbl_wt_windVal = ttk.Label(self.frm_wt_values)
        self.var_wt_windVal = tk.StringVar(value='UNKNOWN')
        self.lbl_wt_windVal.configure(text='UNKNOWN', textvariable=self.var_wt_windVal)
        self.lbl_wt_windVal.grid(column='1', padx='10', pady='5', row='3', sticky='sw')
        self.lbl_wt_windVal.rowconfigure('3', minsize='0', pad='40')
        
        self.lbl_wt_pressure = ttk.Label(self.frm_wt_values)
        self.lbl_wt_pressure.configure(text='Pressure')
        self.lbl_wt_pressure.grid(column='0', padx='20', pady='5', row='4', sticky='e')
        self.lbl_wt_pressure.columnconfigure('0', weight='0')
        
        self.lbl_wt_pressureVal = ttk.Label(self.frm_wt_values)        
        self.var_wt_pressureVal = tk.StringVar(value='UNKNOWN')
        self.lbl_wt_pressureVal.configure(text='UNKNOWN', textvariable=self.var_wt_pressureVal)
        self.lbl_wt_pressureVal.grid(column='1', padx='10', pady='5', row='4', sticky='w')
        
        self.lbl_wt_tMax = ttk.Label(self.frm_wt_values)
        self.lbl_wt_tMax.configure(text='Temp.max')
        self.lbl_wt_tMax.grid(column='0', padx='20', pady='5', row='5', sticky='e')
        self.lbl_wt_tMax.rowconfigure('5', minsize='0')
        self.lbl_wt_tMax.columnconfigure('0', weight='0')
        self.lbl_wt_tMaxVal = ttk.Label(self.frm_wt_values)
        self.var_wt_tMaxVal = tk.StringVar(value='UNKNOWN')
        self.lbl_wt_tMaxVal.configure(text='UNKNOWN', textvariable=self.var_wt_tMaxVal)
        self.lbl_wt_tMaxVal.grid(column='1', padx='10', pady='5', row='5', sticky='w')
        self.lbl_wt_tMaxVal.rowconfigure('5', minsize='0')
        
        self.lbl_wt_tMin = ttk.Label(self.frm_wt_values)
        self.lbl_wt_tMin.configure(text='Temp.min')
        self.lbl_wt_tMin.grid(column='0', padx='20', pady='5', row='6', sticky='e')
        self.lbl_wt_tMin.columnconfigure('0', weight='0')
        self.lbl_wt_tMinVal = ttk.Label(self.frm_wt_values)
        self.var_wt_tMinVal = tk.StringVar(value='UNKNOWN')
        self.lbl_wt_tMinVal.configure(text='UNKNOWN', textvariable=self.var_wt_tMinVal)
        self.lbl_wt_tMinVal.grid(column='1', padx='10', pady='5', row='6', sticky='w')
        
        self.lbl_wt_humidity = ttk.Label(self.frm_wt_values)
        self.lbl_wt_humidity.configure(text='Humidity')
        self.lbl_wt_humidity.grid(column='0', padx='20', pady='5', row='7', sticky='e')
        self.lbl_wt_humidity.columnconfigure('0', weight='0')
        
        self.lbl_wt_humidityVal = ttk.Label(self.frm_wt_values)
        self.var_wt_humidityVal = tk.StringVar(value='UNKNOWN')
        self.lbl_wt_humidityVal.configure(text='UNKNOWN', textvariable=self.var_wt_humidityVal)
        self.lbl_wt_humidityVal.grid(column='1', padx='10', pady='5', row='7', sticky='w')
        
        self.frm_wt_values.configure(height='200', width='200')
        self.frm_wt_values.grid(column='0', row='1', sticky='nsw')
        #self.frm_wt_values.columnconfigure('0', weight='1')
        
        self.frm_wt_calendar = ttk.Frame(self.lblfr_bells_weather)
        
        self.lbl_wt_today = ttk.Label(self.frm_wt_calendar)
        self.lbl_wt_today.configure(font='{Arial} 12 {}', text='Today is')
        self.lbl_wt_today.grid(column='0', padx='50', pady='10', row='0', sticky='nsw')
        self.lbl_wt_todayDate = ttk.Label(self.frm_wt_calendar)
        self.var_wt_todayDate = tk.StringVar(value='<todays date>')
        #self.var_wt_todayDate = tk.StringVar(value=dt.date.today().strftime(_dt_datefmt))
        self.var_wt_todayDate.set(dt.date.today().strftime(_dt_datefmt))
        self.lbl_wt_todayDate.configure(font='{Arial} 12 {}', text='<todays date>', textvariable=self.var_wt_todayDate)
        self.lbl_wt_todayDate.grid(column='1', row='0', sticky='nsw')
        
        self.lbl_wt_time = ttk.Label(self.frm_wt_calendar)
        self.lbl_wt_time.configure(font='{Arial} 12 {}', text='Time is')
        self.lbl_wt_time.grid(column='0', padx='50', pady='10', row='1', sticky='nsw')
        self.lbl_wt_timeNum = ttk.Label(self.frm_wt_calendar)
        self.var_wt_CurrentTime = tk.StringVar(value='<time>')
        self.lbl_wt_timeNum.configure(font='{Arial} 12 {}', text='<time>', textvariable=self.var_wt_CurrentTime)
        self.lbl_wt_timeNum.grid(column='1', row='1', sticky='nsw')
                
        self.var_Calendar = tk.StringVar(value='--.--.----')
        self.cal_wt = tkcal.Calendar(self.frm_wt_calendar, 
                                       selectmode='day', date_pattern=_cal_datefmt,
                                       textvariable=self.var_Calendar)
        self.cal_wt.grid(column='0', columnspan='2', padx='50', row='2', sticky='s')
        
        # self.cal_wt = CalendarFrame(self.frm_wt_calendar)
        # # TODO - self.cal_wt: code for custom option 'firstweekday' not implemented.
        # # TODO - self.cal_wt: code for custom option 'month' not implemented.
        # self.cal_wt.grid(column='0', columnspan='2', padx='50', row='2', sticky='s')
        self.cal_wt.rowconfigure('2', pad='30')
        
        self.lbl_wt_date = ttk.Label(self.frm_wt_calendar)
        self.lbl_wt_date.configure(font='{Arial} 12 {}', text='Selected date:')
        self.lbl_wt_date.grid(column='0', padx='50', pady='10', row='3', sticky='nsw')
        self.lbl_wt_date.rowconfigure('3', pad='10')
        
        self.lbl_wt_selection = ttk.Label(self.frm_wt_calendar)
        self.var_wt_selection = tk.StringVar(value='<Selected date>')
        self.lbl_wt_selection.configure(font='{Arial} 12 {}', text='<Selected date>', textvariable=self.var_Calendar)
        self.lbl_wt_selection.grid(column='1', row='3', sticky='nsw')
        self.lbl_wt_selection.rowconfigure('3', pad='10')
        
        self.frm_wt_calendar.configure(height='200', width='200')
        self.frm_wt_calendar.grid(column='1', row='1', sticky='n')
        self.frm_wt_calendar.columnconfigure('1', weight='1')
        
        self.lblfr_bells_weather.configure(height='200', padding='30 0', text='Weather', width='200')
        self.lblfr_bells_weather.grid(column='0', ipadx='10', padx='5', pady='5', row='1', sticky='n')
        self.lblfr_bells_weather.rowconfigure('1', weight='1')
        self.lblfr_bells_weather.columnconfigure('0', pad='0', weight='1')
        
        self.frm_bells.configure(height='200', width='200')
        self.frm_bells.grid(column='0', row='0', sticky='nsew')
        # weight = 0, chose lblfr wont resize the row
        self.frm_bells.rowconfigure('0', weight='0')
        self.frm_bells.columnconfigure('0', weight='1')
        
        self.frm_bells.rowconfigure('1', weight='1')        

        self.ntb_app.add(self.frm_bells, text='Bells and whistlers')
        
        
        ### NOTEBOOK GRID ...
        self.ntb_app.configure(style='Toolbutton', takefocus=True)
        self.ntb_app.grid(column='0', padx='5', pady='5', row='0', sticky='nsew')
        self.ntb_app.master.rowconfigure('0', weight=1)
        self.ntb_app.master.columnconfigure('0', weight=1)
        self.root_app.configure(relief='flat')
        self.root_app.geometry('800x600')
        self.root_app.minsize(700, 400)
        self.root_app.resizable(True, True)
        self.root_app.title('Python cash')
        self.root_app.iconbitmap('pig1.ico')
        
        # SHOW window, fully constructed
        self.root_app.deiconify()
        ### 
        return self.root_app


if __name__ == '__main__':
    
    app = AppWin()
    app.run()
   

