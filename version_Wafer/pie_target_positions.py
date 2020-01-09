from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
import matplotlib
from matplotlib.figure import Figure


class Pie_target_positions(LabelFrame):
    def __init__(self, master, labels, colors = None):
        super().__init__(master)
        self.labels = labels
        self.colors = colors
        self.v_rotation = DoubleVar() #rotation

        frame_f = Frame(self)
        frame_scales = Frame(self)

        frame_f.pack()
        frame_scales.pack()
        Button(frame_f, text = 'set', command = lambda frame_scales=frame_scales: self.on_start_set(frame_scales)).pack()
        self.init_fig(frame_f)
        self.pie_plot()

    def on_start_set(self, frame_scales):
        position = PhotoImage(file='position.png')
        frame_r = LabelFrame(frame_scales, text = 'anticlockwise rotation (deg)')
        f = LabelFrame(frame_scales,text ='')

        lf = LabelFrame(f, text = 'view of sequence')
        l = Label(lf,image = position)
        l.pack()
        l.image = position

        frame_s = LabelFrame(f, text = 'element sequence (anticlockwise)')
        frame_s.pack(side = 'left', padx = (5,5), pady = (5,5))
        lf.pack(side = 'left', padx = (80,5), pady = (5,5))
        f.pack( padx = (5,5), pady = (5,5))
        frame_r.pack( padx = (5,5), pady = (5,5))

        Scale(frame_r, variable = self.v_rotation, from_ = 0, to =360, length = 400, orient = 'horizontal', command = self.on_update_pie).pack(padx = (10,10))
        self.sequence = Ele_sequence(frame_s, self.labels)
        self.sequence.pack()
        Button(frame_s, text = 'set sequence', fg = 'blue', command = self.update_pie).pack()


    #change color
    def set_slice_color(self, eleindex, newcolor):
        self.my_pie[eleindex].set_color(newcolor)
        self.colors[eleindex] = self.my_pie[eleindex].get_edgecolor()
        self.canvas.draw()


    #update pie
    def update_pie(self):

        ele_index = self.sequence.get_sequence()
        newSizes = [self.sizes[i] for i in ele_index]
        newLabels = [self.labels[i] for i in ele_index]
        newColors = [self.colors[i] for i in ele_index]

        self.ax.clear()


        self.my_pie, t = self.ax.pie(newSizes, labels=newLabels, colors = newColors, startangle = self.v_rotation.get(), wedgeprops = {'linewidth' :0.5, 'edgecolor' :'black'})
        self.canvas.draw()


    #return values for the outside
    def get_pie_setting(self):
        return {'startangle': self.v_rotation.get(), 'sequence': self.sequence.get_sequence(), 'colors': self.colors}











def main():
    root = Tk()
    labels = ['Frogs', 'Hogs', 'Dogs', 'Logs', 'ss']

    app = Pie_target_positions(root, labels)
    app.pack()


    root.mainloop()

if __name__ == '__main__':
    main()
