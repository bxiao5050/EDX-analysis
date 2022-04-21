from tkinter import *
from tkinter.colorchooser import *
from tkinter import filedialog, messagebox, ttk
import pickle
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from matplotlib import colors
from matplotlib import cm



try:
    from legend import Legend
    from pieChart2 import PieChart
    from fontPanel import FontPanel
    from pie_target_positions2 import Pie_target_positions
    from pie_slice_setting_on import Pie_slice_setting_on
except:
    from version_Wafer.legend import Legend
    from version_Wafer.pieChart2 import PieChart
    from version_Wafer.fontPanel import FontPanel
    from version_Wafer.pie_target_positions2 import Pie_target_positions
    from version_Wafer.pie_slice_setting_on import Pie_slice_setting_on

class Publication_piechart(Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.canvas = Canvas(self, width = 1300, height = 900, background = 'white',highlightthickness=0)

        self.data = data
        para = Frame(self)

        eles = [v for v in self.data.columns[3:]]
        colors = cm.Set3(np.linspace(0, 1, len(eles)))

        self.elements = {ele:ele for ele in eles}
        self.colorlist = {ele:col for ele, col in zip(eles, colors)}

        #plot piechart
        f = Figure(figsize = (8,8))
        self.piechart = PieChart(f, master =self.canvas, data =data, elements=eles, colorlist = colors)
        #target position
        fig = Figure(figsize=(1.7,1.7))

        self.tar_pos = Pie_target_positions(fig, self.canvas, labels=eles, colors = colors)

        #legend
        self.plot_leg = Legend(self.canvas, elements=eles, colorlist = colors)




        self.piechart.get_tk_widget().place(x =50,y =50)
        self.plot_leg.place(x = 850, y = 640)
        self.tar_pos.get_tk_widget().place(x = 700, y = 0)

        self.plot_leg.place_forget()
        self.tar_pos.get_tk_widget().place_forget()

        self.piechart.get_tk_widget().bind("<Button-1>",self.drag_start)
        self.piechart.get_tk_widget().bind("<B1-Motion>",self.drag_motion)
        self.piechart.get_tk_widget().bind("<ButtonRelease-1>",self.stop_scrolling)
        self.plot_leg.bind("<Button-1>",self.drag_start)
        self.plot_leg.bind("<B1-Motion>",self.drag_motion)
        self.plot_leg.bind("<ButtonRelease-1>",self.stop_scrolling)
        self.tar_pos.get_tk_widget().bind("<Button-1>",self.drag_start)
        self.tar_pos.get_tk_widget().bind("<B1-Motion>",self.drag_motion)
        self.tar_pos.get_tk_widget().bind("<ButtonRelease-1>",self.stop_scrolling)

        #parameters panel
        pie_setting = Pie_slice_setting_on(para, data, plot_pie=self.piechart, tar_pos=self.tar_pos, plot_leg=self.plot_leg, elements=self.elements, colorlist = self.colorlist)
        #add font
        fontpanel = FontPanel(self, self.canvas)
        fontpanel.pack(side = 'bottom')
        addfont_b = Button(para, text = 'add font', fg = 'green', command = fontpanel.on_add)


        pie_setting.grid(row = 0, column = 0, sticky = 'nw', padx = (5,5), pady = (5,5))
        addfont_b.grid(row = 1, column = 0, sticky = 'nw', padx = (5,5), pady = (5,5))

        self.canvas.pack(side = 'left', fill = 'both', expand = True)
        para.pack(side = 'right',anchor = 'nw')




    def drag_start(self,event):
        event.widget.config(relief = 'sunken')
        widget = event.widget
        widget.startX = event.x
        widget.startY = event.y

    def drag_motion(self,event):
        widget = event.widget
        x = widget.winfo_x() - widget.startX + event.x
        y = widget.winfo_y() - widget.startY + event.y
        widget.place(x=x,y=y)

    def stop_scrolling(self,event):
        event.widget.config(relief = 'flat')







def main():
    root = Tk()
    data = pd.read_csv('aa.csv', sep = ';')
    # d = pd.read_csv('data.csv')
    # print(data.head())
    # print(d.head())
    Publication_piechart(root, data).pack(fill = 'both', expand = True)
    # Ele_sequence(root, ['1', '2', '3']).pack()



    root.mainloop()

if __name__ == '__main__':
    main()
