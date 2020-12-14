#Author: Jordon Calder
#Date: November 4th 2020
#Title: Elevator Calculator *Automated App*

#Dependecies or Libraries 
from tkinter import *
import pandas as pd
from PIL import ImageTk, Image
import math as mt
import os


class App(Frame):
    def __init__(self, master=None):
        # Pull excel with data. NOTE: The file can be updated and changes shown on restart of app
        self.file = pd.read_excel("Interval Chart.xlsx")

        Frame.__init__(self, master)
        self.frame = Frame(master)

        #Background Image
        photo = ImageTk.PhotoImage(Image.open("Lounge.jpg"))
        background_label = Label(self.frame, image=photo)
        background_label.image = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=3)
        

        # Initialize binding variables
        self.variable = StringVar()
        self.Rt = StringVar()
        self.Hc = StringVar()
        self.H = StringVar()
        self.variable.set(self.file["Facility Type"][0])
        self.Rt.set("")
        self.Hc.set("")
        self.H.set("")
        self.label6Text = StringVar()
        self.label7Text = StringVar()
        self.label6Text.set("Elevator Interval: {0}".format(self.file["Interval"][0]))
        self.label7Text.set("Estimated Waiting Time: {0}".format(self.file["Waiting Time"][0]))


        # Creating Dropdown for Facility
        self.dropdown = OptionMenu(self.frame, self.variable,*self.file["Facility Type"], command=self.updateLabels).grid(row=1)


        # Creating Labels
        self.indx = self.file.index[self.file["Facility Type"]==self.variable.get()]
        self.label1 = Label(self.frame, text="Select Facility Type: ",font=("Courier", 10)).grid(row=0, sticky = W)
        self.label6 = Label(self.frame, textvariable=self.label6Text).grid(row=0, column=1,sticky = W)
        self.label7 = Label(self.frame, textvariable=self.label7Text).grid(row=0, column =2, sticky = W)
        self.label2 = Label(self.frame, text="Enter the Round-trip time: ").grid(row=3, sticky = W,pady=2)
        self.label3 = Label(self.frame, text="Enter the Elevator handling capacity: ").grid(row=4, sticky = W, pady=2)
        self.label4 = Label(self.frame, text="Enter the 5-minute handling capacity: ").grid(row=5, sticky = W, pady=2)

        # Creating Entries
        self.rt = Entry(self.frame, textvariable=self.Rt).grid(row=3, column=1, sticky = W,pady=2)
        self.hc = Entry(self.frame, textvariable=self.Hc).grid(row=4, column=1, sticky = W,pady=2)
        self.h = Entry(self.frame, textvariable=self.H).grid(row=5, column=1, sticky = W,pady=2)

        # creating TextBox
        self.text = Text(self.frame)
        self.text.insert(INSERT,"Results will display here.....")
        self.text.grid(row=11, columnspan=6,rowspan=6, sticky = W, pady = 2)

        self.frame2  = Frame(self.frame)

        # Create Buttons
        self.button1 = Button(self.frame2, text="SUBMIT", command= lambda: self.ok("SUBMIT")).grid(row=0, column =0,sticky=E,pady=4, padx=3)
        self.button2 = Button(self.frame2, text="CLEAR", command= lambda: self.clear("SUBMIT")).grid(row=0,column =1, sticky=W, pady=4, padx=3)
        self.button3 = Button(self.frame2, text="QUIT", command= lambda: self.exitApp("SUBMIT")).grid(row=0,column =2, sticky=W, pady=4, padx=3)

        # Aligning Buttons' frame to mainFrame
        self.frame2.grid(row=8, column=1)
        self.frame.pack()

    # Update label6&7 function
    def updateLabels(self, value):
        upIndx = self.file.index[self.file["Facility Type"]==self.variable.get()]
        print(self.file["Interval"][upIndx[0]])
        self.label6Text.set("Elevator Interval: {0}".format(self.file["Interval"][upIndx[0]]))
        print("Elevator Interval: {0}".format(self.file["Interval"][upIndx[0]]))
        self.label7Text.set("Estimated Waiting Time: {0}".format(self.file["Waiting Time"][upIndx[0]]))

         
    # Calculating Functions
    def calculator(self, value):
        print ("value is: {0}:{1}:{2}:{3}".format(self.variable.get(), self.Rt.get(), self.Hc.get(), self.H.get()))
        indx = self.file.index[self.file["Facility Type"]==self.variable.get()]
        interval = str(self.file["Interval"][indx[0]])
        n= mt.ceil(float(self.Hc.get())/float(self.H.get()))
        print(interval)
        O=1
        message = []
        for N in range(n,0,-1):
            O=N
            i = float(self.Rt.get())/N
            if interval == "50+":
                tempinterval = int(interval[0:2])
                if i >= tempinterval:
                    message.append( """\n\n**Design meets performance requirements.
                            1. Number of Elevator: {0}
                            2. Interval calculated (I): {1}
                            3. Tolerance of I: {2}""".format(N, i, (i-tempinterval)))
                    break;
                else:
                    message.append( """\n**Design exceeds performance requirements. \nNumber of Elevator: {0},Interval calculated (I): {1}\n""".format(N, i))
            else:
                tempinterval1 = int(interval[0:2])
                tempinterval2 = int(interval[5:])
                print(i-tempinterval1)
                print(i-tempinterval2)
                if  ((i-tempinterval1) == 0.0 or (i-tempinterval2) == 0.0):
                    message.append("""\n\n**Design meets performance requirements.
                            1. Number of Elevator: {0}
                            2. Interval calculated (I): {1}
                            3. Tolerance of I: {2}""".format(N, i, (i-tempinterval2)))
                    break;
                elif -(0.5) <= (i-tempinterval1) <= 0.5 or (tempinterval1 <= i <= tempinterval2):
                    message.append("""\n\n**Design narrowly meets performance requirements.
                                1. Number of Elevator: {0}
                                2. Interval calculated (I): {1}
                                3. Tolerance of I: {2}""".format(N, i, (i-tempinterval1)))
                    break;
                elif (-(0.5) <= (i-tempinterval2) <= 0.5) or (tempinterval1 <= i <= tempinterval2):
                    message.append("""\n\n**Design narrowly meets performance requirements at:
                                1. Number of Elevator: {0}
                                2. Interval calculated (I): {1}
                                3. Tolerance of I: {2}""".format(N, i, (i-tempinterval2)))
                    break;
                else:
                    message.append("""\n**Design exceeds performance requirements. \nNumber of Elevator: {0},Interval calculated (I): {1}\n""".format(N, i))

            
            if N==1:
                message.append("\n\nThe list has been exhausted. Number of Elevator required: {0}".format(N-1))
                self.text.config(state=NORMAL)
                self.text.insert(INSERT,"".join(message))
                print("".join(message))

        if O!=1:
            self.text.config(state=NORMAL)
            self.text.insert(INSERT,"".join(message))
            print("".join(message))


    def ok(self, value):
        self.text.config(state=NORMAL)
        self.text.delete(1.0,END)
        print(~self.Rt.get().isdigit())
        if not self.Rt.get() or not self.Hc.get() or not self.H.get():
            self.text.config(state=NORMAL)
            self.text.insert(INSERT,"Null Value not accepted. Enter numberic values to continue...")
##        elif ("." in self.Rt.get()) or ("." in self.Hc.get()) or ("." in self.H.get()):
##            x = self.Rt.get().split(".")
##            y = self.Hc.get().split(".")
##            z = self.H.get().split(".")
##            lenTable = pd.DataFrame()
##            lenTable["Variable"] = ["x","y","z"]
##            lenTable["Boolean"] = [len(x),len(y),len(z)]
##            lenTable["Value1"] = [x[0],y[0],z[0]]
##            lenTable["Value2"] = [x[1],y[1],z[1]]
##            lenTable.drop(lenTable[lenTable["Boolean"]!=2].index, inplace=True)
##            print(lenTable["Value1"])
##            if (len(x) == 2) or (len(y) == 2) or (len(z) == 2):
##                if not (x[0].isdigit() and x[1].isdigit()) or not (y[0].isdigit()and y[1].isdigit()) or not (z[0].isdigit() and z[1].isdigit()):
##                    self.text.config(state=NORMAL)
##                    self.text.insert(INSERT,"String Value not accepted. Enter numberic values to continue...")
##                else:
##                    self.calculator(".")
##            else:
##                self.text.config(state=NORMAL)
##                self.text.insert(INSERT,"String Value not accepted. Enter numberic values to continue...")
##        elif not self.Rt.get().isdigit() or not self.Hc.get().isdigit() or not self.H.get().isdigit():
##            text.config(state=NORMAL)
##            text.insert(INSERT,"String Value not accepted. Enter numberic values to continue...")
        else:
            self.calculator(".")
              
    # Clear Textbox function
    def clear(self, value):
        self.text.config(state=NORMAL)
        self.text.delete(1.0,END)
        self.text.insert(INSERT,"Results shows here. Enter values to continue....")

    # Close program
    def exitApp(self, value):
        os._exit(0)


# Creating maser and sub Frames
mainFrame = Tk()
mainFrame.title("Buildings' Elevator Calculator")
run = App(mainFrame)
run.mainloop()
