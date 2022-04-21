from tkinter import *
from tkinter import messagebox, filedialog

from pandastable import Table, TableModel
import pandas as pd

class TextInf(Frame):
    def __init__(self, master):
        super().__init__(master)
        f = Frame(self)


        self.table =Table(f, dataframe=None,
                                showtoolbar=False, showstatusbar=True, width = 50)
        self.table.contractColumns(factor=80)


        f.pack(fill = 'both', expand = 1)
        Button(self, text = 'save to .csv', command = self._on_save).pack()

        self.table.show()


        self.df = None
        # return

        # self.inf.pack()

    def insert_text(self, df):
        self.df = df
        self.table.updateModel(TableModel(df))
        self.table.redraw()

    def clear(self):
        self.table.updateModel(TableModel(None))
        self.table.redraw()






    def _on_save(self):

        f = filedialog.asksaveasfilename(title = "Select file",filetypes = (("csv","*.csv"),("all files","*.*")))

        if len(f) ==0: return

        self.df.to_csv(f+'.csv', sep = ';', index = False)
        messagebox.showinfo(message = 'file saved')


