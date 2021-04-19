import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_809=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_809["font"] = ft
        GLabel_809["fg"] = "#333333"
        GLabel_809["justify"] = "center"
        GLabel_809["text"] = "hello user"
        GLabel_809.place(x=10,y=40,width=70,height=25)

        GLabel_33=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_33["font"] = ft
        GLabel_33["fg"] = "#333333"
        GLabel_33["justify"] = "center"
        GLabel_33["text"] = "date, location, weather"
        GLabel_33.place(x=150,y=40,width=433,height=30)

        GButton_585=tk.Button(root)
        GButton_585["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_585["font"] = ft
        GButton_585["fg"] = "#000000"
        GButton_585["justify"] = "center"
        GButton_585["text"] = "Add receipt/expances"
        GButton_585.place(x=430,y=170,width=132,height=51)
        GButton_585["command"] = self.GButton_585_command

        GButton_865=tk.Button(root)
        GButton_865["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_865["font"] = ft
        GButton_865["fg"] = "#000000"
        GButton_865["justify"] = "center"
        GButton_865["text"] = "Display data"
        GButton_865.place(x=430,y=360,width=132,height=43)
        GButton_865["command"] = self.GButton_865_command

    def GButton_585_command(self):
        print("command")


    def GButton_865_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
