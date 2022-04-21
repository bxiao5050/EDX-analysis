from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
import matplotlib
from matplotlib.figure import Figure



class Pie_target_positions(FigureCanvasTkAgg):
    def __init__(self, fig, master, labels, colors = None):
        super().__init__(fig, master =master)

        self.elee = labels
        self.colors = colors


        fig.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1)
        self.ax = fig.add_subplot(111)
        self.sizes = [1/len(self.elee) for i in self.elee]
        self.my_pie, text = self.ax.pie(self.sizes, labels=self.elee, colors = self.colors, wedgeprops = {'linewidth' :0.5, 'edgecolor' :'black'})

    #set color
    def set_alpha(self, alpha):
        for p in self.my_pie:
            p.set_alpha(alpha)
        self.draw()

    def update_pos(self, elee, colors, startangle):
        self.elee = elee
        self.ax.clear()
        self.my_pie, t = self.ax.pie(self.sizes, labels=elee, colors = colors,startangle = startangle, wedgeprops = {'linewidth' :0.5, 'edgecolor' :'black'})

    def update_color(self, ele, color):
        self.my_pie[self.elee.index(ele)].set_facecolor(color)
        # self.my_pie[self.elee.index(ele)].set_color(color)
        self.draw()




class View_of_target_sequence(Frame):
    def __init__(self, master, elenum):
        super().__init__(master)
        self.elenum = elenum

        fig = Figure(figsize=(1.5, 1.5), dpi=100)
        fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        self.canvas = FigureCanvasTkAgg(fig, master=master)
        self.ax = fig.add_subplot()

        self.canvas.get_tk_widget().pack()

        self.update_pos(0)

    def update_pos(self, startangle):
        self.ax.clear()
        a = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10', '11', '12', '13','14']
        labels = a[0: self.elenum]
        self.my_pie, text = self.ax.pie([1/self.elenum]*self.elenum, labels=labels, colors = ['white']*self.elenum,startangle = startangle, labeldistance = 0.6, wedgeprops = {'linewidth' :1, 'edgecolor' :'black'})

        for t in text:
            t.set_horizontalalignment('center')
            t.set_size(15)


        self.canvas.draw()



def main():
    root = Tk()
    fig = Figure(figsize=(2,2))
    elee = ['Frogs', 'Hogs', 'Dogs', 'Logs', 'ss']

    app = View_of_target_sequence(root, 4)
    app.pack()


    # app = Pie_target_positions(fig, root, elee)
    # app.get_tk_widget().pack(fill='both', expand=0)


    root.mainloop()

if __name__ == '__main__':
    main()
