import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from itertools import combinations
import pandas as pd

from tkinter import *
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import filedialog
try:
    from quaternary_view_full import Quaternary_view_full
except:
    from version_Wafer.quaternary_view_full import Quaternary_view_full


class QuaternaryPlot_quasi(Frame):
    def __init__(self, master, df):
        super().__init__(master)
        self.pack(expand = 1, fill = 'both')
        # self.df = df
        self.elements = df.columns
        f_l = Frame(self)
        f_l.pack(side ='left', anchor = 'n', padx = (5,5), pady = (10,10))

        self.sel_GUI = GUI_select(f_l, df)

        self.sel_GUI.grid(row = 0, column = 0, columnspan = 2, pady = (5,5), sticky = 'nw')
        Button(f_l, text = 'OK', fg ='red', command = self.on_ok).grid(row = 1, column = 0, pady = (5,5), sticky = 'n')
        Button(f_l, text = '>', command = self.on_analysis).grid(row = 2, column = 1, pady = (5,5), sticky = 'ne')


        fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        self.ax = fig.add_subplot(111, projection="3d")#Create a 3D plot in most recent version of matplot
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()

        self.canvas.get_tk_widget().pack(fill='both', expand=1)


        fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')


        self.quasi_df = self.sel_GUI.get_sel_checkbuttons()
        self.plot_3d(self.get_norm_sel_eles(self.quasi_df))

    def on_analysis(self):
        w = Toplevel(self)
        w.title('Quaternary diagram relationship between cartesian and barycentric coordinates')


        Quaternary_view_full(w, self.get_norm_sel_eles(self.quasi_df))


    def on_ok(self):
        self.ax.clear()
        self.quasi_df = self.sel_GUI.get_sel_checkbuttons()
        self.plot_3d(self.get_norm_sel_eles(self.quasi_df))

    #df contains only 4 data columns
    def get_norm_sel_eles(self, df):
        return df.div(df.sum(axis =1), axis = 0)



# load data and plot
    def plot_3d(self,df):
        self.plot_ax()
        self.label_points(labels = df.columns[0:4])
        self.plot_3d_tern(df)

        self.canvas.draw()


    def plot_ax(self):               #plot tetrahedral outline
        verts=[[0,0,0],
         [1,0,0],
         [0.5,np.sqrt(3)/2,0],
         [0.5,0.28867513, 0.81649658]]
        lines=combinations(verts,2)
        for x in lines:
            line=np.transpose(np.array(x))
            self.ax.plot3D(line[0],line[1],line[2],c='0')

    def label_points(self, labels):  #create labels of each vertices of the simplex
        a=(np.array([1,0,0,0])) # Barycentric coordinates of vertices (A or c1)
        b=(np.array([0,1,0,0])) # Barycentric coordinates of vertices (B or c2)
        c=(np.array([0,0,1,0])) # Barycentric coordinates of vertices (C or c3)
        d=(np.array([0,0,0,1])) # Barycentric coordinates of vertices (D or c3)
        # labels=['Ru',  'Pd',  'Ir',  'Pt']
        # labels=['Ru', 'Pd', 'Ir', 'Pt']
        # labels=['a','b','c','d']
        cartesian_points=self.get_cartesian_array_from_barycentric([a,b,c,d])
        for point,label in zip(cartesian_points,labels):
            self.ax.text(point[0],point[1],point[2], label, size=16)

    def get_cartesian_array_from_barycentric(self, b):      #tranform from "barycentric" composition space to cartesian coordinates
        verts=[[0,0,0],
             [1,0,0],
             [0.5,np.sqrt(3)/2,0],
             [0.5,0.28867513, 0.81649658]]

        #create transformation array vis https://en.wikipedia.org/wiki/Barycentric_coordinate_system
        t = np.transpose(np.array(verts))
        t_array=np.array([t.dot(x) for x in b]) #apply transform to all points
        return t_array

    def plot_3d_tern(self, df): #use function "get_cartesian_array_from_barycentric" to plot the scatter points
    #args are b=dataframe to plot and c=scatter point color

        bary_arr=df.iloc[:, 0:4].values # 5 columns, first 4 columns are data the last is EC
        c = df.iloc[:,3]
        cartesian_points=self.get_cartesian_array_from_barycentric(bary_arr)
        self.ax.scatter(cartesian_points[:,0],cartesian_points[:,1],cartesian_points[:,2], s = 2)


class GUI_select(LabelFrame):
    def __init__(self, master, df):
        super().__init__(master)
        self.df = df
        self.config(text = 'choose elements')
        eles = df.columns

        self.vertex1 = self.checkbuttons_and_info('vertex 1:', eles, self,0)
        self.vertex2 = self.checkbuttons_and_info('vertex 2:', eles, self,1)
        self.vertex3 = self.checkbuttons_and_info('vertex 3:', eles, self,2)
        self.vertex4 = self.checkbuttons_and_info('vertex 4:', eles, self,3)



    def checkbuttons_and_info(self, text, eles, container, n):
        def on_click_me():
            string = ''
            for var, ele in zip(check_vars, eles):
                if var.get() == 1:
                    string += ele + '+'
            ele_inf.config(fg = 'blue', text = string[0:-1])


        f = Frame(container)
        f.pack(anchor = 'w', pady = (3,3))
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
        data['vertex1'] = self.vertex1.cget('text')
        data['vertex2'] = self.vertex2.cget('text')
        data['vertex3'] = self.vertex3.cget('text')
        data['vertex4'] = self.vertex4.cget('text')

        vertex1 = self.df[data['vertex1'].split('+')].sum(axis =1)
        vertex2 = self.df[data['vertex2'].split('+')].sum(axis =1)
        vertex3 = self.df[data['vertex3'].split('+')].sum(axis =1)
        vertex4 = self.df[data['vertex4'].split('+')].sum(axis =1)

        data['points'] = pd.concat([vertex1,vertex2,vertex3,vertex4], axis = 1).values


        return pd.DataFrame(data = data['points'], columns = [data['vertex1'] , data['vertex2'] , data['vertex3'] ,data['vertex4'] ])


def main():
    root = Tk()

    d = {'Nb': (0, 35.7), 'Mo': (0, 16.3), 'Ta': (54, 34.9), 'W': (36, 3.1), 'Ag': (10, 10)}
    df = pd.DataFrame(data = d)/100

    print (df)


    app = QuaternaryPlot_quasi(root, df)
    app.pack()


    root.mainloop()

if __name__ =='__main__':
    main()





