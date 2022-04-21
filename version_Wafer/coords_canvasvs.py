import pandas as pd
import numpy as np

import glob
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
import matplotlib
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector



class Coords_canvasvs(LabelFrame):
    '''show canvas in scatter
    '''
    def __init__(self, master):
        super().__init__(master)
        self.coords = pd.read_csv('coordsvs.txt', header = 0, index_col = 0)
        self.width = 4000
        self.x, self.y = self.coords.iloc[:,0], self.coords.iloc[:,1]

        self.b_clear = Button(self, text = 'clear selections', fg = 'blue', command = self._on_clear)
        self.b_clear.pack()

        self.fig = Figure(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.ax = self.fig.add_subplot(111)
        self.canvas.get_tk_widget().pack(fill='both', expand=1)
        # toolbar = NavigationToolbar2Tk(self.canvas, self)
        # toolbar.update()
        # self.ax.invert_yaxis()
        # self.ax.scatter(self.x, self.y, marker = 's', linewidths = 2)# plot all the coords

        self.clicked_xy=[]
        self.plot_clicked = []




    def importData(self, df):
        # bary_arr=df.iloc[:, 0:4].values # 5 columns, first 4 columns are data the last is EC
        c = df.iloc[:,4]

        cax = self.ax.scatter(self.x, self.y, c= c, marker = 's', linewidths = 2, cmap = 'jet_r')
        self.cbar = self.fig.colorbar(cax)

        # self.cid1 = self.canvas.mpl_connect('button_press_event', self.on_click)
        # #__________________uncomment when multi-mouse selection needed______________
        # self.RS = RectangleSelector(self.ax, self.line_select_callback,
        #                                        drawtype='box', useblit=True,
        #                                        button=[1, 3],  # don't use middle button
        #                                        minspanx=5, minspany=5,
        #                                        spancoords='pixels',
        #                                        interactive=False)
        self.canvas.draw()

    # return clicked index
    def get_clicked_index(self):
        ind = []
        for (x, y) in self.get_clicked():
            ind.append(self.coords[(self.coords['x'] == x)&(self.coords['y'] == y)].index.item())

        return ind






    #return clicked positions
    def get_clicked(self):
        return list(set(self.clicked_xy))

    def _on_clear(self):
        for line in self.plot_clicked:
            line.remove()
        self.clicked_xy.clear()
        self.plot_clicked.clear()
        self.canvas.draw()


    def on_click(self, event):
        if event.inaxes!=self.ax: return
        self.get_click_xy(event.xdata, event.ydata)


    # return clicked x, y
    def get_click_xy(self, xdata, ydata):
        index_x = np.abs(self.x-xdata) < self.width/2
        index_y = np.abs(self.y-ydata) < self.width/2
        list1 = self.x[index_x].index
        list2 = self.y[index_y].index

        #get the common index from x and y index
        index = list(set(list1).intersection(list2))

        if len(index): #find commen value between two arrays
            click_x, click_y = self.x.loc[index].iat[0], self.y.loc[index].iat[0]
            if (click_x, click_y) in self.get_clicked(): # click again then remove
                self.clicked_xy.remove((click_x, click_y))
            else:
                self.clicked_xy.append((click_x, click_y))

        self.updata_canvas()

    def line_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        # self.clicked_xy = []
        for x, y in zip(self.x, self.y):
            if x> min(x1, x2) and x < max(x1, x2) and y > min(y1, y2) and y< max(y1, y2):
                self.clicked_xy.append((x,y))

        self.updata_canvas()
        # return clicked_xy

    def updata_canvas(self):
        #clear all highlights
        for line in self.plot_clicked:
            line.remove()
        self.plot_clicked.clear()

        x = [x for x, y in self.clicked_xy]
        y = [y for x, y in self.clicked_xy]

        # line, = self.ax.plot(x, y,linestyle='none', marker='s', markeredgecolor="orange",markersize = 7, markerfacecolor='red',markeredgewidth =2)
        line, = self.ax.plot(x, y,linestyle='none', marker='x', markeredgecolor="gray",markersize = 11, markerfacecolor='white',markeredgewidth =2)
        self.plot_clicked.append(line)
        self.canvas.draw()










def main():
    root = Tk()
    app = Coords_canvasvs(root)
    app.pack()
    app.mainloop()

if __name__=='__main__':
    main()
