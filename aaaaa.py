from Tkinter import *
from registerDB import *
import tkMessageBox

import RPi.GPIO as GPIO
import MFRC522
import signal
import os
import time

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


scanFlag = 0;
mode = 0

polPin = 36
detPin = 38
resetPin = 40

TRIG = 35 
ECHO = 37

TRIG2 = 33 
ECHO2 = 31

servo1 = 11
servo2 = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(polPin, GPIO.IN)         ## POL PIN METAL DETECTOR
GPIO.setup(detPin, GPIO.IN)         ## DET PIN METAL DETECTOR
GPIO.setup(resetPin, GPIO.OUT), GPIO.output(resetPin, GPIO.HIGH)

GPIO.setup(TRIG,GPIO.OUT)               ## ULTRASONIC 1 TRIGGER
GPIO.setup(ECHO,GPIO.IN)                ## ULTRASONIC 1 ECHO

GPIO.setup(TRIG2,GPIO.OUT)          ## ULTRASONIC 2 TRIGGER
GPIO.setup(ECHO2,GPIO.IN)           ## ULTRASONIC 2 ECHO

GPIO.setup(servo1, GPIO.OUT)            ## servo 1
pwm1=GPIO.PWM(servo1, 50)  
pwm1.start(0)

GPIO.setup(servo2, GPIO.OUT)             ## servo 2
pwm2=GPIO.PWM(servo2, 50)            
pwm2.start(0)


time.sleep(1)
GPIO.output(resetPin, GPIO.HIGH)      # Reset No Detect
GPIO.output(resetPin, GPIO.LOW)       # Reset No Detect
time.sleep(1)

def servo1Angle(angle1):
     duty = angle1 / 18 + 2
     GPIO.output(servo1, True)
     pwm1.ChangeDutyCycle(duty)
     time.sleep(1)
     GPIO.output(servo1, False)
     pwm1.ChangeDutyCycle(0)

def servo2Angle(angle2):
     duty = angle2 / 18 + 2
     GPIO.output(servo2, True)
     pwm2.ChangeDutyCycle(duty)
     time.sleep(1)
     GPIO.output(servo2, False)
     pwm2.ChangeDutyCycle(0)

# ************************************************
# ********** GRAPH *******************************
LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
p = f.add_subplot(111)
b = f.add_subplot(111)


def animate(i):
    totalBottle = 0;
    totalCan = 0;
    global mode
    if mode == 2 :
        #print "Member"
        # ****************************************************
        # ********** B O T T L E *****************************
        try :
             bottleData = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ cardVar.get() +'/bottle.txt',"r").read()
             dataList = bottleData.split('\n')
             bdayList = []        # Number of Days
             bottleList = []      # Number of Papers
             for eachLine in dataList:
                 if len(eachLine) > 1:
                     x, y = eachLine.split(',')
                     bdayList.append(int(x))
                     bottleList.append(int(y))
                     totalBottle = totalBottle + int(y)
             #print totalBottle
        except :
             pass
                

        # ****************************************************
        # ********** P A P E R *******************************
        try :
             paperData = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ cardVar.get() +'/can.txt',"r").read()
             dataList = paperData.split('\n')
             pdayList = []        # Number of Days
             paperList = []      # Number of Papers
             for eachLine in dataList:
                 if len(eachLine) > 1:
                     x, y = eachLine.split(',')
                     pdayList.append(int(x))
                     paperList.append(int(y))
                     totalCan = totalCan + int(y)
             #print totalCan
        except :
             pass
        try :
             totalBottle = totalBottle * 1
             totalCan = totalCan * 1.5
             overallTotal = totalBottle + totalCan

             #print float(overallTotal)
             totalVar.set(float(overallTotal))
             p.clear()
             b.clear()
             p.plot(pdayList, paperList, color = 'b',)
             b.plot(bdayList, bottleList, color = 'r')
             p.plot()
             b.plot()
        except :
             pass
    elif mode == 1:
        print "guest"
        # ****************************************************
        # ********** B O T T L E *****************************
        try :
             bottleData = open('/home/pi/Desktop/sourceCode/GuestEarthJuan/'+ cardVar.get() +'/bottle.txt',"r").read()
             dataList = bottleData.split('\n')
             bdayList = []        # Number of Days
             bottleList = []      # Number of Papers
             for eachLine in dataList:
                 #print "Data"
                 if len(eachLine) > 1:
                     x, y = eachLine.split(',')
                     bdayList.append(int(x))
                     bottleList.append(int(y))
                     totalBottle = totalBottle + int(y)

             # ****************************************************
             # ********** P A P E R *******************************
             paperData = open('/home/pi/Desktop/sourceCode/GuestEarthJuan/'+ cardVar.get() +'/can.txt',"r").read()
             dataList = paperData.split('\n')
             pdayList = []        # Number of Days
             paperList = []      # Number of Papers
             for eachLine in dataList:
                 if len(eachLine) > 1:
                     x, y = eachLine.split(',')
                     pdayList.append(int(x))
                     paperList.append(int(y))
                     totalCan = totalCan + int(y)

             totalBottle = totalBottle * 1
             totalCan = totalCan * 1.5
             overallTotal = totalBottle + totalCan

             totalVar.set(float(overallTotal))
             p.clear()
             b.clear()
             p.plot(pdayList, paperList, color = 'b',)
             b.plot(bdayList, bottleList, color = 'r')
             p.plot()
             b.plot()
        except :
             pass
# *****************************************************************************************************8
# ***********************************************************************************
# ***********************************************************************************
# ************************************************************************************
# ********************************************************************************************

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = Font = ('Helvetica', 18, "bold", "italic")
        self.bottleCount = 0;
        self.canCount = 0;

        self.eva1 = 'Evaluation/1.txt'
        self.eva2 = 'Evaluation/2.txt'
        self.eva3 = 'Evaluation/3.txt'

        self.MemberPath = '/home/pi/Desktop/sourceCode/EarthJuan/'
        self.GuestPath = '/home/pi/Desktop/sourceCode/GuestEarthJuan/'
        
        # *******************************************
        # ******* GUI BG ****************************
        self.Bg = PhotoImage(file = "Image/Main.gif")
        self.BgReg = PhotoImage(file = "Image/ButtonRegister.gif")
        self.BlankBg = PhotoImage(file = "Image/Back.gif")
        self.BgMotherEarth = PhotoImage(file = "Image/motherEarth.gif")
        self.BgRedeem = PhotoImage(file = "Image/redeemPoints.gif")
        self.BgGuestRedeem = PhotoImage(file = "Image/guestFinal.gif")
        self.BgExperience = PhotoImage(file = "Image/trashBin.gif")
        
        self.BgChoose = PhotoImage(file = "Image/Choose.gif")
        self.BgCreateAccount = PhotoImage(file = "Image/CreateAccount.gif")
        self.BgHome = PhotoImage(file = "Image/ButtonHome.gif")
        self.Bg1 = PhotoImage(file = "Image/1.gif")
        self.Bg2 = PhotoImage(file = "Image/2.gif")
        self.Bg3 = PhotoImage(file = "Image/3.gif")
        
        # ********************************************
        # ******* MEMBER *****************************
        self.BgMemberLogin = PhotoImage(file = "Image/LoginMember.gif")
        self.BgMemberData = PhotoImage(file = "Image/MemberData.gif")
        self.BgMemberAddTrash = PhotoImage(file = "Image/Scan.gif")
        self.BgWrongItem = PhotoImage(file = "Image/Wrong.gif")

        self.BgMemberContinue = PhotoImage(file = "Image/LoginContinue.gif")
        self.BgLogin = PhotoImage(file = "Image/ButtonLogin.gif")
        self.BgAddTrash = PhotoImage(file = "Image/ButtonMemberAddTrash.gif")
        self.BgBackHome = PhotoImage(file = "Image/ButtonMemberBackHome.gif")
        self.BgScan = PhotoImage(file = "Image/ButtonScan.gif")
        self.BgDone = PhotoImage(file = "Image/ButtonAreYouDone.gif")
        self.BgMore = PhotoImage(file = "Image/ButtonAddMore.gif")
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
        for F in (StartPage, Choose, CreateAccount, Guest, MemberLogin, MemAddtrash, MemberData, MemberDoneMore, MotherEarth, Redeem, GuestRedeem, Experience):      # FRAME *************
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        
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
        btnGuest.place(x = 50, y = 281)

        btnLogin = Button(self, image = controller.BgLogin, border = 0,
                           command = MemberLog)
        btnLogin.place(x = 1208, y = 281)

        btnReg = Button(self, image = controller.BgReg, border = 0,
                           command=lambda: controller.show_frame("CreateAccount"))
        btnReg.place(x = 629, y = 281)

class CreateAccount(Frame):

    def __init__(self, parent, controller):
        global rfidVar,nameVar,phonenumVar,eaddVar
        Frame.__init__(self, parent)
        self.controller = controller

        def btnRegister () :
            addEntry()
            if flag == 1 :
                controller.show_frame("Choose")

        def Home () :
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
        btn.place(x = 1000, y = 790)

        btnHome = Button(self, image = controller.BgHome, command = Home)
        btnHome.place(x = 500, y = 790)

        saveContact()

class Guest(Frame):

    def __init__(self, parent, controller):
        global cardVar, memberNameVar, mobileNumVar, eAddVar, totalVar, EnterNumVar
        Frame.__init__(self, parent)
        self.controller = controller

        def ContinueFunc () :
            global mode

            if EnterNumVar.get() == "" :
                tkMessageBox.showinfo("","Please, Input Your Number.")
            else :
                try : 
                    os.makedirs('/home/pi/Desktop/sourceCode/GuestEarthJuan/'+EnterNumVar.get())
                
                    guestCan = open('/home/pi/Desktop/sourceCode/GuestEarthJuan/'+ EnterNumVar.get() +'/can.txt','w')
                    guestCan.write('0,0')
                    guestCan.write('\n')
                    guestCan.close()

                    cancounter = open('/home/pi/Desktop/sourceCode/GuestEarthJuan/'+ EnterNumVar.get() +'/cancounter.txt','w')
                    cancounter.write('0')
                    cancounter.write('\n')
                    cancounter.close()

                    guestBottle = open('/home/pi/Desktop/sourceCode/GuestEarthJuan/'+ EnterNumVar.get() +'/bottle.txt','w')
                    guestBottle.write('0,0')
                    guestBottle.write('\n')
                    guestBottle.close()

                    bottlecounter = open('/home/pi/Desktop/sourceCode/GuestEarthJuan/'+ EnterNumVar.get() +'/bottlecounter.txt','w')
                    bottlecounter.write('0')
                    bottlecounter.write('\n')
                    bottlecounter.close()
                except :
                    print "PASS"
                    pass
                
                mode = 1                # GUEST MODE
                numbers = EnterNumVar.get()
                cardVar.set(str(numbers))
                memberNameVar.set("Guest")
                mobileNumVar.set("Guest")
                eAddVar.set("Guest")
                controller.show_frame("MemberData")

        def Home () :
            mode = 0
            EnterNumVar.set("")
            cardVar.set("")
            memberNameVar.set("")
            mobileNumVar.set("")
            eAddVar.set("")
            totalVar.set("")
            controller.show_frame("Choose")
            
        label = Label(self, image = controller.BgEnterNumber)
        label.pack()

        EnterNumVar = StringVar()
        txtEnterNum = Entry(self, text = EnterNumVar, font = ('Helvetica', 30), justify = "center")
        txtEnterNum.place(x = 260, y = 378, width = 1307, height = 75)

        btnContinue = Button(self, image = controller.BgMemberContinue, command=ContinueFunc)
        btnContinue.place(x = 1000, y = 553)

        btnHome = Button(self, image = controller.BgHome, command = Home)
        btnHome.place(x = 500, y = 553)

    
class MemberLogin(Frame):

    def __init__(self, parent, controller):
        global tapCardVar
        
        Frame.__init__(self, parent)
        self.controller = controller

        def Continue () :
            global mode
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
                    mode = 2
                    cardVar.set(str(Register[Num][0]))
                    memberNameVar.set(str(Register[Num][1]))
                    mobileNumVar.set(str(Register[Num][2]))
                    eAddVar.set(str(Register[Num][3]))
                    controller.show_frame("MemberData")
                else :
                    tkMessageBox.showinfo("","Invalid Card or Not Registered")

        def Home () :
            mode = 0
            EnterNumVar.set("")
            cardVar.set("")
            memberNameVar.set("")
            mobileNumVar.set("")
            eAddVar.set("")
            totalVar.set("")
            controller.show_frame("Choose")
                        
        
        label = Label(self, image = controller.BgMemberLogin)
        label.pack()

        tapCardVar = StringVar()
        tapCard = Entry(self, text = tapCardVar, font = ('Helvetica', 30), justify = "center", state = "readonly")
        tapCard.place(x = 386, y = 367, width = 1039, height = 97)

        btnContinue = Button (self, image = controller.BgMemberContinue, command = Continue)
        btnContinue.place(x = 1000, y = 553)

        btnHome = Button(self, image = controller.BgHome, command = Home)
        btnHome.place(x = 500, y = 553)

class MemberData(Frame):

    def __init__(self, parent, controller):
        global cardVar, memberNameVar, mobileNumVar, eAddVar, totalVar
        
        Frame.__init__(self, parent)
        self.controller = controller


        def Home () :
            mode = 0
            EnterNumVar.set("")
            cardVar.set("")
            memberNameVar.set("")
            mobileNumVar.set("")
            eAddVar.set("")
            totalVar.set("")
            controller.show_frame("Choose")

        label = Label(self, image = controller.BgMemberData)
        label.pack()

        # *************************************************************************
        # ************* TK CANVAS FOR PLOT ****************************************

        canvas2 = FigureCanvasTkAgg(f, self)
        canvas2.show()
        canvas2.get_tk_widget().place(x = 0 , y = 0, width = 0 , height = 0)

        toolbar = NavigationToolbar2TkAgg(canvas2, self)
        toolbar.update()
        canvas2._tkcanvas.place(x = 815, y = 85, width = 803, height = 369)

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

        btnAddTrash = Button(self, image = controller.BgAddTrash, command = lambda: controller.show_frame("MemAddtrash"))
        btnAddTrash.place(x = 980, y = 550)

        btnHome = Button(self, image = controller.BgBackHome, command = Home)
        btnHome.place(x = 1330, y = 550)

class MemAddtrash(Frame):

    def __init__(self, parent, controller):
        bottleCount = 0;
        Frame.__init__(self, parent)
        self.controller = controller
        
        def servo1Close ():
            servo1Angle(90)
            time.sleep(1)
        def servo1Open():
            servo1Angle(55)
            time.sleep(1)

        def servo2Close ():
            servo2Angle(55)
            time.sleep(1)
        def servo2Open():
            servo2Angle(90)
            time.sleep(1)

        def scan () :
            global bottleCount
            ctrFlag = 0;
            ## ***************************************************************
            ## ******************  B O T T L E  ******************************
           
            DET = GPIO.input(detPin)
            POT = GPIO.input(polPin)
            print "DET", DET, "POT", POT
            if DET != 1 or POT != 1:
                tkMessageBox.showerror("", "You've Place A\nWrong Item\nPlease Input Another\nThenPress OK")

            GPIO.output(TRIG, False)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            while GPIO.input(ECHO)==0:
                pulse_start = time.time()
            while GPIO.input(ECHO)==1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            print "Distance1:",distance,"cm"

            if distance < 13 :
                ctrFlag = 1
                print "distance 1 enter"
                servo1Open()
                servo1Close()
                controller.canCount = controller.canCount + 1
                
                
            GPIO.output(TRIG2, False)
            GPIO.output(TRIG2, True)
            time.sleep(0.00001)
            GPIO.output(TRIG2, False)
            while GPIO.input(ECHO2)==0:
                pulse_start = time.time()
            while GPIO.input(ECHO2)==1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            print "Distance2:",distance,"cm"

            if distance < 13 :
                 print "distance 2 enter"
                 ctrFlag = 1
                 servo2Open ()
                 servo2Close ()
                 controller.bottleCount = controller.bottleCount + 1
                 
            if ctrFlag == 1 :     
                 controller.show_frame("MemberDoneMore")
                 ctrFlag = 0

            
        label = Label(self, image = controller.BgMemberAddTrash)
        label.pack()

        btnScan = Button(self, image = controller.BgScan, command = scan)
        btnScan.place(x = 765, y = 600)

class MemberDoneMore(Frame):

    def __init__(self, parent, controller):
         
        bottleCount = 0;
        Frame.__init__(self, parent)
        self.controller = controller

        def Done () :
             global mode, cardVar
             if mode == 2 :
                  print "MEMBER MODE"
                  if controller.bottleCount != 0 :          
                       bottleData = open(controller.MemberPath + cardVar.get() +'/bottlecounter.txt','r')
                       x = bottleData.readlines()
                       for m in x :
                            y = int(m) + 1
                       print y
                       file = open(controller.MemberPath + cardVar.get() +'/bottlecounter.txt','w')
                       file.write(str(y))
                       file.close()
                       ## **************************
                       ## **************************
                       updateBottleData = open(controller.MemberPath + cardVar.get() +'/bottle.txt','a')
                       updateBottleData.write(str(y))
                       updateBottleData.write(',')
                       updateBottleData.write(str(controller.bottleCount))
                       updateBottleData.write('\n')
                       updateBottleData.close()
                       controller.bottleCount = 0
                       
                  if controller.canCount != 0 :
                       canData = open(controller.MemberPath + cardVar.get() +'/cancounter.txt','r')
                       x = canData.readlines()
                       for m in x :
                            y = int(m) + 1
                       file = open(controller.MemberPath + cardVar.get() +'/cancounter.txt','w')
                       file.write(str(y))
                       file.close()
                       ## **************************
                       ## **************************
                       updateCanData = open(controller.MemberPath + cardVar.get() +'/can.txt','a')
                       updateCanData.write(str(y))
                       updateCanData.write(',')
                       updateCanData.write(str(controller.canCount))
                       updateCanData.write('\n')
                       updateCanData.close()
                       controller.CanCount = 0
                       
             elif mode == 1:
                  print "GUEST MODE"
                  if controller.bottleCount != 0 :     
                       bottleData = open(controller.GuestPath + cardVar.get() +'/bottlecounter.txt','r')
                       x = bottleData.readlines()
                       for m in x :
                            y = int(m) + 1
                       print y
                       file = open(controller.GuestPath + cardVar.get() +'/bottlecounter.txt','w')
                       file.write(str(y))
                       file.close()
                       ## **************************
                       ## **************************
                       updateBottleData = open(controller.GuestPath + cardVar.get() +'/bottle.txt','a')
                       updateBottleData.write(str(y))
                       updateBottleData.write(',')
                       updateBottleData.write(str(controller.bottleCount))
                       updateBottleData.write('\n')
                       updateBottleData.close()
                       controller.bottleCount = 0
                       
                  if controller.canCount != 0 :
                       canData = open(controller.GuestPath + cardVar.get() +'/cancounter.txt','r')
                       x = canData.readlines()
                       for m in x :
                            y = int(m) + 1
                       file = open(controller.GuestPath + cardVar.get() +'/cancounter.txt','w')
                       file.write(str(y))
                       file.close()
                       ## **************************
                       ## **************************
                       updateCanData = open(controller.GuestPath + cardVar.get() +'/can.txt','a')
                       updateCanData.write(str(y))
                       updateCanData.write(',')
                       updateCanData.write(str(controller.canCount))
                       updateCanData.write('\n')
                       updateCanData.close()
                       controller.CanCount = 0
             controller.show_frame("MotherEarth")

        label = Label(self, image = controller.BlankBg)
        label.pack()

        btnDone = Button(self, image = controller.BgDone, command = Done)
        btnDone.place(x = 400, y = 300)

        btnAddMore = Button(self, image = controller.BgMore,
                            command=lambda: controller.show_frame("MemAddtrash"))
        btnAddMore.place(x = 1000, y = 300)

class MotherEarth(Frame):

    def __init__(self, parent, controller):
        bottleCount = 0;
        Frame.__init__(self, parent)
        self.controller = controller
        def OkFunc () :
             global mode
             
             if mode == 2 :
                  controller.show_frame("Redeem")
             elif mode == 1 :
                  controller.show_frame("GuestRedeem")
                  
        label = Label(self, image = controller.BgMotherEarth)
        label.pack()

        btnOk = Button(self, image = controller.BgOK,
                       command=OkFunc)
        btnOk.place(x = 765, y = 740)

class Redeem(Frame):

    def __init__(self, parent, controller):
        bottleCount = 0;
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, image = controller.BgRedeem)
        label.pack()

        btnOk = Button(self, image = controller.BgOK,
                       command=lambda: controller.show_frame("Experience"))
        btnOk.place(x = 765, y = 740)

class GuestRedeem(Frame):

    def __init__(self, parent, controller):
        bottleCount = 0;
        Frame.__init__(self, parent)
        self.controller = controller

        label = Label(self, image = controller.BgGuestRedeem)
        label.pack()

        btnOk = Button(self, image = controller.BgOK,
                       command=lambda: controller.show_frame("Experience"))
        btnOk.place(x = 765, y = 740)


class Experience(Frame):

    def __init__(self, parent, controller):
        bottleCount = 0;
        Frame.__init__(self, parent)
        self.controller = controller

        def one () :
                file = open(controller.eva1,'r')
                x = file.readlines()
                for m in x :
                        y = int(m) + 1
                print y
                file = open(controller.eva1,'w')
                file.write(str(y))
                file.close()
                controller.show_frame("StartPage")

        def two () :
                file = open(controller.eva2,'r')
                x = file.readlines()
                for m in x :
                        y = int(m) + 1
                print y
                file = open(controller.eva2,'w')
                file.write(str(y))
                file.close()
                controller.show_frame("StartPage")

        def three () :
                file = open(controller.eva3,'r')
                x = file.readlines()
                for m in x :
                        y = int(m) + 1
                print y
                file = open(controller.eva3,'w')
                file.write(str(y))
                file.close()
                controller.show_frame("StartPage")

        label = Label(self, image = controller.BgExperience)
        label.pack()

        btn1 = Button(self, image = controller.Bg1, command = one)
        btn1.place(x = 270, y = 500)

        btn2 = Button(self, image = controller.Bg2, command = two)
        btn2.place(x = 850, y = 500)

        btn3 = Button(self, image = controller.Bg3, command = three)
        btn3.place(x = 1380, y = 500)



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
            
            can = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ rfidVar.get() +'/can.txt','w')
            can.write('0,0')
            can.write('\n')
            can.close()

            cancounter = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ rfidVar.get() +'/cancounter.txt','w')
            cancounter.write('0')
            cancounter.write('\n')
            cancounter.close()

            bottle = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ rfidVar.get() +'/bottle.txt','w')
            bottle.write('0,0')
            bottle.write('\n')
            bottle.close()

            bottlecounter = open('/home/pi/Desktop/sourceCode/EarthJuan/'+ rfidVar.get() +'/bottlecounter.txt','w')
            bottlecounter.write('0')
            bottlecounter.write('\n')
            bottlecounter.close()

            rfidVar.set("")
            nameVar.set("")
            phonenumVar.set("")
            eaddVar.set("")
            flag = 1
            

def saveContact () :
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
