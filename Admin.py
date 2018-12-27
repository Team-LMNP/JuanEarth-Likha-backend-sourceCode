from Tkinter import *
import tkMessageBox
from registerDB import *
import shutil
import os

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = Font = ('Helvetica', 18, "bold", "italic")
        self.BlankBg = PhotoImage(file = "Image/AdminMain.gif")
        self.AdminBg = PhotoImage(file = "Image/Admin.gif")
        self.Button = PhotoImage(file = "Image/ButtonAdminLogin.gif")
        self.DataPath = '/home/pi/Desktop/sourceCode/Evaluation/'
        self.Datas = '/home/pi/Desktop/sourceCode/EarthJuan/'
        self.BgReset = PhotoImage(file = "Image/ButtonAdminReset.gif")

        # *******************************************
        # ********** PATH ***************************
        self.databasePath = "/home/pi/Desktop/sourceCode/registerDB.py"
        self.evaPath = "/home/pi/Desktop/sourceCode/Evaluation/"
        # *******************************************

        self.canCtr = 0
        self.bottleCtr = 0
        self.canVar = StringVar ()
        self.bottleVar = StringVar()

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Main):      # FRAME *************
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")
        
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Login(Frame):

    def __init__(self, parent, controller):
        global passwordVar, idVar
        Frame.__init__(self, parent)
        self.controller = controller

        def btnFunc () :
            total = 0
            if idVar.get() == "" or passwordVar.get() == "" :
                tkMessageBox.showinfo("","Please, Input Id and Password !")
            elif idVar.get() != "Admin" or passwordVar.get() != "Admin" :
                tkMessageBox.showinfo("","Invalid Id or Passwword !")
            else :
                for item in range(0, len(Register)) :
                    #print Register[item][0]
                    data = open(controller.Datas + str(Register[item][0]) + '/bottle.txt', 'r').read()
                    dataList = data.split('\n')
                    for eachLine in dataList:
                        if len(eachLine) > 1:
                            x, y = eachLine.split(',')
                            #print int(y)
                            controller.bottleCtr = controller.bottleCtr + int(y)
                            print controller.bottleCtr

                    data = open(controller.Datas + str(Register[item][0]) + '/can.txt', 'r').read()
                    dataList = data.split('\n')
                    for eachLine in dataList:
                        if len(eachLine) > 1:
                            x, y = eachLine.split(',')
                            #print int(y)
                            controller.canCtr = controller.canCtr + int(y)
                            print controller.canCtr
                controller.bottleVar.set(str(controller.bottleCtr))
                controller.canVar.set(str(controller.canCtr))
                controller.show_frame("Main")

        label = Label(self, image = controller.AdminBg)
        label.pack()

        idVar = StringVar ()
        id = Entry(self, text = idVar, font = ("Helvetica", 35), justify = "center")
        id.place(x = 677 , y = 273, width = 743, height = 100)

        passwordVar = StringVar ()
        password = Entry(self, text = passwordVar, font = ("Helvetica", 35), justify = "center", show = "*")
        password.place(x = 677 , y = 426, width = 743, height = 100)
        
        btnContinue = Button(self, image = controller.Button, border = 0,
                            command = btnFunc)

        btnContinue.place(x = 760, y = 600)


class Main(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def Reset () :
            result = tkMessageBox.askquestion("Reset", "Are you sure you want to RESET all data ?", icon = "warning")
            if result == "no" :
                print "NO"
            else :
                Database = open (controller.databasePath,'w')
                Database.write("Register = []")
                Database.close()
                try :
                    shutil.rmtree('EarthJuan')
                except :
                    pass
                os.makedirs('EarthJuan')

                try :
                    shutil.rmtree('GuestEarthJuan')
                except :
                    pass
                os.makedirs('GuestEarthJuan')

                eva1 = open (controller.evaPath+'1.txt','w')
                eva1.write('0')
                eva1.close()

                eva2 = open (controller.evaPath+'2.txt','w')
                eva2.write('0')
                eva2.close()

                eva3 = open (controller.evaPath+'3.txt','w')
                eva3.write('0')
                eva3.close()

                tkMessageBox.showinfo("","Reset Successfully !!")

            

        label = Label(self, image = controller.BlankBg)
        label.pack() 

        ## ***********************************************************************************
        ## ********  B A R - G R A P H  ******************************************************
        f = Figure(figsize=(5,4), dpi=100)
        ax = f.add_subplot(111)

        data1 = open(controller.DataPath + '1.txt','r')
        x = data1.readlines()
        for a in x :
            print a

        data2 = open(controller.DataPath + '2.txt','r')
        y = data2.readlines()
        for b in y :
            print b

        data3 = open(controller.DataPath + '3.txt','r')
        z = data3.readlines()
        for c in z :
            print c
            
        data = (int(a))
        data2 = (int(b))
        data3 = (int(c))

        position = [1]
        position2 = [2]
        position3 = [3]
        width = .5

        rects1 = ax.bar(position, data, width)
        rects2 = ax.bar(position2, data2, width)
        rects3 = ax.bar(position3, data3, width)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(x = 0 , y = 0, width = 0 , height = 0)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.place(x = 800, y = 500, width = 803, height = 369)

        ## *********** E N D  OF  B A R - G R A P H *****************************************

        can = Entry(self, text = controller.canVar, font = ("Helvetica", 50), justify = "right")
        can.place (x = 71, y = 250, width = 217, height = 117)

        bottle = Entry(self, text = controller.bottleVar, font = ("Helvetica", 50), justify = "right")
        bottle.place (x = 296, y = 250, width = 225, height = 117)

        btnReset = Button(self, image = controller.BgReset, command = Reset)
        btnReset.place(x = 150, y = 650)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
