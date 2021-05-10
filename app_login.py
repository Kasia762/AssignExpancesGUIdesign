# -*- coding: utf-8 -*-
"""
Created on Mon May 10 16:58:15 2021

@author: ilia
"""
import tkinter as tk
import tkinter.ttk as ttk


class LoginDialog:
    def __init__(self, master=None):
        
    
        # Main widget
        self.loginWindow = self.GUI(master)
        self.loginWindow.title("Login")
        self.loginWindow.grab_set()



    def cb_CreateUser(self):
        """
        Create user callback

        Returns
        -------
        None.

        """

        if not self.txt_usernameAddUser.get():
            self.lbl_usernameAddUser.config(foreground="red")
            self.var_AddUserResult.set(value="User name cannot be empty")
            return False
        else:
            self.lbl_usernameAddUser.configure(foreground="black")
        
        if not self.txt_passwordAdd.get():
            self.lbl_PasswordAdd.config(foreground="red")
            self.var_AddUserResult.set(value="Password cannot be empty")
            return False
        else:
            self.lbl_PasswordAdd.configure(foreground="black")
        
        if not (self.txt_passwordAdd.get() == self.txt_passwordConfAdd.get()):
            self.lbl_PasswordAdd.config(foreground="red")
            self.lbl_PasswordConfAdd.config(foreground="red")
            self.var_AddUserResult.set(value="Passwords are not match")
            return False
        else:
            self.lbl_PasswordAdd.configure(foreground="black")
            self.lbl_PasswordConfAdd.configure(foreground="black")
        ## TODO: call UserCreate()
        self.var_AddUserResult.set(value="Creating user...")
        pass
    
    
    def cb_Login(self):
        """
        Create user callback

        Returns
        -------
        None.

        """
        if  self.cmb_UserLogin.current() < 0:
            self.lbl_selectUser.config(foreground="red")
            return False
        else:
            self.lbl_selectUser.configure(foreground="black")

        if not self.txt_PasswordLogin.get():
            self.lbl_PasswordLogin.config(foreground="red")
            return False
        else:
            self.lbl_PasswordLogin.configure(foreground="black")
        
        ## TODO: call UserLogin() 
        pass


    def GUI(self, master):
        # build ui
        if master == None:
            self.root_login = tk.Tk()
        else:
            self.root_login = tk.Toplevel(master)
            
        ## Hide window 
        ## DO NOT forget to show at the end of init!!!
        self.root_login.withdraw()     
            
        self.ntb_Login = ttk.Notebook(self.root_login)
        
        #LOG IN TAB
        self.frm_login = ttk.Frame(self.ntb_Login)
        self.lbfr_login = ttk.Labelframe(self.frm_login)
        self.lbl_selectUser = ttk.Label(self.lbfr_login)
        self.lbl_selectUser.configure(text='Select user')
        self.lbl_selectUser.grid(column='0', row='0', sticky='s')
        self.lbl_selectUser.master.rowconfigure('0', pad='20', weight='0')
        self.lbl_selectUser.master.columnconfigure('0', pad='0', weight='1')
        self.cmb_UserLogin = ttk.Combobox(self.lbfr_login, 
                                          state="readonly")
        self.cmb_UserLogin.configure(width='20')
        self.cmb_UserLogin.grid(column='0', pady='10', row='1')
        self.cmb_UserLogin.master.columnconfigure('0', pad='0', weight='1')
        self.lbl_PasswordLogin = ttk.Label(self.lbfr_login)
        self.lbl_PasswordLogin.configure(text='Enter password')
        self.lbl_PasswordLogin.grid(column='0', row='2', sticky='s')
        self.lbl_PasswordLogin.master.rowconfigure('2', pad='15')
        self.lbl_PasswordLogin.master.columnconfigure('0', pad='0', weight='1')
        self.txt_PasswordLogin = ttk.Entry(self.lbfr_login)
        self.txt_PasswordLogin.configure(show='*', width='20')
        self.txt_PasswordLogin.grid(column='0', pady='10', row='3')
        self.txt_PasswordLogin.master.columnconfigure('0', pad='0', weight='1')
        self.btn_Login = ttk.Button(self.lbfr_login, 
                                    command = self.cb_Login)
        self.btn_Login.configure(text='LOG IN', width='15')
        self.btn_Login.grid(column='0', pady='20', row='4')
        self.btn_Login.master.columnconfigure('0', pad='0', weight='1')
        self.lbfr_login.configure(height='0', text='Please log in below', width='0')
        self.lbfr_login.grid(column='0', ipady='30', padx='40', pady='40', row='0', sticky='nsew')
        self.lbfr_login.master.rowconfigure('0', pad='10', weight='1')
        self.lbfr_login.master.columnconfigure('0', pad='20', weight='1')
        self.frm_login.configure(height='0', width='0')
        self.frm_login.grid(column='0', row='0', sticky='nsew')
        self.frm_login.master.rowconfigure('0', weight='1')
        self.frm_login.master.columnconfigure('0', weight='1')
        self.ntb_Login.add(self.frm_login, state='hidden', sticky='nsew', text='log in')        
        
        
        # ADD USER TAB
        self.frm_addUser = ttk.Frame(self.ntb_Login)
        self.lbfr_addUser = ttk.Labelframe(self.frm_addUser)
        self.lbl_InfoAddUser = ttk.Label(self.lbfr_addUser)
        self.lbl_InfoAddUser.configure(justify='center', text='Please, enter new user name\n and type your password two times')
        self.lbl_InfoAddUser.grid(column='0', columnspan='2', pady='15', row='0')
        self.lbl_InfoAddUser.master.rowconfigure('0', pad='0')
        self.lbl_InfoAddUser.master.columnconfigure('0', pad='10')
        self.lbl_usernameAddUser = ttk.Label(self.lbfr_addUser)
        self.lbl_usernameAddUser.configure(text='Username')
        self.lbl_usernameAddUser.grid(column='0', padx='11', pady='10', row='1', sticky='e')
        self.lbl_usernameAddUser.master.rowconfigure('1', pad='10')
        self.lbl_usernameAddUser.master.columnconfigure('0', pad='10')
        self.txt_usernameAddUser = ttk.Entry(self.lbfr_addUser)
        self.txt_usernameAddUser.grid(column='1', row='1', sticky='w')
        self.txt_usernameAddUser.master.rowconfigure('1', pad='10')
        self.txt_usernameAddUser.master.columnconfigure('1', pad='11', weight='1')
        self.lbl_PasswordAdd = ttk.Label(self.lbfr_addUser)
        self.lbl_PasswordAdd.configure(text='Password')
        self.lbl_PasswordAdd.grid(column='0', padx='11', pady='5', row='2', sticky='e')
        self.lbl_PasswordAdd.master.rowconfigure('2', pad='5')
        self.lbl_PasswordAdd.master.columnconfigure('0', pad='10')
        self.txt_passwordAdd = ttk.Entry(self.lbfr_addUser)
        self.txt_passwordAdd.configure(show='*')
        self.txt_passwordAdd.grid(column='1', row='2', sticky='w')
        self.txt_passwordAdd.master.rowconfigure('2', pad='5')
        self.txt_passwordAdd.master.columnconfigure('1', pad='11', weight='1')
        self.lbl_PasswordConfAdd = ttk.Label(self.lbfr_addUser)
        self.lbl_PasswordConfAdd.configure(text='Confirm password')
        self.lbl_PasswordConfAdd.grid(column='0', padx='11', pady='5', row='3', sticky='e')
        self.lbl_PasswordConfAdd.master.rowconfigure('3', pad='5')
        self.lbl_PasswordConfAdd.master.columnconfigure('0', pad='10')
        self.txt_passwordConfAdd = ttk.Entry(self.lbfr_addUser)
        self.txt_passwordConfAdd.configure(show='*')
        self.txt_passwordConfAdd.grid(column='1', row='3', sticky='w')
        self.txt_passwordConfAdd.master.rowconfigure('3', pad='5')
        self.txt_passwordConfAdd.master.columnconfigure('1', pad='11', weight='1')
        self.btn_submitAdd = ttk.Button(self.lbfr_addUser, 
                                        command = self.cb_CreateUser)
        self.btn_submitAdd.configure(text='SUBMIT', width='15')
        self.btn_submitAdd.grid(column='0', columnspan='2', ipadx='10', ipady='5', padx='10', pady='15', row='4')
        self.btn_submitAdd.master.columnconfigure('0', pad='10')
        self.lbl_resultAdduser = ttk.Label(self.lbfr_addUser)
        self.var_AddUserResult = tk.StringVar(value='Enter username, password and press Submit button')
        self.lbl_resultAdduser.configure(textvariable=self.var_AddUserResult)
        self.lbl_resultAdduser.grid(column='0', columnspan='2', row='5')
        self.lbl_resultAdduser.master.columnconfigure('0', pad='10')
        self.lbfr_addUser.configure(height='0', text='Please enter the details below', width='0')
        self.lbfr_addUser.grid(column='0', ipady='30', padx='40', pady='40', row='0', sticky='nsew')
        self.lbfr_addUser.master.rowconfigure('0', weight='1')
        self.lbfr_addUser.master.columnconfigure('0', weight='1')
        self.frm_addUser.configure(height='0', width='0')
        self.frm_addUser.grid(column='0', row='0', sticky='nsew')
        self.frm_addUser.master.rowconfigure('0', weight='1')
        self.frm_addUser.master.columnconfigure('0', weight='1')
        self.ntb_Login.add(self.frm_addUser, sticky='nsew', text='add user')
        
        ## Window settings
        self.ntb_Login.configure(width='400')
        self.ntb_Login.grid(column='0', padx='3', pady='3', row='0', sticky='nsew')
        self.ntb_Login.master.rowconfigure('0', minsize='0', weight='1')
        self.ntb_Login.master.columnconfigure('0', minsize='0', weight='1')
        self.root_login.configure(height='150', takefocus=False, width='400')
        self.root_login.resizable(False, False)

        ## Style correcting for tab's well-view
        style = ttk.Style()                     
        current_theme =style.theme_use()
        style.theme_settings(current_theme, 
                {"TNotebook.Tab": {"configure": {"padding": [95, 5]}}})

        # SHOW window, fully constructed
        self.root_login.deiconify()
        return self.root_login