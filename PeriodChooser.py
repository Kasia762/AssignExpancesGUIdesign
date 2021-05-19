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
        self.lbl_inter_from = ttk.Label(self)
        self.lbl_inter_from.configure(text='From:')
        self.lbl_inter_from.grid(column='0', padx='10', row='1', sticky='e')
        self.lbl_inter_from.master.rowconfigure('1', weight='1')
        self.lbl_inter_from.master.columnconfigure('0', pad='0', weight='0')
        self.lbl_inter_to = ttk.Label(self)
        self.lbl_inter_to.configure(text='To:')
        self.lbl_inter_to.grid(column='2', padx='10', row='1')
        self.lbl_inter_to.master.rowconfigure('1', weight='1')
        self.lbl_inter_to.master.columnconfigure('0', pad='0', weight='0')
        self.cal_inter_from = tkcal.DateEntry(self, 
                                      date_pattern=_cal_datefmt,
                                      state="readonly")
        self.cal_inter_from.grid(column='1', pady='5', row='1', rowspan='2', sticky='w')
        self.cal_inter_from.master.rowconfigure('1', weight='1')
        self.cal_inter_from.master.columnconfigure('1', weight='1')
        self.cal_inter_to = tkcal.DateEntry(self, 
                                      date_pattern=_cal_datefmt,
                                      state="readonly")
        self.cal_inter_to.grid(column='3', pady='5', row='1', rowspan='2', sticky='w')
        self.cal_inter_to.master.rowconfigure('1', weight='1')
        self.cal_inter_to.master.columnconfigure('3', weight='1')
        self.spr_inter = ttk.Separator(self)
        self.spr_inter.configure(orient='vertical')
        self.spr_inter.grid(column='4', padx='15', pady='5', row='0', rowspan='3', sticky='ns')
        self.spr_inter.master.rowconfigure('0', weight='1')
        self.spr_inter.master.columnconfigure('4', weight='1')
        self.rbn_inter_week = ttk.Radiobutton(self)
        self.var_date_type = tk.StringVar(value='month')
        self.rbn_inter_week.configure(style='Toolbutton', text='week', value='week', variable=self.var_date_type)
        self.rbn_inter_week.grid(column='5', padx='10', row='0', sticky='ew')
        self.rbn_inter_week.master.rowconfigure('0', weight='1')
        self.rbn_inter_week.master.columnconfigure('5', weight='1')
        self.rbn_inter_month = ttk.Radiobutton(self)
        self.rbn_inter_month.configure(style='Toolbutton', text='month', value='month', variable=self.var_date_type)
        self.rbn_inter_month.grid(column='6', padx='10', row='0', sticky='ew')
        self.rbn_inter_month.master.rowconfigure('0', weight='1')
        self.rbn_inter_month.master.columnconfigure('6', weight='1')
        self.rbn_inter_year = ttk.Radiobutton(self)
        self.rbn_inter_year.configure(style='Toolbutton', text='year', value='year', variable=self.var_date_type)
        self.rbn_inter_year.grid(column='7', padx='10', row='0', sticky='ew')
        self.rbn_inter_year.master.rowconfigure('0', weight='1')
        self.rbn_inter_year.master.columnconfigure('7', weight='1')
        self.btn_inter_prev = ttk.Button(self)
        self.btn_inter_prev.configure(text='<<Previous')
        self.btn_inter_prev.grid(column='5', padx='10', row='1', sticky='ew')
        self.btn_inter_prev.master.rowconfigure('1', weight='1')
        self.btn_inter_prev.master.columnconfigure('5', weight='1')
        self.btn_inter_prev.configure(command=self.h_btn_Prev)
        self.btn_inter_current = ttk.Button(self)
        self.btn_inter_current.configure(text='Current')
        self.btn_inter_current.grid(column='6', padx='10', row='1', sticky='ew')
        self.btn_inter_current.master.rowconfigure('1', weight='1')
        self.btn_inter_current.master.columnconfigure('6', weight='1')
        self.btn_inter_current.configure(command=self.h_btn_Current)
        self.rbn_inter_next = ttk.Button(self)
        self.rbn_inter_next.configure(text='Next>>')
        self.rbn_inter_next.grid(column='7', padx='10', row='1', sticky='ew')
        self.rbn_inter_next.master.rowconfigure('1', weight='1')
        self.rbn_inter_next.master.columnconfigure('7', weight='1')
        self.rbn_inter_next.configure(command=self.h_btn_Next)
        self.lbl_inter_enterinterval = ttk.Label(self)
        self.lbl_inter_enterinterval.configure(text='Free interval selection')
        self.lbl_inter_enterinterval.grid(column='0', columnspan='4', pady='10', row='0')
        self.lbl_inter_enterinterval.master.rowconfigure('0', weight='1')
        self.lbl_inter_enterinterval.master.columnconfigure('0', pad='0', weight='0')
        self.rowconfigure('0', weight='1')
        self.columnconfigure('8', weight='10')

        ### BINDs
        self.cal_inter_from.bind('<<DateEntrySelected>>', lambda x: self._get_calEntryDates() )
        self.cal_inter_to.bind('<<DateEntrySelected>>', lambda x: self._get_calEntryDates()  )
        
        
        self.today = dt.date.today()
        self._default_datePeriod()


    def _default_datePeriod(self):
        start = self.today.replace(day=1)
        end = self.today.replace(day=28) + \
                 dt.timedelta(days=4) 
        end = end - dt.timedelta(days=end.day)
        self.cal_inter_from.set_date(start)
        self.cal_inter_to.set_date(end)
        #self.set_datePeriod(start, end)
        self._get_calEntryDates()
               
        
    # def set_datePeriod(self, date_from, date_to):
    #     self.lbl_inter_selection.configure(text="Date period: " + str(date_from) + " - " + str(date_to))
        
        
    def _get_calEntryDates(self):
        start = self.cal_inter_from.get_date()
        end = self.cal_inter_to.get_date()
        #self.set_datePeriod(start, end)
        self.event_generate('<<PeriodSelected>>')
        print(start, end)
    
    
    def get_datePeriod(self):
        start = self.cal_inter_from.get_date()
        end = self.cal_inter_to.get_date()
        return (start, end)
    
    ### TODO : add underscore   
    def _previousPeriod(self, start):
        if self._get_chartDateType() == 'month':
            end = start - \
                dt.timedelta(days=start.day)
            start = end.replace(day=1)
        elif self._get_chartDateType() == 'week':
            end = start - \
                dt.timedelta(days=1)
            start = end - \
                dt.timedelta(days=end.weekday())
        elif self._get_chartDateType() == 'year':
            end = start.replace(day=1, month=1)
            end = end - \
                dt.timedelta(days=1)
            start = end.replace(day=1, month =1)
        #self.set_datePeriod(start, end)
        self.cal_inter_from.set_date(start)
        self.cal_inter_to.set_date(end)
        self._get_calEntryDates()
    
    
    def _nextPeriod(self, end):
        if self._get_chartDateType() == 'month':
            # date - convert to first day of month
             start = end.replace(day=28) + \
                 dt.timedelta(days=4) 
             start = start.replace(day=1)
             end = start.replace(day=28) + \
                 dt.timedelta(days=4)
             end = end - \
                 dt.timedelta(days=end.day)
        elif self._get_chartDateType() == 'week':
            start = end + \
                dt.timedelta(days=1)
            end = start + \
                dt.timedelta(days = 6)
        elif self._get_chartDateType() == 'year':
            start = end.replace(day=31, month=12) + \
                dt.timedelta(days=1)
            end = start.replace(day=31, month=12)
        else: print("error")
        #self.set_datePeriod(start, end)
        self.cal_inter_from.set_date(start)
        self.cal_inter_to.set_date(end)
        self._get_calEntryDates()
        
        
    def _currentPeriod(self):
        if self._get_chartDateType() == 'month':
            self._default_datePeriod()
        elif self._get_chartDateType() == 'week':
            start = self.today - \
                dt.timedelta(days=self.today.weekday())
            end = start + \
                dt.timedelta(days=6)
            self.cal_inter_from.set_date(start)
            self.cal_inter_to.set_date(end)
            self._get_calEntryDates()
            #self.set_datePeriod(start, end)
        elif self._get_chartDateType() == 'year':
            start = self.today.replace(day=1, month=1)
            end = start.replace(day = 31, month=12)
            self.cal_inter_from.set_date(start)
            self.cal_inter_to.set_date(end)
            #self.set_datePeriod(start, end)
            self._get_calEntryDates()
        else: print("error")
        

   
    def _get_chartDateType(self):  
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
        self._previousPeriod(start)
        
    
    def h_btn_Next(self):
        start = self.cal_inter_from.get_date()
        end = self.cal_inter_to.get_date()
        self._nextPeriod(end)
    
    
    def h_btn_Current(self):
        
        self._currentPeriod()
    
             
    # def run(self):
    #     #self._default_datePeriod()
    #     pass
        

if __name__ == '__main__':
    root = tk.Tk()
    widget = PeriodChooserWidget(root)
    widget.pack(expand=True, fill='both')
    root.mainloop() 
    # widget.run()
