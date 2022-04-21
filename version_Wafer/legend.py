
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog, messagebox, ttk
import pickle
from matplotlib.figure import Figure
import pandas as pd
from matplotlib import colors
try:
    from pieChart2 import PieChart
except:
    from version_Wafer.pieChart2 import PieChart

class Legend(LabelFrame):
    def __init__(self, master, elements, colorlist):
        super().__init__(master, bg = 'white')
        self.legendB = {}
        self.elements = elements
        self.labels = {}
        # self.pieChars = pieChars


        #draw legend
        for  ind, ele in enumerate(elements):
            self.legendB[ele] = Button(self, width = 4, bg = colors.rgb2hex(colorlist[ind]), relief = 'flat', command = lambda ele = ele: self.on_legend(ele))

            self.legendB.get(ele).grid(row = ind, column = 0)
            self.labels[ele] = Label(self, width = 4, text = ele, font='Helvetica 13 bold', bg = 'white')
            self.labels.get(ele).grid(row = ind, column = 1, padx = (0,15))

    def on_legend(self, ele):
        pass


    def get_B(self):
        return self.legendB

    def set_legend(self, fontsize, fontstyle, fontweight, color):
        for ele, l in self.labels.items():
            l.config(font = f'Helvetica {fontsize} {fontstyle} {fontweight}', fg = color)

    def get_colorlist(self):
        return {ele:e.cget('bg') for ele, e in self.legendB.items()}


def main():
    root = Tk()
    data = pd.read_csv('data.csv')
    #piechart
    ind = ['' for i in range(len(data.index))]
    d = data.copy()
    d.insert(0, 'Spectrum', ind)
    f = Figure(figsize = (8,8))
    piechart = PieChart(f, root, d)
    piechart.get_tk_widget().pack()

    #legend
    Legend(root, elements=piechart.get_elements(), pieChars=piechart.get_pieCharts(), colorlist = piechart.get_colorlist()).pack(fill = 'both', expand = True)
    # Ele_sequence(root, ['1', '2', '3']).pack()



    root.mainloop()

if __name__ == '__main__':
    main()
