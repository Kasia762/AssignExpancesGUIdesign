# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:45:39 2021

@author: kasia
"""

import tkinter.ttk as ttk
import tkcalendar as tkcal
import time
import datetime as dt
import tkinter as tk

## both format should match
_dt_datefmt = "%d.%m.%Y"
_cal_datefmt = "dd.mm.yyyy"

class PeriodChooserWidget(ttk.Frame):
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        # self.lbfrm_pr_inter = ttk.Labelframe(self)
        self.lbl_inter_from = ttk.Label(self)
        self.lbl_inter_from.configure(text='Date from:')
        self.lbl_inter_from.grid(column='0', padx='10', row='1', sticky='w')
        self.lbl_inter_from.rowconfigure('1', pad='0')
        self.lbl_inter_from.columnconfigure('0', pad='0', weight='0')
        self.lbl_inter_to = ttk.Label(self)
        self.lbl_inter_to.configure(text='Date to:')
        self.lbl_inter_to.grid(column='0', padx='10', row='2', sticky='w')
        self.lbl_inter_to.columnconfigure('0', pad='0', weight='0')
        
        self.cal_inter_from = tkcal.DateEntry(self, 
                                      date_pattern=_cal_datefmt,
                                      state="readonly")
        self.cal_inter_from.grid(column='1', pady='5', row='1')
        self.cal_inter_from.rowconfigure('1', pad='0')
        
        self.cal_inter_to = tkcal.DateEntry(self, 
                                      date_pattern=_cal_datefmt,
                                      state="readonly")
        self.cal_inter_to.grid(column='1', pady='5', row='2')
        
        self.spr_inter = ttk.Separator(self)
        self.spr_inter.configure(orient='vertical')
        self.spr_inter.grid(column='2', padx='15', row='0', rowspan='3', sticky='ns')
        self.rbn_inter_week = ttk.Radiobutton(self)
        self.var_date_type = tk.StringVar(value='week')
        self.rbn_inter_week.configure(style='Toolbutton', text='week', value='week', variable=self.var_date_type)
        self.rbn_inter_week.grid(column='3', padx='10', row='1', sticky='ew')
        self.rbn_inter_week.rowconfigure('1', pad='0')
        self.rbn_inter_week.columnconfigure('3', pad='10')
        self.rbn_inter_month = ttk.Radiobutton(self)
        self.rbn_inter_month.configure(style='Toolbutton', text='month', value='month', variable=self.var_date_type)
        self.rbn_inter_month.grid(column='4', padx='10', row='1', sticky='ew')
        self.rbn_inter_month.rowconfigure('1', pad='0')
        self.rbn_inter_month.columnconfigure('4', pad='10')
        self.rbn_inter_year = ttk.Radiobutton(self)
        self.rbn_inter_year.configure(style='Toolbutton', text='year', value='year', variable=self.var_date_type)
        self.rbn_inter_year.grid(column='5', padx='10', row='1', sticky='ew')
        self.rbn_inter_year.rowconfigure('1', pad='0')
        self.rbn_inter_year.columnconfigure('5', pad='10')
        self.btn_inter_prev = ttk.Button(self)
        self.btn_inter_prev.configure(text='<<Previous')
        self.btn_inter_prev.grid(column='3', padx='10', row='2', sticky='ew')
        self.btn_inter_prev.configure(command=self.h_btn_Prev)
        self.btn_inter_current = ttk.Button(self)
        self.btn_inter_current.configure(text='Current')
        self.btn_inter_current.grid(column='4', padx='10', row='2', sticky='ew')
        self.btn_inter_current.configure(command=self.h_btn_Current)
        self.rbn_inter_next = ttk.Button(self)
        self.rbn_inter_next.configure(text='Next>>')
        self.rbn_inter_next.grid(column='5', padx='10', row='2', sticky='ew')
        self.rbn_inter_next.configure(command=self.h_btn_Next)
        self.lbl_inter_chooseperiod = ttk.Label(self)
        self.lbl_inter_chooseperiod.configure(text='Or choose period')
        self.lbl_inter_chooseperiod.grid(column='2', columnspan='6', row='0')
        
        # self.lbl_inter_selection = ttk.Label(self)
        # self.lbl_inter_selection.configure(font='{Arial} 16 {}', text='Selected date from: 12.02.2010 to : 12.03.2021')
        # self.lbl_inter_selection.grid(column='0', columnspan='6', padx='20', pady='20', row='3', sticky='ew')
        # self.lbl_inter_selection.rowconfigure('3', pad='0', weight='0')
        # self.lbl_inter_selection.columnconfigure('0', pad='0', weight='0')
        
        self.lbl_inter_enterinterval = ttk.Label(self)
        self.lbl_inter_enterinterval.configure(text='Enter interval')
        self.lbl_inter_enterinterval.grid(column='0', columnspan='2', pady='1', row='0')
        self.lbl_inter_enterinterval.columnconfigure('0', pad='0', weight='0')
        # self.lbfrm_pr_inter.configure(height='200', text='Choose period', width='200')
        # self.lbfrm_pr_inter.grid(column='0', ipadx='10', padx='10', pady='10', row='0', sticky='new')
        
        # self.lbfrm_pr_inter.master.columnconfigure('0', weight='9')
        # self.lbfrm_pr_inter.master.rowconfigure('0', weight='1')

        #bind calendar entries to function
        self.cal_inter_from.bind('<<DateEntrySelected>>', lambda x: self.get_calEntryDates() )
        self.cal_inter_to.bind('<<DateEntrySelected>>', lambda x: self.get_calEntryDates()  )
        
        
        self.today = dt.date.today()
        self.default_datePeriod()


    def default_datePeriod(self):
        start = self.today.replace(day=1)
        end = self.today.replace(day=28) + \
                 dt.timedelta(days=4) 
        end = end - dt.timedelta(days=end.day)
        self.cal_inter_from.set_date(start)
        self.cal_inter_to.set_date(end)
        #self.set_datePeriod(start, end)
        self.get_calEntryDates()
               
        
    # def set_datePeriod(self, date_from, date_to):
    #     self.lbl_inter_selection.configure(text="Date period: " + str(date_from) + " - " + str(date_to))
        
        
    def get_calEntryDates(self):
        start = self.cal_inter_from.get_date()
        end = self.cal_inter_to.get_date()
        #self.set_datePeriod(start, end)
        self.event_generate('<<PeriodSelected>>')
        
    
    
    def get_datePeriod(self):
        start = self.cal_inter_from.get_date()
        end = self.cal_inter_to.get_date()
        return (start, end)
    
    
    ### TODO : add underscore   
    def previousPeriod(self, start):
        if self.get_chartDateType() == 'month':
            end = start - \
                dt.timedelta(days=start.day)
            start = end.replace(day=1)
        elif self.get_chartDateType() == 'week':
            end = start - \
                dt.timedelta(days=1)
            start = end - \
                dt.timedelta(days=end.weekday())
        elif self.get_chartDateType() == 'year':
            end = start.replace(day=1, month=1)
            end = end - \
                dt.timedelta(days=1)
            start = end.replace(day=1, month =1)
        #self.set_datePeriod(start, end)
        self.cal_inter_from.set_date(start)
        self.cal_inter_to.set_date(end)
        self.get_calEntryDates()
    
    
    def nextPeriod(self, end):
        if self.get_chartDateType() == 'month':
            # date - convert to first day of month
             start = end.replace(day=28) + \
                 dt.timedelta(days=4) 
             start = start.replace(day=1)
             end = start.replace(day=28) + \
                 dt.timedelta(days=4)
             end = end - \
                 dt.timedelta(days=end.day)
        elif self.get_chartDateType() == 'week':
            start = end + \
                dt.timedelta(days=1)
            end = start + \
                dt.timedelta(days = 6)
        elif self.get_chartDateType() == 'year':
            start = end.replace(day=31, month=12) + \
                dt.timedelta(days=1)
            end = start.replace(day=31, month=12)
        else: print("error")
        #self.set_datePeriod(start, end)
        self.cal_inter_from.set_date(start)
        self.cal_inter_to.set_date(end)
        self.get_calEntryDates()
        
        
    def currentPeriod(self):
        if self.get_chartDateType() == 'month':
            self.default_datePeriod()
        elif self.get_chartDateType() == 'week':
            start = self.today - \
                dt.timedelta(days=self.today.weekday())
            end = start + \
                dt.timedelta(days=6)
            self.cal_inter_from.set_date(start)
            self.cal_inter_to.set_date(end)
            self.get_calEntryDates()
            #self.set_datePeriod(start, end)
        elif self.get_chartDateType() == 'year':
            start = self.today.replace(day=1, month=1)
            end = start.replace(day = 31, month=12)
            self.cal_inter_from.set_date(start)
            self.cal_inter_to.set_date(end)
            #self.set_datePeriod(start, end)
            self.get_calEntryDates()
        else: print("error")
        

   
    def get_chartDateType(self):  
        if self.var_date_type.get() == "week":
            return "week"
        elif self.var_date_type.get() == "month":
            return "month"
        elif self.var_date_type.get() == "year":
            return "year"
        else: print("no period type selection")
            
    
    def h_btn_Prev(self):
        start = self.cal_inter_from.get_date()
        end = self.cal_inter_to.get_date()
        self.previousPeriod(start)
        
    
    def h_btn_Next(self):
        start = self.cal_inter_from.get_date()
        end = self.cal_inter_to.get_date()
        self.nextPeriod(end)
    
    
    def h_btn_Current(self):
        
        self.currentPeriod()
    
             
    # def run(self):
    #     #self.default_datePeriod()
    #     pass
        

if __name__ == '__main__':
    root = tk.Tk()
    widget = PeriodChooserWidget(root)
    widget.pack(expand=True, fill='both')
    root.mainloop() 
    # widget.run()
