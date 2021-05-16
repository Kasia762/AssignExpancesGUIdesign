# -*- coding: utf-8 -*-
"""
MAIN APP class

@author: ilia
"""
def check_libs(libs, install=False):
    
    import os
    absent_libs = []
    
    if isinstance(libs, str):
        libsToCheck = [libs]
    elif isinstance(libs, (list, tuple)):
        libsToCheck = list(libs)
        
    for lib in libsToCheck:
        try:
            ex = "import " + str(lib)
            print("Trying:", ex,"...", end='' )
            exec(ex)
            print("\t OK")
        except ImportError:
            print("\t cannot import")
            absent_libs.append(lib)
            if install == True:
                comm = 'python -m pip install ' + str(lib).split('.')[0]
                print (f"Trying to install required module: {lib} ...running:")
                print(comm)
                try:
                    #  try to install requests module if not present
                    os.system(comm)
                    #  ... and check is it installed?
                    exec(ex)
                    absent_libs.pop(len(absent_libs)-1)
                except:
                    pass
    return absent_libs


def startup_checking():
    libs = [
        "matplotlib",
        "sqlite3",
        "datetime",
        "numpy",
        "time",
        "dateutil",
        "collections",
        "string",
        "bcrypt",
        "tempfile",
        "os",
        "zlib",
        "base64",
        "sys",
        "pandas",
        "tkinter",
        "tkcalendar"
        ]


    if check_libs("tkinter"):
        ## NO GUI. EXIT
        print('Required library "tkinter" is not found. Please install it running:')
        print('python -m pip install tkinter')
    else:
        import tkinter as tk
        import tkinter.ttk as ttk
        # not empty means smthg absent
        absent = check_libs(libs)
        if absent :
            # GUI QUESTION
            splash_root = tk.Tk()
            splash_root.geometry("400x200")
            splash_label = tk.Label(splash_root,text="Loading...",font=28)
            splash_label.pack()
            splash_root.eval('tk::PlaceWindow . center')
            
            reply =  tk.messagebox.askyesno(title="Libraries absent", 
                                   message="Python libraries absent:\n" + 
                                           "\n".join(absent) +
                                           "\n\nDo you want to install them?")
            if reply == True:
                installres = check_libs(libs, install=True)
                if  installres:
                    print("Please, install that stuff:\n" + "\n".join(installres))
                    print("Cannot continue. Exit.")
                    ### 
                    ### TODO: exit from whole programm
                    exit(1) 
            else:
                ## Libs are missing but answer is NO
                ## TODO: exit from app
                exit(1)
                pass
            splash_root.destroy()
        
class Main_App:
    
    def __init__(self):
        ## UsersHandler instance
        self.usersDataBase = UsersHandler()
        
        
        self.onStartup()
        
        pass
    
    
    def onStartup(self):
        print("Login window opening.")
        loginWin = LoginDialog(None, self.usersDataBase)
        print("Program closed. Thank you for using.")



if __name__ == '__main__':
    ## Check all libraries present
    startup_checking()
    import tkinter as tk
    import tkinter.ttk as ttk
    from app_users import UsersHandler
    from app_login import LoginDialog
    app = Main_App()
   
        