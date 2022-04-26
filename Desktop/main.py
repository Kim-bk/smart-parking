from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from numpy import size
from  tkinter import ttk
import cv2
import sys
from PIL import Image, ImageTk
from datetime import datetime
import os

fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False
link_img="img1.jpg"
Dict = "./image/"


def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True

    button.place_forget()
    button1 = Button(frame_photograph, text="Take", command=saveAndExit)
    button2 = Button(frame_photograph, text="Again", command=resume)
    button1.place(anchor=CENTER, x = 100, y=310)
    button2.place(anchor=CENTER, x = 170, y=310)
    button1.focus()

def saveAndExit(event = 0):
    global link_img
    global prevImg

    if (len(sys.argv) < 2):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        timestamp = str(timestamp)
        filepath= timestamp.replace('.','_')
        filepath = Dict + filepath+".png"
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    link_img = filepath
    prevImg.save(filepath)

    # display
    image_entrance_full = Image.open(link_img)
    image_entrance_full = image_entrance_full.resize((250,250))
    img1 = ImageTk.PhotoImage(image_entrance_full)
    label_image = Label(frame_photograph,image=img1)
    label_image.image = img1
    label_image.place(x=280,y=40)
   
   

def resume(event = 0):
    global button1, button2, button, lmain, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(x = 120,y=300)
    lmain.after(10, show_frame)


   

def changeCam(event=0, nextCam=-1):
    global camIndex, cap, fileName

    if nextCam == -1:
        camIndex += 1
    else:
        camIndex = nextCam
    del(cap)
    cap = cv2.VideoCapture(camIndex)

    #try to get a frame, if it returns nothing
    success, frame = cap.read()
    if not success:
        camIndex = 0
        del(cap)
        cap = cv2.VideoCapture(camIndex)

    f = open(fileName, 'w')
    f.write(str(camIndex))
    f.close()

try:
    f = open(fileName, 'r')
    camIndex = int(f.readline())
except:
    camIndex = 0

cap = cv2.VideoCapture(camIndex)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()
if not success:
    if camIndex == 0:
        print("Error, No webcam found!")
        sys.exit(1)
    else:
        changeCam(nextCam=0)
        success, frame = cap.read()
        if not success:
            print("Error, No webcam found!")
            sys.exit(1)


#main
root = Tk()
root.geometry("1400x700")
root.title("Management's smart park")

### frame contains images to confirm
frame_confirm = Frame(root,width=800,height=280,borderwidth=3,relief="groove")
frame_confirm.place(x=570,y=20)


label_text_entrance = Label(frame_confirm,text="Image Entrance",font=('Courier',15),fg='#008B8B')
label_text_entrance.place(x=120,y=10)

label_text_exit = Label(frame_confirm,text="Image Exit",font=('Courier',15),fg='#008B8B')
label_text_exit.place(x=540,y=10)

# image 1
img_entrance = Image.open('img2.jpg')
img_entrance = img_entrance.resize((150,150))
test = ImageTk.PhotoImage(img_entrance)

label_entrance = Label(frame_confirm,image=test)
label_entrance.image = test
label_entrance.place(x=30,y=40)

label_entrance_analys = Label(frame_confirm,image=test)
label_entrance_analys.image = test
label_entrance_analys.place(x=190,y=40)

label_exit = Label(frame_confirm,image=test)
label_exit.image = test
label_exit.place(x=450,y=40)

label_exit_analys = Label(frame_confirm,image=test)
label_exit_analys.image = test
label_exit_analys.place(x=610,y=40)

#### frame contains table
frame_table = Frame(root,width=800,height=300,borderwidth=3,relief="groove")
frame_table.place(x=570,y=350)

label_table = Label(frame_table,text="List vehicle",font=('Courier',20,'bold'))
label_table.place(x=300,y=15)
set = ttk.Treeview(root)
set['column'] = ('id','full_Name','phone_number','booking_time','place','email','license_plates')
set.column("#0", width=0,  stretch=NO,)
set.column("id",anchor=CENTER, width=30)
set.column("full_Name",anchor=CENTER, width=200)
set.column("phone_number",anchor=CENTER, width=100)
set.column("booking_time",anchor=CENTER, width=100)
set.column("place",anchor=CENTER, width=80)
set.column("email",anchor=CENTER, width=160)
set.column("license_plates",anchor=CENTER, width=80)

set.heading("#0",text="",anchor=CENTER)
set.heading("id",text="id",anchor=CENTER)
set.heading("full_Name",text="full_name",anchor=CENTER)
set.heading("phone_number",text="phone_number",anchor=CENTER)
set.heading("booking_time",text="booking_time",anchor=CENTER)
set.heading("place",text="place",anchor=CENTER)
set.heading("email",text="email",anchor=CENTER)
set.heading("license_plates",text="license_plates",anchor=CENTER)



set.insert(parent='',index='end',iid=0,text='',values=('001','Ngo Nguyen Hoang Dung','0365551975','2022-04-21', 'Đại Lộc','nnhoangdungdh@gmail.com','92-EA 00206'))
set.place(x=600,y=400)

## frame contains image which photographed before entrance and before exit
frame_photograph = Frame(root,width=550,height=680,borderwidth=3,relief="groove")
frame_photograph.place(x=15,y=15)

label_entrance_full = Label(frame_photograph,text='Camera and Image entrance',font=('Courier',15,'bold'),fg='#008B8B')
label_entrance_full.place(x=140,y=10)
mainWindow = Frame(frame_photograph,width=250,height=250)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
mainWindow.place(x=10,y=40)
lmain = Label(mainWindow, compound=CENTER, anchor=CENTER, relief=RAISED)
lmain.config(width=250,height=250)
button = Button(frame_photograph, text="Capture", command=prompt_ok)
lmain.pack()
button.place(x = 120,y=300)
button.focus()

def show_frame():
    global cancel, prevImg, button
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()

root.mainloop()
