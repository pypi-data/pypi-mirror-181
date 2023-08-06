import tkinter as tk
from tkinter import ttk
from tkinter import IntVar, Radiobutton, font
from ipra.Utility.StringUtility import GetStringSingletion
from ipra.Utility.tkinterUtility import *
from ipra.Utility.ConfigUtility import GetConfigSingletion


class LoadingPolicyTopLevel(tk.Toplevel):
    def __init__(self,xPos,yPos, totalSize):
        tk.Toplevel.__init__(self)
        self.geometry(f'+{xPos}+{yPos}')
        self.config_obj = GetConfigSingletion()
        self.stringVar = GetStringSingletion()

        self.title(self.stringVar.importPolicy.get())
        self.iconbitmap('C:\IPRA\RESOURCE\hexicon.ico')

        self.geometry("500x200")

        tk.Frame.rowconfigure(self,0,weight=1)
        tk.Frame.columnconfigure(self,0,weight=1)

        mainFrame = tk.Frame(master=self)
        mainFrame.grid(row=0,column=0,sticky='nsew')
        mainFrame.grid_propagate(False)


        self.progressValue = 0
        self.progressBar = ttk.Progressbar(
            mainFrame,
            orient='horizontal',
            mode='determinate',
            maximum= totalSize
            #time 2 is scrap and build
        )

        self.progressBar.grid(column=0, row=0, padx=5,pady=5,sticky='we')
        self.progressBar.grid_propagate(False)


        self.statusLable = tk.Label(mainFrame,text="Test",font=font.Font(size=15))
        self.statusLable.grid(column=0,row=1,sticky='we')
        self.statusLable.grid_propagate(False)

        self.tkraise()

    def setStatusLableText(self,textStringVar):
        self.statusLable.after(10,self.statusLable.config(text=textStringVar))

    def setStatusProgresValueByValue(self,value):
        self.progressValue = self.progressValue+value
        self.progressBar["value"] = self.progressValue
