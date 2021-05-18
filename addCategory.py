# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:13:20 2021

@author: kasia
"""

import tkinter.ttk as ttk
import tkinter as tk


class AddCategory:
    def __init__(self, master, controller, id_value=None ):
        
        ## 
        self.controller = controller
        ## ID of transaction to change
        self.id_category = id_value

        # build ui
        # Main widget
        self.mainwindow = self.GUI(master)
        self.mainwindow.grab_set()
        
        ### Bindings
        self.btn_confirm.bind('<Return>', lambda x: self.h_btn_confirm() )
        self.mainwindow.bind('<Escape>', lambda x: self.h_btn_cancel() )

        ## Initialisation
        self.__initLoadCategory()
            

    def __initLoadCategory(self):
        if self.id_category == None:
            pass
        else:
            self.win_addcat.title('Change cattegory')
            self.btn_confirm.configure(text='Change')
            cat_data = self.controller.badb.getCategory_byId(self.id_category)
            cat = cat_data[0]
            self.ent_addcat.configure(text=cat)
            if cat:
                self.__setCategoryEntry(cat)
        pass
        

    def __setCategoryEntry(self, value):
        self.ent_addcat.delete(0, tk.END)
        self.ent_addcat.insert(0,value)
        self.ent_addcat.focus()
        self.ent_addcat.select_range(0, tk.END)


    def h_btn_confirm(self):
        #update fields to selected row    
        category = self.ent_addcat.get()
      
        if self.id_category == None:
            res = self.controller.badb.addCategory(category)
            print(res)
            self.__setCategoryEntry("    ")
            self.controller.updateCategoriesTable()
        else:
            res = self.controller.badb.changeCategory(self.id_category, category)
            print(res)
            self.controller.updateCategoriesTable()
            self.id_category = None
            #if not destoyed - next option -add
            ## MUST BE LAST line in function
            self.mainwindow.destroy()


    def h_btn_cancel(self):
        self.mainwindow.destroy()  
        

    def GUI(self, master):
        if master == None:
            print("Cannot run independently. Pass master attribute")
            return
        self.win_addcat = tk.Toplevel(master)
        self.win_addcat.title('Add cattegory')
        ## Hide window 
        ## DO NOT forget to show at the end of init!!!
        self.frm_addcat = ttk.Frame(self.win_addcat)
        
        self.lblfr_cat = ttk.Labelframe(self.frm_addcat)
        
        self.lbl_addcat = ttk.Label(self.lblfr_cat)
        self.lbl_addcat.configure(text='New category')
        self.lbl_addcat.grid(column='0', padx='10', row='0')
        self.ent_addcat = ttk.Entry(self.lblfr_cat)
        self.ent_addcat.grid(column='1', row='0', sticky='w')
        
        self.lblfr_cat.configure(height='200', text='Add new category', width='200')
        self.lblfr_cat.grid(column='0', row='0', sticky='nsew')
        self.lblfr_cat.rowconfigure('0', pad='20', weight='1')
        self.lblfr_cat.columnconfigure('0', pad='10', weight='1')
        self.lblfr_cat.columnconfigure('1', pad='10', weight='1')
        
        self.lblfrm_btn = ttk.Labelframe(self.frm_addcat)
        
        self.btn_cancel = ttk.Button(self.lblfrm_btn)
        self.btn_cancel.configure(text='Cancel')
        self.btn_cancel.grid(column='0', ipady ='3', padx='25', row='0', sticky='e')
        self.btn_cancel.configure(command=self.h_btn_cancel)
        self.btn_confirm = ttk.Button(self.lblfrm_btn)
        self.btn_confirm.configure(state='normal', text='Confirm')
        self.btn_confirm.grid(column='1', padx='25', ipady ='3', row='0', sticky='e')
        self.btn_confirm.configure(command=self.h_btn_confirm)
        
        self.lblfrm_btn.configure(height='200', text='Confirm or cancel', width='200')
        self.lblfrm_btn.grid(column='0', row='1', sticky='nsew')
        self.lblfrm_btn.rowconfigure('0', pad='10', weight='1')
        self.lblfrm_btn.columnconfigure('0', pad='10', weight='1')
        self.lblfrm_btn.columnconfigure('1', pad='10', weight='1')
        
        #self.frm_addcat.configure(height='200', width='200')
        self.frm_addcat.grid(column='0', padx='10', pady='10', row='0', sticky='nsew')
        self.frm_addcat.rowconfigure('0', pad ='10', weight='1')
        self.frm_addcat.rowconfigure('1', pad ='10', weight='1')
        self.frm_addcat.columnconfigure('0', pad ='10', weight='1')
        #self.win_addcat.configure(height='200', width='200')
        self.win_addcat.resizable(False, False)
        
        ## Center window
        x_modal = 300
        y_modal = 170
        x_parent = master.winfo_width()
        y_parent = master.winfo_height()
        x = master.winfo_rootx() + (x_parent - x_modal) // 2
        y = master.winfo_rooty() + (y_parent - y_modal) // 2
        self.win_addcat.geometry('{}x{}+{}+{}'.format(x_modal, y_modal, x, y))
        
        # SHOW window, fully constructed
        self.win_addcat.deiconify()
        
        return self.win_addcat     
    