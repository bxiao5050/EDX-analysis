from tkinter.filedialog import askopenfilenames, askopenfilename
from tkinter.colorchooser import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import colors
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Circle
from tkinter.colorchooser import *
from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
import threading
import time

try:
    from pie_target_positions import Pie_target_positions
except: from version_Wafer.pie_target_positions import Pie_target_positions



class PieChart(FigureCanvasTkAgg):
    def __init__(self, f, master, data,elements, colorlist ):
        super().__init__(f, master = master)
        self.data = data



        """
          Spectrum         x        y    Ru     Pd  Ag   Ir      Pt
        Spectrum 1 {6}  -22,67  -40,969 21,5    5,9 3   50,4    19,1
        Spectrum 1 {7}  -18,169 -40,969 19,6    5,3 2,5 52,6    20
        Spectrum 1 {8}  -13,67  -40,969 18,5    6,5 2,5 51,9    20,5
        """
        self.pieChars = {}#piecharts
        self.ax_sub = {}
        self.ax = f.add_subplot(111)

        self.ax.set_xlim(-53, 53)
        self.ax.set_ylim(-53, 53)
        self.ax.axis('off')
        f.subplots_adjust(left=0.001, bottom=-0.001, right=1, top=1, wspace=0, hspace=0)
        self.insetsize = 5.2
        #draw piechart
        self.deviation = 4.5/2
        self.elee = elements
        self.colorlist = colorlist
        self.canvas_c = Circle((0, 0), radius=50, fill = True, facecolor = 'lightblue', edgecolor = 'black', alpha = 0.5)
        self.ax.add_patch(self.canvas_c)
        self.canvas_c.set_visible(False)



        for index, row in self.data.iterrows():
            x = row[1]-self.insetsize/2
            y = row[2]-self.insetsize/2

            self.ax_sub[index] = self.ax.inset_axes([x, y, self.insetsize, self.insetsize], transform=self.ax.transData)
            self.pieChars[index], t1 = self.ax_sub[index].pie([v for v in row[3:]], colors = self.colorlist, wedgeprops = {'linewidth' :0.5, 'edgecolor' :'black'})
            self.ax_sub[index].axis('off')

    def set_circle(self, facecolor, edgecolor, linewidth, radius, alpha, fill = True):
        self.canvas_c.set_alpha(alpha)
        self.canvas_c.set_edgecolor(edgecolor)
        self.canvas_c.set_facecolor(facecolor)
        self.canvas_c.set_fill(fill)
        self.canvas_c.set_linewidth(linewidth)
        self.canvas_c.set_radius(radius)

        self.draw()


    def update_pie(self, elee, colors,startangle, radius, alpha, linewidth, edgecolor):
        for pie in self.pieChars.values():
            for p in pie:
                p.remove()


        # self.ax.clear()
        # self.ax.set_xlim(-53, 53)
        # self.ax.set_ylim(-53, 53)
        # self.ax.axis('off')

        self.elee = elee

        self.pieChars.clear()
        self.ax_sub.clear()
        d = pd.DataFrame()
        d['x'] = self.data['x']
        d['y'] = self.data['y']

        for ele in self.elee:
            d[ele] = self.data[ele]

        for index, row in d.iterrows():
            x = row['x']-self.insetsize/2
            y = row['y']-self.insetsize/2

            self.ax_sub[index] = self.ax.inset_axes([x, y, self.insetsize, self.insetsize], transform=self.ax.transData)
            self.pieChars[index], t1 = self.ax_sub[index].pie([v for v in row[2:]], colors = colors, startangle = startangle, radius = radius, wedgeprops = {'linewidth' :linewidth, 'edgecolor' : edgecolor, 'alpha':alpha})
            self.ax_sub[index].axis('off')
        self.draw()


    def update_color(self, ele, color):
        for pie in self.pieChars.values():
            pie[self.elee.index(ele)].set_color(color)

        self.draw()


    def get_pieCharts(self):
        return self.pieChars

    def get_ax_sub(self):
        return self.ax_sub





def main():
    root = Tk()
    data = pd.read_csv('aa.CSV')
    f = Figure(figsize = (8,8))
    elements = [v for v in data.columns[3:]]
    colorlist = cm.Set3(np.linspace(0, 1, len(elements)))
    app = PieChart(f, root, data,elements, colorlist)
    app.get_tk_widget().pack()


    root.mainloop()


if __name__ == '__main__':
    main()

