import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)

from tkinter import *
from tkinter import filedialog, colorchooser
from tkinter import ttk
try:
    from pie_target_positions2 import View_of_target_sequence
except:
    from version_Wafer.pie_target_positions2 import View_of_target_sequence


class Pie_slice_setting(Frame):
    def __init__(self, master, data,elements):
        super().__init__(master)

        #select
        f_select = LabelFrame(self, text = 'Select')
        self.position_var = BooleanVar()
        self.position_var.set(False)
        Checkbutton(f_select, text = 'Target position',   variable = self.position_var, command = self.on_position_check).grid(row = 0, column =0, padx = (5,5), pady = (5,5))
        self.legend_var = BooleanVar()
        self.legend_var.set(False)
        Checkbutton(f_select, text = 'Legend',   variable = self.legend_var, command = self.on_legend_check).grid(row = 0, column =1, padx = (5,5), pady = (5,5))
        self.waferCircle_var = BooleanVar()
        self.waferCircle_var.set(False)
        Checkbutton(f_select, text = 'Wafer background',   variable = self.waferCircle_var,  command = self.on_waferCircle_check).grid(row = 0, column =2, padx = (5,5), pady = (5,5))


        #artget position
        f_location = LabelFrame(self, text = 'Target location', relief = 'raised', fg = 'blue')
        el = [v for v in data.columns[3:]]

        frame_r = LabelFrame(f_location, text = 'anticlockwise rotation (deg)')
        f1 = Frame(f_location)
        lf = LabelFrame(f1, text = 'target sequence')
        self.target_sequence = View_of_target_sequence(lf, len(el))
        self.target_sequence.pack()
        frame_s = LabelFrame(f1, text = 'element sequence (anticlockwise)')
        frame_s.pack(side = 'left', padx = (5,5), pady = (5,5))
        lf.pack(side = 'left', padx = (80,5), pady = (5,5))
        f1.pack( padx = (5,5), pady = (5,5))
        frame_r.pack( padx = (5,5), pady = (5,5))
        self.sequence = Ele_sequence(frame_s, elements)
        self.sequence.pack()
        Button(frame_s, text = 'set sequence',  command = self.on_tarpos).pack()
         #rotation
        self.v_rotation = DoubleVar()
        Scale(frame_r, variable = self.v_rotation, from_ = 0, to =360, length = 400, orient = 'horizontal', command = self.on_tarpos).pack(padx = (10,10))
        Button(f_location, text = 'apply to figure', width = 15, fg = 'red', command = self.on_update_pie).pack(padx = (10,10), pady = (5,5))

        #2. piechart
        f_pie = LabelFrame(self, text = 'Piechart configuration', fg= 'blue')
        #scattermarker
        self.pie_types = ttk.Combobox(f_pie, values = ['s', 'o', '.', 'v', '^', '*', 'P','D', 'X'], width = 5,state = 'disabled')
        self.pie_types.current(0)
        self.pie_types.bind('<<ComboboxSelected>>', self._on_set_piechart)
        #size
        self.pie_size = DoubleVar()
        self.pie_size.set(1)
        self.pieSize = Scale(f_pie, from_=0.8, to=1.5, resolution = 0.02, orient = 'horizontal', variable= self.pie_size, width = 10, command =self._on_set_piechart)
        #cmap
        self.scatter_cmap_cb = ttk.Combobox(f_pie, values = ['jet'], state = 'disabled', width = 10)
        self.scatter_cmap_cb.current(0)
        self.scatter_cmap_cb.bind('<<ComboboxSelected>>', self._on_set_piechart)
        #pieEdge_color
        self.pieEdge_color = StringVar()
        self.pieEdge_color.set('black')
        self.pieEdge_color_l = Label(f_pie, text = '      ', bg = 'black')
        self.pieEdge_color_l.bind('<Button-1>', self.on_pieEdge_color)

        #slinewidth
        self.pie_linewidth = DoubleVar()
        self.pie_linewidth.set(0.5)
        self.pie_linewidth_sp = Scale(f_pie, from_=0, to=5, resolution = 0.1,orient = 'horizontal', variable= self.pie_linewidth, width = 10, command = lambda e = '':self._on_set_piechart(e))
        #scatteralpha
        self.pie_alp = DoubleVar()
        self.pie_alp.set(1.0)
        self.pie_alp_sp = Scale(f_pie, from_=0.3, to=1, resolution = 0.1,orient = 'horizontal', variable= self.pie_alp, width = 10, command = self.on_pie_alpha)

        Label(f_pie, text = 'piechart type:').grid(row = 0, column = 0, padx = (5,0), sticky = 'w')
        self.pie_types.grid(row = 0, column = 1, padx = (5,5), sticky = 'w')
        Label(f_pie, text = 'size:').grid(row = 0, column = 2, padx = (5,0), sticky = 'w')
        self.pieSize.grid(row = 0, column = 3, padx = (5,5), sticky = 'w')
        Label(f_pie, text = 'color type:').grid(row = 1, column = 0, padx = (5,0), sticky = 'w')
        self.scatter_cmap_cb.grid(row = 1, column = 1, padx = (5,5), sticky = 'w')
        Label(f_pie, text = 'edge color:').grid(row = 1, column = 2, padx = (5,0), sticky = 'w')
        self.pieEdge_color_l.grid(row = 1, column = 3, padx = (5,5), pady = (5,5), sticky = 'w')
        Label(f_pie, text = 'edge width:').grid(row = 2, column = 0, padx = (5,0), sticky = 'w')
        self.pie_linewidth_sp.grid(row = 2, column = 1, padx = (5,5), sticky = 'w')
        Label(f_pie, text = 'transparent:').grid(row = 2, column = 2, padx = (5,0), sticky = 'w')
        self.pie_alp_sp.grid(row = 2, column = 3, padx = (5,5), sticky = 'w')


        #legend
        f_legend = LabelFrame(self, text = 'Legend configuration', fg = 'blue')
        self.legend_cb = ttk.Combobox(f_legend, values = ['ele', 'percentage','ele + percentage', 'ele + high percentage', 'without title'], state = 'disabled', width = 20)
        self.legend_cb.current(0)
        self.legend_cb.bind('<<ComboboxSelected>>', self.on_set_legend_type)
        #fontsize
        self.legendFont = IntVar()
        self.legendFont.set(13)
        self.legend_font = Spinbox(f_legend, from_ = 1, to = 30, increment = 1, textvariable = self.legendFont, width = 4, wrap = False, command = lambda event = '': self.on_set_legend(event), state = 'readonly')
        #fontcolor
        self.legendColor = StringVar()
        self.legendColor.set('black')
        self.legendColor_l = Label(f_legend, text = '      ', bg = 'black')
        self.legendColor_l.bind('<Button-1>', self.on_legendColor)
        #fontstyle
        self.legendFontStyle = ttk.Combobox(f_legend, values = ['normal', 'italic'], width = 8)
        self.legendFontStyle.current(0)
        self.legendFontStyle.bind('<<ComboboxSelected>>', self.on_set_legend)
        #fontweight
        self.legendFontWeight = ttk.Combobox(f_legend, values = ['normal',  'roman', 'bold'], width = 8)
        self.legendFontWeight.current(2)
        self.legendFontWeight.bind('<<ComboboxSelected>>', self.on_set_legend)
        # title decimal
        self.legendDecimal = IntVar()
        self.legendDecimal.set(1)
        self.legend_decimal = Spinbox(f_legend, from_ = 0, to = 1, increment = 1, textvariable = self.legendDecimal, state = 'disabled', width = 4, wrap = False, command = lambda event = '': self.on_set_legend(event))

        Label(f_legend, text = 'legend type:').grid(row = 0, column = 0, padx = (5,0), sticky = 'w')
        self.legend_cb.grid(row = 0, column = 1, padx = (5,5), sticky = 'w')
        Label(f_legend, text = 'font size:').grid(row = 0, column = 2, padx = (5,0), sticky = 'w')
        self.legend_font.grid(row = 0, column = 3, padx = (5,5), sticky = 'w')
        Label(f_legend, text = 'font color:').grid(row = 1, column = 0, padx = (5,0), pady=(5,5), sticky = 'w')
        self.legendColor_l.grid(row = 1, column = 1, padx = (5,5), pady=(5,5), sticky = 'w')
        Label(f_legend, text = 'font style:').grid(row = 1, column = 2, padx = (5,0), sticky = 'w')
        self.legendFontStyle.grid(row = 1, column = 3, padx = (5,5),pady = (5,5), sticky = 'w')
        Label(f_legend, text = 'font weight:').grid(row = 2, column = 0, padx = (5,0), sticky = 'w')
        self.legendFontWeight.grid(row = 2, column = 1, padx = (5,5), sticky = 'w')
        Label(f_legend, text = 'decimal place:').grid(row = 2, column = 2, padx = (5,5), sticky = 'w')
        self.legend_decimal.grid(row = 2, column = 3, padx = (5,5), pady = (5,5),sticky = 'w')


        #set center patch circle
        f_patch_c = LabelFrame(self, text = 'Wafer background configuration', fg= 'blue')
        self.patch_fill = BooleanVar()
        self.patch_fill.set(True)
        patch_fill_cb = Checkbutton(f_patch_c, text = '', variable = self.patch_fill, command = self.on_set_patch)
        #facecolor
        self.patchFaceColor = StringVar()
        self.patchFaceColor.set('lightblue')
        self.patchFaceColor_l = Label(f_patch_c, text = '      ', bg = 'lightblue')
        self.patchFaceColor_l.bind('<Button-1>', self.on_patchFaceColor)
        #EdgeColor
        self.patchEdgeColor = StringVar()
        self.patchEdgeColor.set('black')
        self.patchEdgeColor_l = Label(f_patch_c, text = '      ', bg = 'black')
        self.patchEdgeColor_l.bind('<Button-1>', self.on_patchEdgeColor)
        #slinewidth
        self.patchLineWidth = DoubleVar()
        self.patchLineWidth.set(1)
        self.patchLineWidth_sp = Scale(f_patch_c, from_=0, to=10, resolution = 0.1,orient = 'horizontal', variable= self.patchLineWidth, width = 10, command = self.on_set_patch)
        #patchRadius
        self.patchRadius = DoubleVar()
        self.patchRadius.set(50)
        self.patchRadius_sp = Scale(f_patch_c, from_=49, to=52.5, resolution = 0.1,orient = 'horizontal', variable= self.patchRadius, width = 10, command = self.on_set_patch)
        #scatteralpha
        self.patchAlpha = DoubleVar()
        self.patchAlpha.set(0.5)
        self.patchAlpha_sp = Scale(f_patch_c, from_=0, to=1, resolution = 0.1,orient = 'horizontal', variable= self.patchAlpha, width = 10, command = self.on_set_patch)

        Label(f_patch_c, text = 'fill the circle:').grid(row = 0, column = 0, padx = (5,0), sticky = 'w')
        patch_fill_cb.grid(row = 0, column = 1, padx = (5,5), sticky = 'w')
        Label(f_patch_c, text = 'fill color:').grid(row = 0, column = 2, padx = (5,0), sticky = 'w')
        self.patchFaceColor_l.grid(row = 0, column = 3, padx = (5,5), sticky = 'w')
        Label(f_patch_c, text = 'edge color:').grid(row = 1, column = 0, padx = (5,0), sticky = 'w')
        self.patchEdgeColor_l.grid(row = 1, column = 1, padx = (5,5), sticky = 'w')
        Label(f_patch_c, text = 'edge width:').grid(row = 1, column = 2, padx = (5,0), sticky = 'w')
        self.patchLineWidth_sp.grid(row = 1, column = 3, padx = (5,5), pady = (5,5), sticky = 'w')
        Label(f_patch_c, text = 'radius:').grid(row = 2, column = 0, padx = (5,0), sticky = 'w')
        self.patchRadius_sp.grid(row = 2, column = 1, padx = (5,5), sticky = 'w')
        Label(f_patch_c, text = 'transparent:').grid(row = 2, column = 2, padx = (5,0), sticky = 'w')
        self.patchAlpha_sp.grid(row = 2, column = 3, padx = (5,5), sticky = 'w')

        #file panel
        exp_p = LabelFrame(self, text = 'Files', fg = 'red') #export button panel
        Button(exp_p, text = 'export image').grid(row = 0, column =0, sticky = 'nw', padx = (5,5), pady = (3,3))
        Button(exp_p, text = 'save as template', bg = 'lightblue', command = self.on_save_template).grid(row = 0, column =2, sticky = 'nw', padx = (5,5), pady = (3,3))
        Button(exp_p, text = 'import template', bg = 'lightblue', command = self.on_import_template).grid(row = 0, column =3
            , sticky = 'nw', padx = (5,5), pady = (3,3))


        f_select.pack(anchor = 'nw', pady = (10,10), fill = 'both', padx = (5,5))
        f_location.pack(anchor = 'nw', pady = (10,10), fill = 'both', padx = (5,5))
        f_pie.pack(anchor = 'nw', pady = (10,10), fill = 'both', padx = (5,5))
        f_legend.pack(anchor = 'nw', pady = (10,10), fill = 'both', padx = (5,5))
        f_patch_c.pack(anchor = 'nw', pady = (0,10), fill = 'both', padx = (5,5))
        exp_p.pack(anchor = 'nw', pady = (0,10), fill = 'both', padx = (5,5))


    # file
    def on_save_template(self):
        pass

    def on_import_template(self):
        pass

    #set patch circle
    def on_patchfill(self):
        pass

    def on_patchFaceColor(self, e=''):
        pass

    def on_patchEdgeColor(self, e=''):
        pass
    def on_set_patch(self, e=''):
        pass

    #select
    def on_position_check(self, e=''):
        pass

    def on_legend_check(self, e=''):
        pass

    def on_waferCircle_check(self, e=''):
        pass


    #set legend
    def on_set_legend(self, e = ''):
        pass

    def on_legendColor(self, e =""):
        pass

    #target position
    def on_update_pie(self, e=''):
        pass

    def on_tarpos(self, e = ''):
        pass

    #piechart
    def _on_set_piechart(self,e):
        pass

    def on_pieEdge_color(self,e):
        pass
    def on_pie_alpha(self, e):
        pass





class Ele_sequence(Frame):
    def __init__(self, master, elements):
        super().__init__(master)
        self.elements = elements
        self.ele_l, self.ele_e, self.ele_var = [], [], []


        for i, t in enumerate(elements.values()):
            self.ele_l.append(Label(self, text =t))
            self.ele_var.append(IntVar())

            self.ele_e.append(Entry(self, textvariable = self.ele_var[-1], width =5))
            self.ele_var[-1].set(i+1)
            # self.ele_e[-1].insert(0, i+1)

            self.ele_l[-1].grid(row = i, column = 0, padx = (3,3), pady = (3,3))
            self.ele_e[-1].grid(row = i, column = 1, padx = (3,3), pady = (3,3))
    #new elements
    def get_eles(self):
        ind = np.array([v.get() for v in self.ele_var])
        new_eles = [list(self.elements.values())[i] for i in np.argsort(ind)]
        return new_eles

    def get_eleEntries(self):
        return [v.get() for v in self.ele_var]

    def set_eleEntries(self, inds):
        [entry.set(ind) for entry, ind in zip(self.ele_var, inds)]





def main():

    root = Tk()
    data = pd.read_csv('aa.csv')
    eles = [v for v in data.columns[3:]]

    elements = {ele:ele for ele in eles}
    app = Pie_slice_setting(root, data, elements = elements)
    app.pack()


    root.mainloop()

if __name__ == '__main__':
    main()
