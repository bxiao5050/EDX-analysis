import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)

from tkinter import *
from tkinter import filedialog, colorchooser
from tkinter import ttk
import pickle
try:
    from pie_slice_setting import Pie_slice_setting
except:
    from version_Wafer.pie_slice_setting import Pie_slice_setting

class Pie_slice_setting_on(Pie_slice_setting):
    def __init__(self, master, data, plot_pie, tar_pos, plot_leg,elements,colorlist):
        super().__init__(master, data,elements)
        self.data =data
        self.plot_pie =plot_pie
        self.tar_pos =tar_pos
        self.plot_leg =plot_leg
        self.elements = elements
        self.colorlist = colorlist

        #override legend button
        for ele, b in plot_leg.get_B().items():
            b.config(command = lambda ele=ele:self._on_legend(ele))





    def on_save_template(self):
        path = filedialog.asksaveasfilename(title='Select path')
        if not path:
            return

        pickle.dump(self.get_all_paras(), open( path+'.EDX_piechart_template', "wb" ) )
        messagebox.showinfo(message = 'EDX template saved!')

    def on_import_template(self):
        path = filedialog.askopenfilename(title = 'Select file',filetypes = (("EDX template file","*.EDX_piechart_template"),("all files","*.*")))
        if not path:
            return
        self.set_all_paras(pickle.load(open( path, "rb" )))


    #override legend button
    def _on_legend(self, ele, color = ''):
        if len(color) ==0:
            newcolor = colorchooser.askcolor()[1] #select color
        else:
            newcolor = color
        self.plot_leg.get_B().get(ele).config(bg = newcolor)
        self.plot_pie.update_color(ele, newcolor)
        #change legend pie
        self.tar_pos.update_color(ele, newcolor)
        self.colorlist = self.plot_leg.get_colorlist()#update

    #center circle (wafer background)
    def on_patchFaceColor(self, e='', color = ''):
        if len(color) == 0:
            color = colorchooser.askcolor(title ="Choose color")[1]
        self.patchFaceColor.set(color)
        self.patchFaceColor_l.config(bg = self.patchFaceColor.get())
        self.on_set_patch()

    def on_patchEdgeColor(self, e='', color = ''):
        if len(color) == 0:
            color = colorchooser.askcolor(title ="Choose color")[1]
        self.patchEdgeColor.set(color)
        self.patchEdgeColor_l.config(bg = self.patchEdgeColor.get())
        self.on_set_patch()

    def on_set_patch(self, e=''):
        self.plot_pie.set_circle(facecolor=self.patchFaceColor.get(), edgecolor=self.patchEdgeColor.get(), linewidth=self.patchLineWidth.get(), radius=self.patchRadius.get(), alpha=self.patchAlpha.get(), fill = self.patch_fill.get())

    #select
    def on_position_check(self, e=''):
        if self.position_var.get() is False:
            self.tar_pos.get_tk_widget().place_forget()
        else:
            self.tar_pos.get_tk_widget().place(x=700,y=0)
        self.plot_pie.draw()

    def on_legend_check(self, e=''):
        if self.legend_var.get() is False:
            self.plot_leg.place_forget()
        else:
            self.plot_leg.place(x = 850, y = 640)
        self.plot_pie.draw()

    def on_waferCircle_check(self, e=''):
        self.plot_pie.canvas_c.set_visible(self.waferCircle_var.get())
        self.plot_pie.draw()


    #set legend
    def on_set_legend_type(self, e = ''):
        pass

    def on_set_legend(self, e = ''):
        self.plot_leg.set_legend(fontsize= self.legendFont.get(), fontstyle = self.legendFontStyle.get(), fontweight = self.legendFontWeight.get(), color = self.legendColor.get())

    def on_legendColor(self, e ="", color = ''):
        if len(color) ==0:
            color = colorchooser.askcolor(title ="Choose color")[1]
        self.legendColor_l.config(bg = color)
        self.legendColor.set(color)

        self.on_set_legend()


    #target position
    def on_update_pie(self, e=''):
        #piechart plot
        eles = self.sequence.get_eles()
        elee = [self.elements[i] for i in eles]
        colors = [self.colorlist[ele] for ele in eles]

        self.plot_pie.update_pie(elee=elee, colors=colors,startangle=self.v_rotation.get(), radius=self.pie_size.get(), alpha=self.pie_alp.get(), linewidth=self.pie_linewidth.get(), edgecolor=self.pieEdge_color.get())
        # #center circle
        # self.on_set_patch()




    def on_tarpos(self, e = ''):
        eles = self.sequence.get_eles()

        newLabels = [self.elements[i] for i in eles]
        newColors = [self.colorlist[i] for i in eles]
        self.tar_pos.update_pos(newLabels, newColors, self.v_rotation.get())
        self.target_sequence.update_pos(self.v_rotation.get()) #sequence
        self.tar_pos.draw()



    #piechart
    def _on_set_piechart(self,e=''):
        for pie in self.plot_pie.get_pieCharts().values():
            for p in pie:
                p.set_radius(self.pie_size.get())
                p.set_lw(self.pie_linewidth.get())
        self.plot_pie.draw()


    def on_pieEdge_color(self,e='', color = ''):
        if len(color) == 0:
            color = colorchooser.askcolor(title ="Choose color")[1]
        self.pieEdge_color.set(color)
        self.pieEdge_color_l.config(bg = color)
        for pie in self.plot_pie.get_pieCharts().values():
            for p in pie:
                p.set_edgecolor(self.pieEdge_color.get())
        self.plot_pie.draw()

    def on_pie_alpha(self, e=''):
        #pie chart
        for pie in self.plot_pie.get_pieCharts().values():
            for p in pie:
                p.set_alpha(self.pie_alp.get())
        self.plot_pie.draw()
        #target position
        self.tar_pos.set_alpha(self.pie_alp.get())


    #export and import
    def get_all_paras(self):
        para = {}
        para['position_var'] = self.position_var.get()
        para['legend_var'] = self.legend_var.get()
        para['waferCircle_var'] = self.waferCircle_var.get()
        para['ele'] = self.sequence.get_eleEntries() #target sequence
        para['v_rotation'] = self.v_rotation.get()
        para['pie_size'] = self.pie_size.get()
        para['pieEdge_color'] = self.pieEdge_color.get()
        para['pie_linewidth'] = self.pie_linewidth.get()
        para['pie_alp'] = self.pie_alp.get()
        para['legendFont'] = self.legendFont.get()
        para['legendColor'] = self.legendColor.get()
        para['legendFontStyle'] = self.legendFontStyle.current()
        para['legendFontWeight'] = self.legendFontWeight.current()
        para['patch_fill'] = self.patch_fill.get()
        para['patchFaceColor'] = self.patchFaceColor.get()
        para['patchEdgeColor'] = self.patchEdgeColor.get()
        para['patchLineWidth'] = self.patchLineWidth.get()
        para['patchRadius'] = self.patchRadius.get()
        para['patchAlpha'] = self.patchAlpha.get()

        para['legendB_C'] = self.plot_leg.get_colorlist()# legend button color

        return para

    def set_all_paras(self, para):
        self.position_var.set(para['position_var'])
        self.legend_var.set(para['legend_var'])
        self.waferCircle_var.set(para['waferCircle_var'])
        self.sequence.set_eleEntries(para['ele'])
        self.v_rotation.set(para['v_rotation'])
        self.pie_size.set(para['pie_size'])
        self.pieEdge_color.set(para['pieEdge_color'])
        self.pie_linewidth.set(para['pie_linewidth'])
        self.pie_alp.set(para['pie_alp'])
        self.legendFont.set(para['legendFont'])
        self.legendColor.set(para['legendColor'])
        self.legendFontStyle.current(para['legendFontStyle'])
        self.legendFontWeight.current(para['legendFontWeight'])
        self.patch_fill.set(para['patch_fill'])
        self.patchFaceColor.set(para['patchFaceColor'])
        self.patchEdgeColor.set(para['patchEdgeColor'])
        self.patchLineWidth.set(para['patchLineWidth'])
        self.patchRadius.set(para['patchRadius'])
        self.patchAlpha.set(para['patchAlpha'])

        self.colorlist=para['legendB_C']

        self._on_set_piechart()
        self.on_pieEdge_color(color =self.pieEdge_color.get())
        self.on_legend_check()
        self.on_waferCircle_check()
        self.on_tarpos()
        self.on_set_legend()
        self.on_legendColor(color =self.legendColor.get())
        self.on_patchFaceColor(color =self.patchFaceColor.get())
        self.on_patchEdgeColor(color =self.patchEdgeColor.get())
        self.on_set_patch()

        for ele, color in para['legendB_C'].items():
            self.plot_leg.get_B().get(ele).config(bg = color)
            self.tar_pos.update_color(ele, color)
        self.on_position_check()
        self.on_update_pie()

def main():

    root = Tk()
    data = pd.read_csv('aa.csv')
    app = Pie_slice_setting(root, data)
    app.pack()


    root.mainloop()

if __name__ == '__main__':
    main()
