from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from numpy import size
from  tkinter import ttk
import cv2

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
img_entrance = Image.open("D:\Semester 6\PBL5\Desktop\img1.jpg")
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
image_entrance_full = Image.open("img2.jpg")
image_entrance_full = image_entrance_full.resize((250,250))
img1 = ImageTk.PhotoImage(image_entrance_full)
label_image = Label(frame_photograph,image=img1)
label_image.image = img1
label_image.place(x=280,y=40)

label_entrance_full = Label(frame_photograph,text='Camera and Image exit',font=('Courier',15,'bold'),fg='#008B8B')
label_entrance_full.place(x=140,y=350)
image_exit_full = Image.open("image2.jpg")
image_exit_full = image_exit_full.resize((250,250))
img2 = ImageTk.PhotoImage(image_exit_full)
label_image1 = Label(frame_photograph,image=img2)
label_image1.image = img2
label_image1.place(x=280,y=390)

root.mainloop()