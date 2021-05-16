# -*- coding: utf-8 -*-
"""
Created on Sat May 15 21:59:17 2021

@author: kasia
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:13:20 2021

@author: kasia
"""

import tkinter.ttk as ttk
import tkinter as tk


class AddContractor:
    def __init__(self, master, controller, id_value=None ):
        
        ## 
        self.controller = controller
        ## ID of transaction to change
        self.id_contractor = id_value

        # build ui
        # Main widget
        self.mainwindow = self.GUI(master)
        self.mainwindow.grab_set()
        
        ### Bindings
        self.btn_confirm.bind('<Return>', lambda x: self.h_btn_confirm() )
        self.mainwindow.bind('<Escape>', lambda x: self.h_btn_cancel() )

        ## Initialisation
        self.__initLoadContractor()
            

    def __initLoadContractor(self):
        if self.id_contractor == None:
            pass
        else:
            self.win_addcontr.title('Change cattegory')
            self.btn_confirm.configure(text='Change')
            contr_data = self.controller.badb.getContractor_byId(self.id_contractor)
            contr = contr_data[0]
            self.ent_addcontr.configure(text=contr)
            if contr:
                self.__setContractorEntry(contr)
        pass
        

    def __setContractorEntry(self, value):
        self.ent_addcontr.delete(0, tk.END)
        self.ent_addcontr.insert(0,value)
        self.ent_addcontr.focus()
        self.ent_addcontr.select_range(0, tk.END)


    def h_btn_confirm(self):
    #update fields to selected row    
        contractor = self.ent_addcontr.get()
      
        if self.id_contractor == None:
            res = self.controller.badb.addContractor(contractor)
            print(res)
            self.__setContractorEntry("    ")
            self.controller.updateContractorsTable()
        else:
            res = self.controller.badb.changeContractor(self.id_contractor, contractor)
            print(res)
            self.controller.updateContractorsTable()
            self.id_contractor = None
            #if not destoyed - next option -add
            ## MUST BE LAST line in function
            self.mainwindow.destroy()


    def h_btn_cancel(self):
        self.mainwindow.destroy()  
        

    def GUI(self, master):
        if master == None:
            print("Cannot run independently. Pass master attribute")
            return
        self.win_addcontr = tk.Toplevel(master)
        self.win_addcontr.title('Add cattegory')
        ## Hide window 
        ## DO NOT forget to show at the end of init!!!
        self.frm_addcontr = ttk.Frame(self.win_addcontr)
        
        self.lblfr_contr = ttk.Labelframe(self.frm_addcontr)
        
        self.lbl_addcontr = ttk.Label(self.lblfr_contr)
        self.lbl_addcontr.configure(text='New contractor')
        self.lbl_addcontr.grid(column='0', padx='10', row='0')
        self.ent_addcontr = ttk.Entry(self.lblfr_contr)
        self.ent_addcontr.grid(column='1', row='0', sticky='w')
        
        self.lblfr_contr.configure(height='200', text='Add new contractor', width='200')
        self.lblfr_contr.grid(column='0', row='0', sticky='nsew')
        self.lblfr_contr.rowconfigure('0', pad='20', weight='1')
        self.lblfr_contr.columnconfigure('0', pad='10', weight='1')
        self.lblfr_contr.columnconfigure('1', pad='10', weight='1')
        
        self.lblfrm_btn = ttk.Labelframe(self.frm_addcontr)
        
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
        
        #self.frm_addcontr.configure(height='200', width='200')
        self.frm_addcontr.grid(column='0', padx='10', pady='10', row='0', sticky='nsew')
        self.frm_addcontr.rowconfigure('0', pad ='10', weight='1')
        self.frm_addcontr.rowconfigure('1', pad ='10', weight='1')
        self.frm_addcontr.columnconfigure('0', pad ='10', weight='1')
        #self.win_addcontr.configure(height='200', width='200')
        self.win_addcontr.resizable(False, False)
        
        ## Center window
        x_modal = 300
        y_modal = 170
        x_parent = master.winfo_width()
        y_parent = master.winfo_height()
        x = master.winfo_rootx() + (x_parent - x_modal) // 2
        y = master.winfo_rooty() + (y_parent - y_modal) // 2
        self.win_addcontr.geometry('{}x{}+{}+{}'.format(x_modal, y_modal, x, y))
        
        # SHOW window, fully constructed
        self.win_addcontr.deiconify()
        
        return self.win_addcontr     
    