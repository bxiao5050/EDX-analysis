
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import filedialog
from matplotlib import colors
from tkinter import *
from tkinter import ttk

try:
   from version_Wafer.composition import ChooseEle
   # from version_Wafer.showeds import ShowEDS
except:
   from composition import ChooseEle
   # from showeds import ShowEDS

# from version_Wafer.composition import ChooseEle
# from version_Wafer.showeds import ShowEDS




class EDS_Main(Frame):
    """ add Menu to main panel"""
    def __init__(self, master):
        Frame.__init__(self, master)

        self.app = ChooseEle(self)
        self.app.pack()

        menu = Menu(master)
        master.config(menu=menu)
        showmanu = Menu(menu)
        # menu.add_cascade(label="Show", menu=showmanu)
        # showmanu.add_command(label="EDS (neeed .csv data)", command=self.showEDS)


        # self.title("XRD phase identification" + self.app.dataExpPanel.title


    def showEDS(self):
        # ShowEDS(Toplevel(self)).pack()
        w = Toplevel(self)
        show = ShowEDS(w)
        show.pack(fill = 'both', expand = 0)
        w.protocol('WM_DELETE_WINDOW', lambda w=w: show.on_closeAll(w))




def main():
    root = Tk()

    EDS_Main(root).pack()
    root.mainloop()





if __name__ == '__main__': main()




