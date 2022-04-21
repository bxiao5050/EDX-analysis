from tkinter import *

from tkinter import filedialog, messagebox, ttk
import pickle

import pandas as pd
try:
    from publicationDraggableCanvas import PublicationDraggableCanvas
    from publication_para import Putlication_colorcode
    from publication_piechart import Publication_piechart
except:
    from version_Wafer.publicationDraggableCanvas import PublicationDraggableCanvas
    from version_Wafer.publication_para import Putlication_colorcode
    from version_Wafer.publication_piechart import Publication_piechart

class Publication_main_panel(Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.data = data
        nb = ttk.Notebook(self)
        frame1 = Frame(nb) #color coded
        frame2 = Frame(nb) #piechart
        nb.add(frame1, text = 'color coded')
        nb.add(frame2, text = 'piechart')

        nb.pack(fill = 'both', expand = True)


        #color coded
        Putlication_colorcode(frame1, data).pack(fill = 'both', expand = True)
        #piechart
        ind = ['' for i in range(len(data.index))]
        d = data.copy()
        d.insert(0, 'Spectrum', ind)

        Publication_piechart(frame2, d).pack(fill = 'both', expand = True)



def main():
    root = Tk()
    data = pd.read_csv('data.csv')
    Publication_main_panel(root, data).pack(fill = 'both', expand = True)


    root.mainloop()

if __name__ == '__main__':
    main()
