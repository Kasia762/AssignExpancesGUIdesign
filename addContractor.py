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
        self.id_value = id_value

        # Main widget
        self.mainwindow = self._GUI(master)
        self.mainwindow.grab_set()
        
        ### Bindings
        self.btn_confirm.bind('<Return>', lambda x: self.h_btn_confirm() )
        self.ent_Limit.bind('<Return>', lambda x: self.__evaluateLimitEntry() )
        self.mainwindow.bind('<Escape>', lambda x: self.h_btn_cancel() )

        ## Initialisation
        self.__initLoad()
            

    def __initLoad(self):
        if self.id_value == None:
            self.mainwindow.title('Add contractor')
            self.btn_confirm.configure(text='Add')
            pass
        else:
            self.mainwindow.title('Change contractor')
            self.btn_confirm.configure(text='Change')
            ### ***
            ### FIXME: Correct Attribute: Category / Contractor
            data = self.controller.badb.getContractor_byId(self.id_value)
            name = data[0]
            limit = data[2]
            comment = data[3]
            self.var_Limit.set( limit )
            self.var_Comment.set( comment )
            self.__setNameEntry( name )
        pass


    def __evaluateLimitEntry(self):
        # Try to evaluate string in Entry as python:
        try:
            s = self.var_Limit.get()
            news = str( eval(s) )
            self.var_Limit.set(news)
            return True
        except:
            print("Limit cannot be calculated...")
            self.ent_Limit.focus()
            self.ent_Limit.select_range(0, tk.END)
            return False


    def __parse_name(self, name):
        # Remove all extra spaces
        name = " ".join(name.split())
        if name == " ":
            return ''
        else:
            return name


    def __setNameEntry(self, value):
        self.var_Name.set(value=value)
        self.ent_Name.focus()
        self.ent_Name.select_range(0, tk.END)


    def h_btn_confirm(self):
        self.var_Name.set( self.__parse_name( self.var_Name.get() ) )
        name = self.var_Name.get()
        if name == '':
            print("Name is empty")
            tk.messagebox.showwarning("Enter valid data",
                                      "Name cannot be empty.\n\nPlease, enter correct name.",
                                      parent=self.mainwindow)
            return
        if not self.__evaluateLimitEntry() :
            return
        limit = abs( float( self.var_Limit.get() ) )
        comment = self.var_Comment.get()
      
        if self.id_value == None:
            ### ***
            ### FIXME: Correct Attribute: Category / Contractor
            if self.controller.badb.isExistsContractor( name ) == True:
                print("Name is already exists.")
                tk.messagebox.showwarning("Enter valid data",
                                          "The Name is already exists.\n\nPlease, enter other name.",
                                          parent=self.mainwindow)
                return
                
            ### ***
            ### FIXME: Correct Attribute: Category / Contractor
            res = self.controller.badb.addContractor(name, limit, comment)
            print(res)
        else:
            ### ***
            ### FIXME: Correct Attribute: Category / Contractor
            res = self.controller.badb.changeContractor(self.id_value, name, limit, comment)
            print(res)
            self.id_value = None
        #if not destoyed - next option -add
        ## MUST BE LAST line in function
        self.mainwindow.destroy()


    def h_btn_cancel(self):
        self.mainwindow.destroy()  
        

    def _GUI(self, master):
        if master == None:
            print("Cannot run independently. Pass master attribute")
            return
        self.win_AttributeProperties = tk.Toplevel(master)
        self.win_AttributeProperties.title('Add attribute')
        ## Hide window 
        ## DO NOT forget to show at the end of init!!!
        self.win_AttributeProperties.withdraw()
        
        self.frm_AttributeProperties = ttk.Frame(self.win_AttributeProperties)
        self.frm_fields = ttk.Frame(self.frm_AttributeProperties)
        self.lbl_Name = ttk.Label(self.frm_fields)
        self.lbl_Name.configure(text='Name')
        self.lbl_Name.grid(column='0', padx='10', row='0', sticky='e')
        self.lbl_Name.master.rowconfigure('0', pad='30')
        self.ent_Name = ttk.Entry(self.frm_fields)
        self.var_Name = tk.StringVar(value='')
        self.ent_Name.configure(textvariable=self.var_Name)
        self.ent_Name.grid(column='1', row='0', sticky='ew')
        self.ent_Name.master.rowconfigure('0', pad='30')
        self.ent_Name.master.columnconfigure('1', minsize='300', weight='1')
        self.lbl_Limit = ttk.Label(self.frm_fields)
        self.lbl_Limit.configure(text='Month limit')
        self.lbl_Limit.grid(column='0', padx='10', row='1', sticky='e')
        self.lbl_Limit.master.rowconfigure('1', pad='10')
        self.ent_Limit = ttk.Entry(self.frm_fields)
        self.var_Limit = tk.StringVar(value='')
        self.ent_Limit.configure(textvariable=self.var_Limit)
        self.ent_Limit.grid(column='1', row='1', sticky='w')
        self.ent_Limit.master.rowconfigure('1', pad='10')
        self.ent_Limit.master.columnconfigure('1', minsize='300', weight='1')
        self.lbl_Comment = ttk.Label(self.frm_fields)
        self.lbl_Comment.configure(text='Comment')
        self.lbl_Comment.grid(column='0', padx='10', row='2', sticky='e')
        self.lbl_Comment.master.rowconfigure('2', pad='10')
        self.ent_Comment = ttk.Entry(self.frm_fields)
        self.var_Comment = tk.StringVar(value='')
        self.ent_Comment.configure(textvariable=self.var_Comment)
        self.ent_Comment.grid(column='1', row='2', sticky='ew')
        self.ent_Comment.master.rowconfigure('2', pad='10')
        self.ent_Comment.master.columnconfigure('1', minsize='300', weight='1')
        self.frm_fields.configure(padding='20 20')
        self.frm_fields.grid(column='0', ipady='10', row='0', sticky='nsew')
        self.frm_fields.master.rowconfigure('0', pad='0', weight='1')
        self.frm_fields.master.columnconfigure('0', pad='0', weight='1')
        self.separator1 = ttk.Separator(self.frm_AttributeProperties)
        self.separator1.configure(orient='horizontal')
        self.separator1.grid(column='0', padx='10', row='1', sticky='sew')
        self.separator1.master.rowconfigure('1', pad='0')
        self.separator1.master.columnconfigure('0', pad='0', weight='1')
        self.frm_buttons = ttk.Frame(self.frm_AttributeProperties)
        self.frm_buttons.rowconfigure('0', minsize='30', pad='20')
        self.frm_buttons.columnconfigure('0', weight='100')
        self.btn_decline = ttk.Button(self.frm_buttons)
        self.btn_decline.configure(text='Cancel', width='10')
        self.btn_decline.grid(column='1', row='0')
        self.btn_decline.master.rowconfigure('0', minsize='30', pad='20')
        self.btn_decline.master.columnconfigure('1', pad='10')
        self.btn_decline.configure(command=self.h_btn_cancel)
        self.btn_confirm = ttk.Button(self.frm_buttons)
        self.btn_confirm.configure(state='normal', text='Add')
        self.btn_confirm.grid(column='2', row='0')
        self.btn_confirm.master.rowconfigure('0', minsize='30', pad='20')
        self.btn_confirm.master.columnconfigure('1', weight='1')
        self.btn_confirm.master.columnconfigure('2', minsize='0', pad='20')
        self.btn_confirm.configure(command=self.h_btn_confirm)
        self.frm_buttons.configure( padding='5 5')
        self.frm_buttons.grid(column='0', row='2', sticky='sew')
        self.frm_buttons.master.rowconfigure('1', pad='10', weight='1')
        self.frm_buttons.master.columnconfigure('0', pad='0', weight='1')
        self.frm_AttributeProperties.grid(column='0', row='0', sticky='nsew')
        self.frm_AttributeProperties.master.rowconfigure('0', weight='1')
        self.frm_AttributeProperties.master.columnconfigure('0', weight='1')
        self.win_AttributeProperties.resizable(False, False)
        
        ## Center window
        self.win_AttributeProperties.update()
        x_modal = self.win_AttributeProperties.winfo_width()
        y_modal = self.win_AttributeProperties.winfo_height()
        x_parent = master.winfo_width()
        y_parent = master.winfo_height()
        x = master.winfo_rootx() + (x_parent - x_modal) // 2
        y = master.winfo_rooty() + (y_parent - y_modal) // 2
        self.win_AttributeProperties.geometry('{}x{}+{}+{}'.format(x_modal, y_modal, x, y))
        
        # SHOW window, fully constructed
        self.win_AttributeProperties.deiconify()
        
        return self.win_AttributeProperties     
    