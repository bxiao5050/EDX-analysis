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
from random import randrange


class Threed_panel(Frame):
    def __init__(self, master):
        super().__init__(master)
        Button(self, text = 'add other EDX data', command = self.on_add, fg = 'red').pack()

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

        self.plot_clicked = []
        self.elements = None

    def on_add(self):
        filename =  filedialog.askopenfilename(title = "Select file",filetypes = (("csv file","*.csv"),("all files","*.*")))
        if len(filename) == 0: return

        # self.df = pd.read_csv('v3.csv', header = 0, index_col = 0, sep = ';')/100
        df = pd.read_csv(filename, header = 0, index_col = 0, sep = ';')/100
        data = pd.DataFrame()
        if self.elements is not None:
            for ele in self.elements[0:4]:
                try:


                    if '+' in ele:
                        # print(ele.split('+'))

                        # data[ele] = np.sum(np.array([df[el].to_numpy() for el in ele.split('+')]))
                        tem = pd.DataFrame()
                        for el in ele.split('+'):
                            tem[el] = df[el]
                        data[ele] = tem.sum( axis = 1)

                        # print(data[ele])
                    else:
                        data[ele] = df[ele]
                        # print(data[ele])
                except:
                    messagebox.showerror(message = f'no column of "{ele}" found in imported data')
                    return
            # data.insert(len(data.columns), '', randrange(10)) # columns saved for other parameters (e.g. current)
            # print(data.head())
            if 'current' in df.columns:
                # print(df['current'])
                data['current'] = df['current']
                self.plot_3d_tern(data, property_col = True)
            else:
                self.plot_3d_tern(data, property_col = False)
        else:
            self.plot_3d_tern(df)

        self.canvas.draw()

    #set element columns for data import
    def set_ele_columns(self, elements):
        self.elements = elements
        # print(elements)



# load data and plot
    def plot_3d(self,df):
        self.plot_ax()
        self.label_points(labels = df.columns[0:4])
        self.plot_3d_tern(df)

        self.canvas.draw()

    def plot_highlight(self, df):
        #clear all highlights
        for line in self.plot_clicked:
            line.remove()
        self.plot_clicked.clear()

        bary_arr=df.iloc[:, 0:4].values
        cartesian_points=self.get_cartesian_array_from_barycentric(bary_arr)
        if len(df.index.values )>0:

            line, = self.ax.plot(cartesian_points[:,0],cartesian_points[:,1],cartesian_points[:,2], marker = 'o', linestyle='none',  markeredgecolor="red",markersize = 6, markerfacecolor='white',markeredgewidth =2)
            self.plot_clicked.append(line)
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

    def plot_3d_tern(self, df, property_col = True): #use function "get_cartesian_array_from_barycentric" to plot the scatter points
    #args are b=dataframe to plot and c=scatter point color

        bary_arr=df.iloc[:, 0:4].values # 5 columns, first 4 columns are data the last is EC
        cartesian_points=self.get_cartesian_array_from_barycentric(bary_arr)
        if property_col:
            c = df.iloc[:,4]
            self.ax.scatter(cartesian_points[:,0],cartesian_points[:,1],cartesian_points[:,2],c=c, s = 2, cmap = 'jet_r')
        else:
            self.ax.scatter(cartesian_points[:,0],cartesian_points[:,1],cartesian_points[:,2], s = 2)




def main():
    root = Tk()
    app = Threed_panel(root)
    app.pack(expand = 1, fill = 'both')

    data = pd.read_csv('v3.csv', header = 0, index_col = 0, sep = ';')/100
    app.plot_3d(data)

    root.mainloop()

if __name__ =='__main__':
    main()





