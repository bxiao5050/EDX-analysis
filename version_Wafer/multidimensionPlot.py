import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from itertools import combinations
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
from tkinter import filedialog
import matplotlib
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector


class MultidimensionPlot(Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.pack(fill = 'both', expand = True)
        Button(self, text = 'add other EDX data', fg = 'red', command = self.on_add_other_data).pack()
        fig = Figure(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        self.ax = fig.add_subplot(111)
        self.canvas.get_tk_widget().pack(fill='both', expand=1)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()

        self.ele_columns = data.columns # elements columns and sequence

        print(data.head())

        corners = self.polycorners(ncorners=len(self.ele_columns))
        self.corners = corners
        lines=combinations(corners,2)
        for x in lines:
            line=np.transpose(np.array(x))
            self.ax.plot(line[0],line[1],c='black')
        for c,el in zip(corners,data.columns):
            self.ax.text(c[0]+0.06,c[1],el,fontsize=16)

        ba = self.bary2cart(data.values, corners = corners)
        self.ax.scatter(ba[:,0],ba[:,1],alpha = 0.4)

        # self.tetrahedron_plot(data, self.ele_columns)

        self.canvas.draw()

    def on_add_other_data(self):
        filename =  filedialog.askopenfilename(title = "Select file",filetypes = (("csv file","*.csv"),("all files","*.*")))
        if len(filename) == 0: return

        # self.df = pd.read_csv('v3.csv', header = 0, index_col = 0, sep = ';')/100
        df = pd.read_csv(filename, header = 0, index_col = 0, sep = ';')/100

        # get the element columns with the certain sequence
        data = pd.DataFrame()

        for ele in self.ele_columns:
            try:
                data[ele] = df[ele]
            except:
                messagebox.showerror(message = f'no column of "{ele}" in imported data')
                return

        ba = self.bary2cart(data.values, corners = self.corners)
        self.ax.scatter(ba[:,0],ba[:,1],alpha = 0.4)
        self.canvas.draw()

    def polycorners(self, ncorners=3):
        '''
        Return 2D cartesian coordinates of a regular convex polygon of a specified
        number of corners.
        Args:
            ncorners (int, optional) number of corners for the polygon (default 3).
        Returns:
            (ncorners, 2) np.ndarray of cartesian coordinates of the polygon.
        '''

        center = np.array([0.5, 0.5])
        points = []

        for i in range(ncorners):
            angle = (float(i) / ncorners) * (np.pi * 2) + (np.pi / 2)
            x = center[0] + np.cos(angle) * 0.5
            y = center[1] + np.sin(angle) * 0.5
            points.append(np.array([x, y]))

        return np.array(points)

    def bary2cart(self, bary, corners=None):
        '''
        Convert barycentric coordinates to cartesian coordinates given the
        cartesian coordinates of the corners.
        Args:
            bary (np.ndarray): barycentric coordinates to convert. If this matrix
                has multiple rows, each row is interpreted as an individual
                coordinate to convert.
            corners (np.ndarray): cartesian coordinates of the corners.
        Returns:
            2-column np.ndarray of cartesian coordinates for each barycentric
            coordinate provided.
        '''

        # if corners is None:
        #    corners = self.polycorners(bary.shape[-1])
        # else:
        #    cart = None


        if len(bary.shape) > 1 and bary.shape[1] > 1:
            cart = np.array([np.sum(b / np.sum(b) * corners.T, axis=1) for b in bary])
        else:
            cart = np.sum(bary / np.sum(bary) * corners.T, axis=1)

        return cart






    def pentagon_plot(self, dfs,labels = None, space5D=None,label_offset = 0.06,colors=None,alpha = 0.4):
        corners = self.polycorners(ncorners=5)



        fig = plt.figure(figsize=(10,9))
        ax = plt.subplot()
        lines=combinations(corners,2)
        for x in lines:
            line=np.transpose(np.array(x))
            ax.plot(line[0],line[1],c='black')
        for c,el in zip(corners,labels):
            ax.text(c[0]+label_offset,c[1],el,fontsize=16)


        ba = self.bary2cart(dfs.values/100,corners = corners)
        ax.scatter(ba[:,0],ba[:,1],alpha = alpha)
        plt.show()


        ax.set_axis_off()


    def tetrahedron_plot(self, df,labels,space5D=None,elev=-15,azim=15,label_offset = 0.06,colors=None,alpha = 0.5):
        corners = np.array([[0,0,0],
                 [1,0,0],
                 [0.5,np.sqrt(3)/2,0],
                 [0.5,0.28867513, 0.81649658],
                  [0.5       , 0.28867513, 0.20412415]])

        fig = plt.figure(figsize=(10,9))
        ax = Axes3D(fig)
        ax.view_init(elev=elev, azim=azim)
        lines=combinations(corners,2)
        for x in lines:
            line=np.transpose(np.array(x))
            ax.plot(line[0],line[1],line[2],c='black',alpha=1)

        if space5D is not None:
            D3 = self.bary2cart(space5D.values/100,corners = corners)
            ax.scatter(D3[:,0],D3[:,1],D3[:,2],s=5,c='grey',alpha=0.1)

        if colors is not None:
            for df,c in zip(dfs,colors):
                D3 = bary2cart(df.values/100,corners = corners)
                ax.scatter(D3[:,0],D3[:,1],D3[:,2],alpha=alpha,c=c,cmap='bwr_r',vmin=np.quantile(colors,0.1),vmax=np.quantile(colors,0.9))
        else:
            # for df in dfs:
            D3 = self.bary2cart(df.values/100,corners = corners)
            ax.scatter(D3[:,0],D3[:,1],D3[:,2],alpha=alpha)


        for c,el in zip(corners,labels):
            ax.text(c[0]+label_offset,c[1]-label_offset,c[2]+label_offset,el,fontsize=16)

        ax.set_axis_off()
        fig.show()



def main():
    root = Tk()

    # d = {'Nb': (0, 35.7), 'Mo': (0, 16.3), 'Ta': (54, 34.9), 'W': (36, 3.1), 'Ag': (10, 10)}
    # d = pd.read_csv('0004967_0004960_Cantor-O_5at%_EDX.csv').iloc[:,1:]
    d = {'Nb': (0, 35.7), 'Mo': (0, 16.3), 'Ta': (54, 34.9), 'W': (36, 3.1), 'Ti': (10, 10)}

    df = pd.DataFrame(data = d)/100



    app = MultidimensionPlot(root, df)


    root.mainloop()

if __name__ =='__main__':
    main()




