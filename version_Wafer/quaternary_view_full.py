import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from itertools import combinations
import pandas as pd
from matplotlib.widgets import RectangleSelector
try:
    from threed_panel import Threed_panel
    from coords_canvasvs import Coords_canvasvs
    from textInf import TextInf
except:
    from version_Wafer.threed_panel import Threed_panel
    from version_Wafer.coords_canvasvs import Coords_canvasvs
    from version_Wafer.textInf import TextInf
from tkinter import *
from tkinter import filedialog
import os
from datetime import *
import subprocess
class Quaternary_view_full(Frame):
    def __init__(self, master, df):
        super().__init__(master)
        self.pack(fill = 'both', expand =1)

        menubar = Menu(self)

        docmanu = Menu(menubar)
        docmanu.add_command(label="Algorithm: tetrahedral plot diagram", command=self.on_wafer_figure)
        menubar.add_cascade(label="Document", menu=docmanu)
        master.config(menu=menubar)


        df.insert(len(df.columns), '', 0) # columns saved for other parameters (e.g. current)
        self.df = df

        panel_f = Frame(self) #left panel
        self.panel3D = Threed_panel(self) #right panel
        self.panel3D.set_ele_columns(df.columns)

        panel_f.pack(side = 'left', anchor = 'n')
        self.panel3D.pack(side = 'right', fill ='both', expand =1)

        # self.addB = Button(panel_f, text = 'import data', command = self.on_importData)
        # self.addB.pack()
        self.canvas = Coords_canvasvs(panel_f)
        self.canvas.pack(pady = (20,3))
        # Button(panel_f, text = 'show cartesian coordinates for selected points', command = self.on_show_selected_information).pack()
        inf_f = LabelFrame(panel_f, text = 'information for selected points')
        inf_f.pack(fill = 'both', expand = True)

        self.inf = TextInf(inf_f) #information textbox

        # inf = TextInf(w,self._get_pos_eds_Cartesian())

        self.inf.pack(fill = 'both', expand = True)

        #multi selections
        self.cid1 = self.canvas.canvas.mpl_connect('button_press_event', self.on_click)
        self.RS = RectangleSelector(self.canvas.ax, self.line_select_callback,
                                               drawtype='box', useblit=True,
                                               button=[1, 3],  # don't use middle button
                                               minspanx=5, minspany=5,
                                               spancoords='pixels',
                                               interactive=False)
        self.canvas.b_clear.config(command = self._on_clear)

        self.on_importData()

    def on_wafer_figure(self):
        subprocess.Popen('18_5371Shimura.pdf',shell=True)



    def _get_pos_eds_Cartesian(self):
        rows = np.array(self.canvas.get_clicked_index())
        selected_df = self.df.iloc[rows-1, :] #selected EDX
        bary_arr=selected_df.iloc[:, 0:4].values
        #selected Cartesian coords
        cartesian_points=self.panel3D.get_cartesian_array_from_barycentric(bary_arr)
        cartesian_df = pd.DataFrame(data = cartesian_points, index = selected_df.index,columns = ['x', 'y', 'z'])
        pos_eds_cartesian = pd.concat([selected_df, cartesian_df], axis = 1)
        pos_eds_cartesian.sort_index(inplace=True)
        pos_eds_cartesian.reset_index(level = 0, inplace = True)

        return pos_eds_cartesian




    def on_importData(self):
        # filename =  filedialog.askopenfilename(title = "Select file",filetypes = (("csv file","*.csv"),("all files","*.*")))
        # if len(filename) == 0: return


        # self.df = pd.read_csv(filename, header = 0, index_col = 0, sep = ';')/100
        self.panel3D.plot_3d(self.df)
        self.canvas.importData(self.df)
        # self.canvas.config(text = os.path.basename(filename))
        # self.addB.config(state = 'disabled')

    def _on_clear(self):
        self.canvas._on_clear()
        self.on_show_in_3d()



#override click on canvas method
    def on_click(self, event):
        self.canvas.on_click(event)
        self.on_show_in_3d()

    def line_select_callback(self, eclick, ereleas):
        self.canvas.line_select_callback(eclick, ereleas)
        self.on_show_in_3d()


    def on_show_in_3d(self):
        rows = np.array(self.canvas.get_clicked_index())
        self.panel3D.plot_highlight(self.df.iloc[rows-1, :])
        #update information textbox
        if len(rows) == 0:
            self.inf.clear()
        else:
            self.inf.insert_text(self._get_pos_eds_Cartesian())



def main():


    root = Tk()

    df = pd.read_csv('v3.csv', header = 0, index_col = 0, sep = ';')/100
    app = Quaternary_view_full(root, df)


    root.title('Quaternary view')




    root.mainloop()

if __name__ =='__main__':
    main()
