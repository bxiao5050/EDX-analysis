import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from itertools import combinations
import pandas as pd

from tkinter import *
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox


class QuaternaryPlot(Frame):

    def __init__(self, master, df):
        super().__init__(master)
        self.pack(expand = 1, fill = 'both')
        self.df = df
        self.elements = df.columns
        lf = LabelFrame(self, text = 'choose elements')
        lf.pack()
        #by default, select the first 4 elements to show
        self.choosed_checkbox = [] #selected 4 elements
        for i, ele in enumerate(self.elements):
            v = IntVar()
            v.set(1) if i <4 else v.set(0)
            self.choosed_checkbox.append(v)
            Checkbutton(lf, text = ele, variable = v, onvalue = 1, offvalue = 0).pack(side = 'left', padx = (2,2))

        Button(lf, text = 'OK', fg ='red', command = self.on_ok).pack(side = 'left', padx = (5,2))



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


        self.plot_3d(self.get_norm_sel_eles(df))


    def on_ok(self):
        self.ax.clear()
        self.plot_3d(self.get_norm_sel_eles(self.df))


    def get_norm_sel_eles(self, df):
        choosed_eles = [v for ele, v in zip(self.choosed_checkbox, self.elements) if ele.get()]
        choosed_df = df[choosed_eles]
        if len(choosed_eles) != 4:
            messagebox.showwarning(message = 'please select 4 elements')

        return choosed_df.div(choosed_df.sum(axis =1), axis = 0)



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




def main():
    root = Tk()

    d = {'Nb': (0, 35.7), 'Mo': (0, 16.3), 'Ta': (54, 34.9), 'W': (36, 3.1), 'Ag': (10, 10)}
    df = pd.DataFrame(data = d)/100

    print (df)

    app = QuaternaryPlot(root, df)


    root.mainloop()

if __name__ =='__main__':
    main()





