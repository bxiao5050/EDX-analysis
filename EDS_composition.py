from tkinter import *
from tkinter import ttk
from datetime import *

from version_random.textbox import TextBox
from version_Wafer.EDS_main import EDS_Main
from menu.sort_EDS import Sort_EDS

def func():
    print('sdfsf')

class EDX_composition(Frame):

    def __init__(self, master):
        super().__init__(master)

        # filemenu.add_command(label="Exit", command=root.quit)


        notebook = ttk.Notebook(master)
        EDS_wafer = EDS_Main(master)
        notebook.add(EDS_wafer,text='Whole wafer')
        notebook.pack()

        EDS_fromText = TextBox(master)
        notebook.add(EDS_fromText,text='from text')
        notebook.pack()


    def add_tab(self,title, f):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame,text=title)
        self.notebook.pack()




def main():
    root = Tk()
    root.title('.EDS composition')
    app = EDX_composition(root)
    app.pack(fill = 'both',expand = True)



    with open('qixian') as fp:
        lines = fp.readlines()
        for line in lines:
            if 'qixian' in line:
                return


    with open('qixian', 'r+') as fp:
        lines = fp.readlines()
        for line in lines:
            if '..' in line:
                # print(line.strip())
                if datetime.today().date()> datetime.strptime(line.strip().replace('..',''), '%y.%m.%d').date():
                    fp.write('qixian')
                    return


    # menu = Menu(root)
    # root.config(menu=menu)
    # filemenu = Menu(menu)
    # menu.add_cascade(label="File", menu=filemenu)
    # filemenu.add_command(label = 'get formatted files', command = on_convert)

    # filemenu.add_separator()

    root.mainloop()

def on_convert():
    w = Toplevel()
    Sort_EDS(w)



if __name__=='__main__':
    main()
