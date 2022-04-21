from tkinter import*
from tkinter import ttk, colorchooser
from tkinter import font
import tkinter as tk
from matplotlib.figure import Figure

class Myfont():
    def __init__(self, master, canvas, text = 'xxxx', x=100, y=50):
        self.canvas = canvas
        self.rect_item = None

    # def new_text(self, text):
        self.fontf_var = StringVar()
        self.fontf_var.set('Times New Roman')
        self.fontw_var = StringVar()
        self.fontw_var.set('normal')
        self.fonts_var = IntVar()
        self.fonts_var.set(12)
        self.fontc_var = StringVar()
        self.fontc_var.set('black')
        self.fonta_var = IntVar()
        self.fonta_var.set(0)
        self.font_var = StringVar()
        self.font_var.set('dsdsds')

        # self.font_var.set(slabel.itemcget(self.obj, 'text'))
        self.label = Label(canvas, textvariable = self.font_var, bg = 'white', font = ('Times New Roman', 12, 'normal'))
        self.obj = self.canvas.create_window(x, y, window = self.label)

        self.canvas.update()
        #movement
        self.label.bind('<B1-Motion>', self.mov)
        self.fontgui = FontGUI(master, canvas, self)


    def get_para(self):
        para = {}
        para['fontf_var'] = self.fontf_var.get()
        para['fontw_var'] = self.fontw_var.get()
        para['fonts_var'] = self.fonts_var.get()
        para['fontc_var'] = self.fontc_var.get()
        para['fonta_var'] = self.fonta_var.get()
        para['font_var'] = self.font_var.get()
        return para

    def loseFocus(self, e):
        if self.rect_item is not None:
            self.canvas.delete(self.rect_item)
        self.canvas.update()


    def drag_start(self, event):
        widget = event.widget
        widget.startX = event.x
        widget.startY = event.y

    def mov(self, event):
        # self.highlight()
        widget = event.widget
        x = widget.winfo_x() - widget.startX + event.x
        y = widget.winfo_y() - widget.startY + event.y
        widget.place(x=x,y=y)
        self.canvas.update()

    def mouse_release(self, event):
        self.highlight()

    def highlight(self, e=''):
        if self.rect_item is not None:
            self.canvas.delete(self.rect_item)
        bbox = self.canvas.bbox(self.obj)
        self.rect_item = self.canvas.create_rectangle(bbox, outline="red2", fill="")
        self.canvas.tag_raise(self.obj,self.rect_item)
        self.canvas.update()



class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 30
        y = y + self.widget.winfo_rooty() -30
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

class FontGUI(Frame):
    def __init__(self, master, canvas, myfont):
        super().__init__(master)
        self.canvas = canvas
        self.obj = myfont.obj
        self.label = myfont.label
        self.myfont = myfont


        #mainGUI
        tool_f = LabelFrame(self, text = 'set font')
        tool_f.pack()
        #fontfamily
        self.fontf_var = StringVar()
        self.fontf_var.set('Times New Roman')
        fontf = ttk.Combobox(tool_f , textvariable = self.fontf_var, values = font.families(), state = 'readonly')
        fontf.bind('<<ComboboxSelected>>', self.on_font)
        #fontweight
        self.fontw_var = StringVar()
        self.fontw_var.set('normal')
        fontw = ttk.Combobox(tool_f , width = 7, textvariable = self.fontw_var, values = ['normal', 'bold', 'italic'], state = 'readonly')
        fontw.bind('<<ComboboxSelected>>', self.on_font)
        #fontsize
        self.fonts_var = IntVar()
        self.fonts_var.set(12)
        fonts = Scale(tool_f, from_ = 5, to=100, resolution = 1,  width = 8,orient = 'horizontal', variable = self.fonts_var, command = self.on_font)
        #fontcolor
        self.fontc_var = StringVar()
        self.fontc_var.set('black')
        self.fontc = Button(tool_f, text = '     ', relief = 'flat', bg = self.fontc_var.get(), command = self.on_font_color)
        #fontangle
        self.fonta_var = IntVar()
        self.fonta_var.set(0)
        fonta = Scale(tool_f, from_ = 0, to=360, resolution = 1, width = 8, orient = 'horizontal', variable = self.fonta_var, command = self.on_font)
        #font content
        self.font_var = StringVar()
        # self.font_var.set(self.canvas.itemcget(self.obj, 'text'))
        font_e = Entry(tool_f,width = 50, textvariable = self.font_var, relief = 'flat')
        font_e.bind('<FocusOut>',  self.on_update_text)
        font_e.bind('<Return>',   self.on_update_text)

        fontf.grid(row =0,column=0, padx = (5,5), pady = (5,5))
        fontw.grid(row =0,column=1, padx = (5,5), pady = (5,5))
        fonts.grid(row =0,column=2, padx = (5,5), pady = (5,5))
        self.fontc.grid(row =0,column=3, padx = (5,5), pady = (5,5))
        fonta.grid(row =0,column=4, padx = (5,5), pady = (5,5))
        font_e.grid(row =0,column=5, columnspan = 5, padx = (5,5), pady = (5,5))

        CreateToolTip(fontf, 'pick a new font for the text')
        CreateToolTip(fontw, 'bold or italic')
        CreateToolTip(fonts, 'font size')
        CreateToolTip(self.fontc, 'font color')
        CreateToolTip(fonta, 'rotete the text')

        para = myfont.get_para()
        self.set_para(para)


    def on_update_text(self, e):
        text = self.font_var.get()
        self.myfont.font_var.set(text)
        self.canvas.update()



    def on_font_color(self):
        color_code = colorchooser.askcolor(title ="Choose color")[1]
        self.fontc_var.set(color_code)
        self.fontc.config(bg = self.fontc_var.get())
        self.on_font()

    def on_font(self, e=''):
        self.set_font(deg= self.fonta_var.get(), fontsize = self.fonts_var.get(), fontcolor = self.fontc_var.get(), fontfamily = self.fontf_var.get(), fontweight = self.fontw_var.get())

    def set_font(self, deg, fontsize, fontcolor, fontfamily, fontweight):
        self.label.config( font = (fontfamily, fontsize, fontweight))
        # self.canvas.itemconfigure(self.obj, angle = deg)
        self.label.config( fg = fontcolor)

    def set_para(self, para):
        self.fontf_var.set(para['fontf_var'])
        self.fontw_var.set(para['fontw_var'])
        self.fonts_var.set(para['fonts_var'])
        self.fontc_var.set(para['fontc_var'])
        self.fonta_var.set(para['fonta_var'])
        self.font_var.set(para['font_var'])


class FontPanel(Frame):
    def __init__(self, master,canvas):
        super().__init__(master)
        self.canvas = canvas

        self.myfonts = []
        self.num = 0
        self.canvas.bind("<Button-1>", self.on_canvas)

    def on_canvas(self, e):
        for font in self.myfonts:
            font.fontgui.pack_forget()
            font.label.config(relief = 'flat')



    def on_add(self):
        font = Myfont(self, self.canvas, x= 500+self.num*20, y = 20+self.num*10)
        self.myfonts.append(font)
        self.num+=1

        font.label.bind("<Button-1>", lambda e, obj = font:self.on_click(e, obj))
        return font

    def on_click(self,event, obj):
        for font in self.myfonts:
            font.fontgui.pack_forget()
            font.label.config(relief = 'flat')

        obj.label.config(relief = 'solid')
        obj.fontgui.pack(side = 'bottom')
        obj.drag_start(event)







def main():
    root = Tk()
    root.geometry('1000x600+500+100')
    canvas=Canvas(root,width=200,height=300)


    canvas.pack(fill=BOTH, expand=1)

    fontPanel = FontPanel(root, canvas)
    fontPanel.pack()


    b = Button(canvas, text = 'add', bg = 'white', relief = 'flat')
    b.config(command =  fontPanel.on_add)
    b.pack()




    root.mainloop()


if __name__ == '__main__':
    main()








