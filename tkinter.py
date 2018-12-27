from Tkinter import *
from registerDB import *
import tkMessageBox

import RPi.GPIO as GPIO
import MFRC522
import signal
import os

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

GPIO.setwarnings(False)

continue_reading = True

# ************************************************
# ********** GRAPH *******************************
LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
p = f.add_subplot(111)
b = f.add_subplot(111)


def animate(i):

    if cardVar.get() != "" :
        # ****************************************************
        # ********** B O T T L E *****************************
        bottleData = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ rfidVar.get() +'/bottle.txt',"r").read()
        dataList = bottleData.split('\n')
        bdayList = []        # Number of Days
        bottleList = []      # Number of Papers
        for eachLine in dataList:
            if len(eachLine) > 1:
                x, y = eachLine.split(',')
                bdayList.append(int(x))
                s = bottleList.append(int(y))

        # ****************************************************
        # ********** P A P E R *******************************
        paperData = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ rfidVar.get() +'/paper.txt',"r").read()
        dataList = paperData.split('\n')
        pdayList = []        # Number of Days
        paperList = []      # Number of Papers
        for eachLine in dataList:
            if len(eachLine) > 1:
                x, y = eachLine.split(',')
                pdayList.append(int(x))
                paperList.append(int(y))

        #plt.xlabel('x')
        #plt.ylabel('y')

        p.clear()
        b.clear()
        p.plot(pdayList, paperList, color = 'b',)
        b.plot(bdayList, bottleList, color = 'r')
        p.plot()
        b.plot()
# ************************************************

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = Font = ('Helvetica', 18, "bold", "italic")

        # *******************************************
        # ******* GUI BG ****************************
        self.Bg = PhotoImage(file = "Image/Main.gif")
        self.BgReg = PhotoImage(file = "Image/ButtonRegister.gif")
        
        self.BgChoose = PhotoImage(file = "Image/Choose.gif")
        self.BgCreateAccount = PhotoImage(file = "Image/CreateAccount.gif")
        
        # ********************************************
        # ******* MEMBER *****************************
        self.BgMemberLogin = PhotoImage(file = "Image/LoginMember.gif")
        self.BgMemberData = PhotoImage(file = "Image/MemberData.gif")

        self.BgMemberContinue = PhotoImage(file = "Image/LoginContinue.gif")
        self.BgLogin = PhotoImage(file = "Image/ButtonLogin.gif")
        # ********************************************
        # ******* GUEST ******************************
        self.BgGuest = PhotoImage(file = "Image/ButtonGuest.gif")
        self.BgGuestData = PhotoImage(file = "Image/guestData.gif")
        
        self.BgEnterNumber = PhotoImage(file = "Image/EnterNumber.gif")
        self.BgContinue = PhotoImage(file = "Image/ButtonContinue.gif")
        self.BgOK = PhotoImage(file = "Image/ButtonOK.gif")
        

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Choose, CreateAccount, Guest, Guestdata, MemberLogin, MemberData):      # FRAME *************
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        #self.show_frame("MemberData")
        

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, image = controller.Bg)
        label.pack()

        btnContinue = Button(self, image = controller.BgContinue, border = 0,
                            command=lambda: controller.show_frame("Choose"))

        btnContinue.place(x = 760, y = 500)


class Choose(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def MemberLog () :
            tapCardVar.set("")
            controller.show_frame("MemberLogin")
        
        label = Label(self, image = controller.BgChoose)
        label.pack()
        
        btnGuest = Button(self, image = controller.BgGuest, border = 0,
                           command=lambda: controller.show_frame("Guest"))
        btnGuest.place(x = 233, y = 120)

        btnLogin = Button(self, image = controller.BgLogin, border = 0,
                           command = MemberLog)
        btnLogin.place(x = 1109, y = 120)

        btnReg = Button(self, image = controller.BgReg, border = 0,
                           command=lambda: controller.show_frame("CreateAccount"))
        btnReg.place(x = 675, y = 520)

class CreateAccount(Frame):

    def __init__(self, parent, controller):
        global rfidVar,nameVar,phonenumVar,eaddVar
        Frame.__init__(self, parent)
        self.controller = controller

        def btnRegister () :
            addEntry()
            if flag == 1 :
                controller.show_frame("Choose")
                
        
        label = Label(self, image = controller.BgCreateAccount)
        label.pack()

        rfidVar = StringVar()
        txtRfid = Entry(self, text = rfidVar, font = ('Helvetica', 30), justify = "center", state = "readonly")
        txtRfid.place(x = 915, y = 290, width = 768, height = 67)

        nameVar = StringVar()
        txtName = Entry(self, text = nameVar, font = ('Helvetica', 30), justify = "center")
        txtName.place(x = 915, y = 408, width = 768, height = 67)

        phonenumVar = StringVar()
        txtPhoneNum = Entry(self, text = phonenumVar, font = ('Helvetica', 30), justify = "center")
        txtPhoneNum.place(x = 915, y = 529, width = 768, height = 67)

        eaddVar = StringVar()
        txteadd = Entry(self, text = eaddVar, font = ('Helvetica', 30), justify = "center")
        txteadd.place(x = 915, y = 652, width = 768, height = 67)

        btn = Button(self, image = controller.BgOK, command = btnRegister)
        btn.place(x = 768, y = 790)

        saveContact()

class Guest(Frame):

    def __init__(self, parent, controller):
        global EnterNumVar
        Frame.__init__(self, parent)
        self.controller = controller

        def ContinueFunc () :
            global guestNumberVar

            numbers = EnterNumVar.get()
            guestNumberVar.set(str(numbers))
            controller.show_frame("Guestdata")
            
        label = Label(self, image = controller.BgEnterNumber)
        label.pack()

        EnterNumVar = StringVar()
        txtEnterNum = Entry(self, text = EnterNumVar, font = ('Helvetica', 30), justify = "center")
        txtEnterNum.place(x = 260, y = 378, width = 1307, height = 75)

        btnContinue = Button(self, image = controller.BgContinue, command=ContinueFunc)
        btnContinue.place(x = 0, y = 0)

        

class Guestdata(Frame):

    def __init__(self, parent, controller):
        global guestNumberVar
        
        print EnterNumVar.get()
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, image = controller.BgGuestData)
        label.pack()

        # *************************************************************************
        # ************* TK CANVAS FOR PLOT ****************************************

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(x = 0 , y = 0, width = 0 , height = 0)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.place(x = 815, y = 85, width = 803, height = 369)

        # **************************************************************************
        

        guestNumberVar = StringVar()
        guestNumber = Entry(self, text = guestNumberVar, font = ('Helvetica', 30), justify = "center", state = "readonly")
        guestNumber.place(x = 46, y = 117, width = 433, height = 44)

    
class MemberLogin(Frame):

    def __init__(self, parent, controller):
        global tapCardVar
        
        Frame.__init__(self, parent)
        self.controller = controller

        def Continue () :
            Com = 0
            print tapCardVar.get()
            if tapCardVar.get() == "" :
                tkMessageBox.showinfo("","Tap Card First")
            else :
                for item in range(0, len(Register)) :
                    if Register[item][0] == tapCardVar.get() :
                        Com = 1
                        Num = item
                        break

                if Com == 1 :
                    tkMessageBox.showinfo("","Login Successfull")
                    cardVar.set(str(Register[Num][0]))
                    memberNameVar.set(str(Register[Num][1]))
                    mobileNumVar.set(str(Register[Num][2]))
                    eAddVar.set(str(Register[Num][3]))
                    #totalVar
                    controller.show_frame("MemberData")
                else :
                    tkMessageBox.showinfo("","Invalid Card or Not Registered")
                        
        
        label = Label(self, image = controller.BgMemberLogin)
        label.pack()

        tapCardVar = StringVar()
        tapCard = Entry(self, text = tapCardVar, font = ('Helvetica', 30), justify = "center", state = "readonly")
        tapCard.place(x = 386, y = 367, width = 1039, height = 97)

        btnContinue = Button (self, image = controller.BgMemberContinue, command = Continue)
        btnContinue.place(x = 711, y = 553)

class MemberData(Frame):

    def __init__(self, parent, controller):
        global cardVar, memberNameVar, mobileNumVar, eAddVar, totalVar
        
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, image = controller.BgMemberData)
        label.pack()

        # *************************************************************************
        # ************* TK CANVAS FOR PLOT ****************************************

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(x = 0 , y = 0, width = 0 , height = 0)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.place(x = 815, y = 85, width = 803, height = 369)

        # **************************************************************************

        cardVar = StringVar()
        card = Entry(self, text = cardVar, font = ('Helvetica', 15), justify = "center", state = "readonly")
        card.place(x = 315, y = 151, width = 319, height = 40)

        memberNameVar = StringVar()
        memberName = Entry(self, text = memberNameVar, font = ('Helvetica', 15), justify = "center", state = "readonly")
        memberName.place(x = 315, y = 215, width = 319, height = 40)

        mobileNumVar = StringVar()
        mobileNum = Entry(self, text = mobileNumVar, font = ('Helvetica', 15), justify = "center", state = "readonly")
        mobileNum.place(x = 315, y = 280, width = 319, height = 40)

        eAddVar = StringVar()
        eAdd = Entry(self, text = eAddVar, font = ('Helvetica', 15), justify = "center", state = "readonly")
        eAdd.place(x = 315, y = 347, width = 319, height = 40)

        totalVar = StringVar()
        total = Entry(self, text = totalVar, font = ('Helvetica', 15), justify = "center", state = "readonly")
        total.place(x = 315, y = 411, width = 319, height = 40)

# ***********************************************************************************
# ******************** FUNCTION *****************************************************
            
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def readCard () :
    global rfidVar
    signal.signal(signal.SIGINT, end_read)

    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print "Card detected"
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:

        print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])

        cardNumber = str(uid[0]) +"-"+ str(uid[1]) +"-"+ str(uid[2]) +"-"+ str(uid[3])

        rfidVar.set(str(cardNumber))
        tapCardVar.set(str(cardNumber))
        
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        MIFAREReader.MFRC522_SelectTag(uid)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"
    app.after(500, readCard)

def addEntry () :
    global rfidVar, nameVar, phonenumVar, eaddVar, flag
    Com = 0
    flag = 0
    for item in range(0, len(Register)) :
        if Register[item][0] == rfidVar.get() :
            Com = 1
            tkMessageBox.showinfo("","Card Number already Registered !\n  Please Tap another Card")
            break
                        
    if Com == 0 :
        if rfidVar.get() == "" :
            tkMessageBox.showwarning("","Tap Card First !")
        elif nameVar.get() =="" or phonenumVar.get() == "" or eaddVar.get() == "" :
            tkMessageBox.showinfo("","Fill up all information !")
        else :
            Register.append ([rfidVar.get(), nameVar.get(), phonenumVar.get(), eaddVar.get()])  
            setSelect ()
            saveContact()
            tkMessageBox.showinfo("","Registration Successfull")

            # *********************************************************
            # ***** MAKE FILE FOR JUAN EARTH **************************
            os.makedirs('/home/pi/Desktop/sourceCode/EarthJuan/'+rfidVar.get())
            
            paper = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ rfidVar.get() +'/paper.txt','w')
            paper.write('0,0')
            paper.write('\n')
            paper.close()

            bottle = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ rfidVar.get() +'/bottle.txt','w')
            bottle.write('0,0')
            bottle.write('\n')
            bottle.close()

            rfidVar.set("")
            nameVar.set("")
            phonenumVar.set("")
            eaddVar.set("")
            flag = 1
            

def saveContact () :
    print "test"
    global rfid, name, phonenum, eadd
                    
    f = open("registerDB.py", "w")
    f.write("Register = [")
    for rfid, name, phonenum, eadd in Register:
        f.write(" ".join(["['%s','%s','%s','%s'],"%(rfid, name, phonenum, eadd)]))
    f.write("]")
    f.close()

def setSelect () :
    Register.sort()

if __name__ == "__main__":
    app = SampleApp()
    ani = animation.FuncAnimation(f, animate, interval=500)
    readCard()
    setSelect()
    app.mainloop()
