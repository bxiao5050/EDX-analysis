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


class MultidimensionPlot_3d(Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.pack(fill = 'both', expand = True)
        Button(self, text = 'add other EDX data', fg = 'red', command = self.on_add_other_data).pack()
        fig = Figure(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        self.ax = Axes3D(fig)
        self.canvas.get_tk_widget().pack(fill='both', expand=1)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()

        self.ele_columns = data.columns # elements columns and sequence

        # corners = self.polycorners(ncorners=len(self.ele_columns))
        # self.corners = corners
        # lines=combinations(corners,2)
        # for x in lines:
        #     line=np.transpose(np.array(x))
        #     self.ax.plot(line[0],line[1],c='black')
        # for c,el in zip(corners,data.columns):
        #     self.ax.text(c[0]+0.06,c[1],el,fontsize=16)

        # ba = self.bary2cart(data.values, corners = corners)
        # self.ax.scatter(ba[:,0],ba[:,1],alpha = 0.4)

        self.tetrahedron_plot(data, self.ele_columns)

        self.canvas.draw()

    def on_add_other_data(self):
        filename =  filedialog.askopenfilename(title = "Select file",filetypes = (("csv file","*.csv"),("all files","*.*")))
        if len(filename) == 0: return

        # self.df = pd.read_csv('v3.csv', header = 0, index_col = 0, sep = ';')/100
        df = pd.read_csv(filename, header = 0, index_col = 0, sep = ';')

        # get the element columns with the certain sequence
        data = pd.DataFrame()

        for ele in self.ele_columns:
            try:
                data[ele] = df[ele]
            except:
                messagebox.showerror(message = f'no column of "{ele}" in imported data')
                return

        ba = self.bary2cart(data.values, corners = self.corners)

        self.ax.scatter(ba[:,0],ba[:,1],ba[:,2],alpha = 0.4)
        self.canvas.draw()


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





    def tetrahedron_plot(self, df,labels,space5D=None,elev=-15,azim=15,label_offset = 0.06,colors=None,alpha = 0.5):

        n = len(df.columns) - 1
        theta = [2*np.pi/n*i for i in range(n)]
        corners =[(np.sin(t), np.cos(t), 0 )for t in theta]

        corners.append([0, 0, 0.8])
        corners = np.array(corners)
        self.corners = corners





        lines=combinations(corners,2)
        for x in lines:
            line=np.transpose(np.array(x))
            self.ax.plot(line[0],line[1],line[2],c='black',alpha=1)

        if space5D is not None:
            D3 = self.bary2cart(space5D.values/100,corners = corners)
            self.ax.scatter(D3[:,0],D3[:,1],D3[:,2],s=5,c='grey',alpha=0.1)

        if colors is not None:
            for df,c in zip(dfs,colors):
                D3 = bary2cart(df.values/100,corners = corners)
                self.ax.scatter(D3[:,0],D3[:,1],D3[:,2],alpha=alpha,c=c,cmap='bwr_r',vmin=np.quantile(colors,0.1),vmax=np.quantile(colors,0.9))
        else:
            # for df in dfs:
            D3 = self.bary2cart(df.values/100,corners = corners)
            self.ax.scatter(D3[:,0],D3[:,1],D3[:,2],alpha=alpha)


        for c,el in zip(corners,labels):

            self.ax.text(c[0]+label_offset,c[1]-label_offset,c[2]+label_offset,el,fontsize=16)

        # ax.set_axis_off()
        self.canvas.draw()



def main():
    root = Tk()

    # d = {'Nb': (0, 35.7), 'Mo': (0, 16.3), 'Ta': (54, 34.9), 'W': (36, 3.1), 'Ag': (10, 10)}
    # d = pd.read_csv('0004967_0004960_Cantor-O_5at%_EDX.csv').iloc[:,1:]
    d = {'Nb': (0, 35.7), 'Mo': (0, 16.3), 'Ta': (54, 34.9), 'W': (36, 3.1)}

    df = pd.DataFrame(data = d)/100



    app = MultidimensionPlot_3d(root, df)


    root.mainloop()

if __name__ =='__main__':
    main()




