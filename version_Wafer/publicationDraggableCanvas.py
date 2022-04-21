from tkinter import *
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib
from PIL import Image,ImageTk
from io import BytesIO
import math
try:
    from matplotlib.markers import MarkerStyle
except:
    from version_Wafer.matplotlib.markers import MarkerStyle

class PublicationDraggableCanvas(Frame):
    def __init__(self, master, data):
        super().__init__(master)

        self.canvas = Canvas(self, width = 1300, height = 900, background = 'white',highlightthickness=0,)
        self.data = data

        self.x = data['x']
        self.y = data['y']
        self.eles = data.columns[2:]
        self.axes = []
        self.canvases = []
        self.cbar = []
        self.cax = []

        for i, ele in enumerate(self.eles):
            c = data[ele]
            fig = Figure(figsize=(4, 3), dpi = 100)
            self.axes.append(fig.add_subplot(111))
            self.canvases.append(FigureCanvasTkAgg(fig, master=self.canvas))

            self.cax.append(self.axes[-1].scatter(self.x, self.y, c = c, s = 30,cmap = 'jet', marker = 's'))
            self.cbar.append(fig.colorbar(self.cax[-1], ax = self.axes[-1], ticks = np.round(np.linspace(c.min(), c.max(), 8, endpoint = True), 1)))
            self.cbar[-1].ax.set_title('at.%', fontsize = 8)
            self.axes[-1].set_title(ele, fontsize = 8)

            self.canvases[-1].get_tk_widget().place(x=(i%3)*400, y = int(i/3)*300+40)
            self.canvases[-1].get_tk_widget().bind("<Button-1>",self.drag_start)
            self.canvases[-1].get_tk_widget().bind("<B1-Motion>",self.drag_motion)

        # b_export.pack()
        self.canvas.pack(fill = 'both', expand = True)

    #set colorbar num
    def set_colorbar_ticknum(self, ticknum, decimalnum):
        for cb, ele, canvas in zip(self.cbar, self.eles, self.canvases):
            c = self.data[ele]
            if decimalnum != 0:
                # cb.set_ticklabels()
                cb.set_ticks(np.round(np.linspace(c.min(), c.max(), ticknum, endpoint = True), decimalnum))
                cb.set_ticklabels( np.round(np.linspace(c.min(), c.max(), ticknum, endpoint = True), decimalnum))
            else:
                cb.set_ticks(np.round(np.linspace(c.min(), c.max(), ticknum, endpoint = True), 1))
                cb.set_ticklabels([int(i) for i in np.round(np.linspace(c.min(), c.max(), ticknum, endpoint = True), decimalnum)])
            canvas.draw()

    #set figure title
    def set_fig_title(self, figTitle, fontsize, color, fontstyle, fontweight):
        for i, ele in enumerate(self.eles):
            self.axes[i].set_title(figTitle[i], fontsize = fontsize, color =color, fontstyle = fontstyle, fontweight = fontweight)
            self.canvases[i].draw()

    #set colorbar title
    def set_colorbar_title(self, figTitle, fontsize, color, fontstyle, fontweight):
        for i, ele in enumerate(self.eles):
            self.cbar[i].ax.set_title(figTitle[i], fontsize = fontsize, color =color, fontstyle = fontstyle, fontweight = fontweight)
            self.canvases[i].draw()

    #set colorbar ticks
    def set_colorbar_ticks(self, fontsize, color, fontstyle, fontweight):
        for cb,canvas in zip(self.cbar, self.canvases):
            for t in cb.ax.get_yticklabels():
                t.set_fontsize(fontsize)
                t.set_color(color)
                t.set_fontstyle(fontstyle)
                t.set_fontweight(fontweight)
            canvas.draw()

    #set figure scatter
    def set_fig_scatter(self,marker , markersize,  cmap, alpha, linewidth, edgecolors):

        for i, ele in enumerate(self.eles):
            self.cax[i].set_paths([MarkerStyle(marker).get_path().transformed(MarkerStyle(marker).get_transform()) for i in self.data[ele]])
            self.cax[i].set_sizes([markersize for i in self.data[ele]])
            self.cax[i].set_alpha(alpha)
            self.cax[i].set_cmap(cmap)
            self.cax[i].set_linewidth(linewidth)
            self.cax[i].set_edgecolors(edgecolors)
            self.canvases[i].draw()

    #set axis ticks
    def set_fig_ticks(self, axistype):
         for i, ele in enumerate(self.eles):
            self.axes[i].axis('on')
            if axistype == 'normal':
                self.axes[i].xaxis.set_visible(True)
                self.axes[i].yaxis.set_visible(True)
            elif axistype == 'without axis':
                self.axes[i].xaxis.set_visible(False)
                self.axes[i].yaxis.set_visible(False)
            elif axistype == 'without X-axis':
                self.axes[i].xaxis.set_visible(False)
                self.axes[i].yaxis.set_visible(True)
            elif axistype == 'without Y-axis':
                self.axes[i].xaxis.set_visible(True)
                self.axes[i].yaxis.set_visible(False)
            elif axistype == 'without frame':
                self.axes[i].axis('off')

            self.canvases[i].draw()

    #set axis tick color
    def set_fig_tick_color(self, color):
        for ax, canvas in zip(self.axes, self.canvases):
            ax.tick_params(color=color, labelcolor=color)
            for spine in ax.spines.values():
                spine.set_edgecolor(color)
            canvas.draw()
    #set axis fontsize
    def set_fig_axis_fontsize(self, fontsize):
        for ax, canvas in zip(self.axes, self.canvases):
            for item in ([ ax.xaxis.label, ax.yaxis.label] +
                         ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontsize(fontsize)
            canvas.draw()
    #set axis font
    def set_axis_font(self, weight):
        for ax, canvas in zip(self.axes, self.canvases):
            labels = ax.get_xticklabels() + ax.get_yticklabels()
            for label in labels:
                label.set_fontweight(weight)
            canvas.draw()




    def drag_start(self,event):
        widget = event.widget
        widget.startX = event.x
        widget.startY = event.y

    def drag_motion(self,event):
        widget = event.widget
        x = widget.winfo_x() - widget.startX + event.x
        y = widget.winfo_y() - widget.startY + event.y
        widget.place(x=x,y=y)





def main():
    root = Tk()
    data = pd.read_csv('data.csv')

    PublicationDraggableCanvas(root, data).pack(fill = 'both', expand =1)

    root.mainloop()

if __name__ == '__main__':
    main()
