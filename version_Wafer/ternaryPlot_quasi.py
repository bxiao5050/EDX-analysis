import ternary
import numpy as np

from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import math


class TernaryPlot_quasi(Frame):
    def __init__(self, master, df = None):
        super().__init__(master)
        self.pack(fill = 'both', expand = True)
        self.sel_GUI = GUI_select(self, df)
        self.sel_GUI.pack()

        Button(self, text = 'Ok', fg = 'red', command = self.on_OK).pack()


        self.scale = 100
        self.t1 = None
        self.ternaryP = None
        self.l1 = None

        self.on_OK()


    def myPlot(self, points, leftLabel = '', rightLabel = '', bottomLabel = ''):
        # self.f.delaxes(self.tax)

        if self.t1 is not None:
            self.t1.remove()
            self.t2.remove()
            self.t3.remove()
            self.plot_f.pack_forget()



        self.plot_f = Frame(self)
        self.plot_f.pack(fill = 'both', expand = True)

        self.f, self.tax = ternary.figure(scale=self.scale)
        # self.ax = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.f, master = self.plot_f)
        self.canvas.get_tk_widget().pack(fill = 'both', expand = True)
        toolbar = NavigationToolbar2Tk(self.canvas, self.plot_f)
        toolbar.update()
        self.canvas.figure.canvas.mpl_connect('button_press_event', self.onclick)


        self.ternaryP = self.tax.scatter(points, marker='s', color='red', label="Red Squares", s = 3)
        self.t1 = self.f.text(0.17,0.55, leftLabel, fontsize = 16)
        self.t2 = self.f.text(0.44, 0.05, bottomLabel, fontsize = 16)
        self.t3 = self.f.text(0.76, 0.55, rightLabel, fontsize = 16)
        #draw boundary and gridlines
        self.tax.boundary(linewidth=2.0)
        self.tax.gridlines(multiple=int(self.scale/10), color="blue")


        # self.tax.set_title("Scatter Plot", fontsize=20)
        self.tax.ticks(axis='lbr', linewidth=1, multiple=int(self.scale/10), offset= 0.03)
        self.tax.get_axes().axis('off')
        self.tax.clear_matplotlib_ticks()
        self.canvas.draw()

    def on_OK(self):
        leftLabel = self.sel_GUI.get_sel_checkbuttons()['leftlabel']
        rightLabel = self.sel_GUI.get_sel_checkbuttons()['rightlabel']
        bottomLabel = self.sel_GUI.get_sel_checkbuttons()['bottomlabel']
        points = self.normalization(self.sel_GUI.get_sel_checkbuttons()['points'])


        self.myPlot(points, leftLabel = leftLabel, rightLabel = rightLabel, bottomLabel = bottomLabel)

    def onclick(self, event):
        click = event.xdata, event.ydata

        if None not in click :
            if self.l1 is not None:
                self.l1.remove()
                self.l2.remove()
                self.l3.remove()


            x = click[0] - math.sqrt(1/3)*click[1]
            z = self.scale - click[0] - math.sqrt(1/3)*click[1]
            y = self.scale - x -z

            p0 = (x,y,z)#click point
            p_bottom = (x, 0, self.scale - x)
            p_right = (self.scale -y, y, 0)
            p_left = (0, self.scale -z, z)

            self.l1, = self.tax.get_axes().plot((click[0], x), (click[1], 0), color = 'green', linestyle = ':')
            self.l2, = self.tax.get_axes().plot((click[0], click[0]+z), (click[1], click[1]), color = 'green', linestyle = ':')
            self.l3, = self.tax.get_axes().plot((click[0], 0.5*(self.scale -z)), (click[1], math.sqrt(3)/2*(self.scale -z)), color = 'green', linestyle = ':')


            self.canvas.draw()



    def normalization(self, points):
        nor_point = []
        for row in points:
            nor_point.append(np.array(row)/sum(row)*100)
        return nor_point




class GUI_select(LabelFrame):
    def __init__(self, master, df):
        super().__init__(master)
        self.df = df
        self.config(text = 'choose elements')
        eles = df.columns

        self.ele_left = self.checkbuttons_and_info('left:', eles, self,0)
        self.ele_buttom = self.checkbuttons_and_info('buttom:', eles, self,1)
        self.ele_right = self.checkbuttons_and_info('right:', eles, self,2)



    def checkbuttons_and_info(self, text, eles, container, n):
        def on_click_me():
            string = ''
            for var, ele in zip(check_vars, eles):
                if var.get() == 1:
                    string += ele + '+'
            ele_inf.config(fg = 'blue', text = string[0:-1])


        f = Frame(container)
        f.pack(anchor = 'w')
        Label(f, text = text, width = 6).pack(anchor = 'w', side = 'left') # label
        check_vars = []
        for i, ele in enumerate(eles):
            var = IntVar()
            if i == n:
                var.set(1)
            Checkbutton(f, text = ele, variable = var, command = on_click_me).pack(anchor = 'w', side = 'left')
            check_vars.append(var)

        ele_inf = Label(f)

        ele_inf.pack(anchor = 'w', side = 'left', padx = (10,5))
        on_click_me()
        return ele_inf

    def get_sel_checkbuttons(self):
        def getSum(string):
            for s in string.split('+'):
                self.df[s]
        data = {}
        data['leftlabel'] = self.ele_left.cget('text')
        data['bottomlabel'] = self.ele_buttom.cget('text')
        data['rightlabel'] = self.ele_right.cget('text')

        bottompoints = self.df[data['bottomlabel'].split('+')].sum(axis =1)
        rightpoints = self.df[data['rightlabel'].split('+')].sum(axis =1)
        leftpoints = self.df[data['leftlabel'].split('+')].sum(axis =1)


        data['points'] = pd.concat([bottompoints,rightpoints,leftpoints], axis = 1).values


        return data




def main():
    root = Tk()
    d = {'Ni': (40, 21, 31, 20), 'Co': (5.5, 36, 37, 30), 'Cu': (55, 43, 31, 50)}
    df = pd.DataFrame(data = d)
    app = TernaryPlot_quasi(root, df)
    # GUI_select(root, df).pack()


    root.mainloop()

if __name__ == '__main__':
    main()
