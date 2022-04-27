from tkinter import *
from tkinter import font
from tkinter import filedialog
from PIL import Image, ImageTk
from numpy import size
from  tkinter import ttk
import cv2
import sys
from PIL import Image, ImageTk
from datetime import datetime
import os
import win32api

# AI code 
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
import keras
from tensorflow.python.saved_model import loader_impl
from tensorflow.python.keras.saving.saved_model import load as saved_model_load
from sklearn.metrics import f1_score 


# Testing the above function
def display(img_, title=''):
    img = cv2.cvtColor(img_, cv2.COLOR_BGR2RGB)
    # plt.figure(figsize=(1,6))
    ax = plt.subplot(111)
    ax.imshow(img)

    plt.axis('off')
    plt.title(title)
 


def detect_plate(img, text=''): # the function detects and perfors blurring on the number plate.
    try:
        plate_img = img.copy()
        roi = img.copy()

        plate_rect = plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.2, minNeighbors = 7) # detects numberplates and returns the coordinates and dimensions of detected license plate's contours.
    
        # print(plate_rect)
        for (x,y,w,h) in plate_rect:
            roi_ = roi[y:y+h, x:x+w, :] # extracting the Region of Interest of license plate for blurring.
            plate = roi[y:y+h, x:x+w, :]
            cv2.rectangle(plate_img, (x+2,y), (x+w-3, y+h-5), (51,181,155), 3) # finally representing the detected contours by drawing rectangles around the edges.
        if text!='':
            plate_img = cv2.putText(plate_img, text, (x-w//2,y-h//2), 
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.5, (51,181,155), 1, cv2.LINE_AA)
            
        return plate_img, plate # returning the processed image.

    except UnboundLocalError:
            message = "Không phát hiện được biển số xe vui lòng chụp lại!"
            win32api.MessageBox(0, message, 'title')

# Match contours to license plate or character template
def find_contours(dimensions, img) :

    # Find all contours in the image
    cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Retrieve potential dimensions
    lower_width = dimensions[0]
    upper_width = dimensions[1]
    lower_height = dimensions[2]
    upper_height = dimensions[3]
    
    # Check largest 5 or  15 contours for license plate or character respectively
    cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:15]
    
    ii = cv2.imread('contour.jpg')
    
    x_cntr_list = []
    target_contours = []
    img_res = []
    for cntr in cntrs :
        # detects contour in binary image and returns the coordinates of rectangle enclosing it
        intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)
        
        # checking the dimensions of the contour to filter out the characters by contour's size
        if intWidth > lower_width and intWidth < upper_width and intHeight > lower_height and intHeight < upper_height :
            x_cntr_list.append(intX) #stores the x coordinate of the character's contour, to used later for indexing the contours

            char_copy = np.zeros((44,24))
            # extracting each character using the enclosing rectangle's coordinates.
            char = img[intY:intY+intHeight, intX:intX+intWidth]
            char = cv2.resize(char, (20, 40))

            plt.figure(4)
            cv2.rectangle(ii, (intX,intY), (intWidth+intX, intY+intHeight), (50,21,200), 2)
            plt.imshow(ii, cmap='gray')

            # Make result formatted for classification: invert colors
            char = cv2.subtract(255, char)

            # Resize the image to 24x44 with black border
            char_copy[2:42, 2:22] = char
            char_copy[0:2, :] = 0
            char_copy[:, 0:2] = 0
            char_copy[42:44, :] = 0
            char_copy[:, 22:24] = 0

            img_res.append(char_copy) # List that stores the character's binary image (unsorted)
    
  
    # Return characters on ascending order with respect to the x-coordinate (most-left character first)
            
    # plt.show()
    # arbitrary function that stores sorted list of character indeces
    indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
    img_res_copy = []
    for idx in indices:
        img_res_copy.append(img_res[idx])# stores character images according to their index
    img_res = np.array(img_res_copy)
    # print(img_res)

    return img_res

# Find characters in the resulting images
def segment_characters(image) :

    # Preprocess cropped license plate image
    img = cv2.resize(image, (333, 75))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_binary = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_erode = cv2.erode(img_binary, (3,3))
    img_dilate = cv2.dilate(img_erode, (3,3))

    LP_WIDTH = img_dilate.shape[0]
    LP_HEIGHT = img_dilate.shape[1]

    # Make borders white
    img_dilate[0:3,:] = 255
    img_dilate[:,0:3] = 255
    img_dilate[72:75,:] = 255
    img_dilate[:,330:333] = 255

    # Estimations of character contours sizes of cropped license plates
    plt.figure(3)
    dimensions = [LP_WIDTH/6, LP_WIDTH/2, LP_HEIGHT/10, 2*LP_HEIGHT/3]
    plt.imshow(img_dilate, cmap='gray')
    cv2.imwrite('contour.jpg',img_dilate)
    # Get contours within cropped license plate
    char_list = find_contours(dimensions, img_dilate)
    return char_list

# Predicting the output
def fix_dimension(img): 
  new_img = np.zeros((28,28,3))
  for i in range(3):
    new_img[:,:,i] = img
  return new_img

def show_results(char):
    dic = {}
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i,c in enumerate(characters):
        dic[i] = c

    output = []
    for i,ch in enumerate(char): #iterating over the characters
        img_ = cv2.resize(ch, (28,28), interpolation=cv2.INTER_AREA)
        img = fix_dimension(img_)
        img = img.reshape(1,28,28,3) #preparing image for the model
     

        predict_x = model.predict(img)[0] 
        y_= np.argmax(predict_x)
        # y_ = model.predict_classes(img)[0] #predicting the class
        character = dic[y_] #
        output.append(character) #storing the result in a list
        
    plate_number = ''.join(output)
    
    return plate_number

# Metrics for checking the model performance while training
def f1score(y, y_pred):
  return f1_score(y, tf.math.argmax(y_pred, axis=1), average='micro') 

def custom_f1score(y, y_pred):
  return tf.py_function(f1score, (y, y_pred), tf.double)

  
# end AI code


fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False
filePath = ''
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
    label_image = Label(frame_photograph,image=img1,borderwidth=3,relief="groove")
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

def openFileExit():
    global filePath
    filePath = filedialog.askopenfilename()
    print(filePath)
    if len(filePath)>0:
        img_entrance = Image.open(filePath)
        img_entrance = img_entrance.resize((250,250))
        test = ImageTk.PhotoImage(img_entrance)
   
    
    label_image_test = Label(frame_photograph,image=test,borderwidth=3,relief='groove')
    label_image_test.image = test
    label_image_test.place(x=280,y=350)


    img = cv2.imread(filePath)
    old_img = img

    # Getting plate prom the processed image
    output_img, plate = detect_plate(img)

    # Cắt khung chứa biển số
    plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
    plate_tg = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)

    cv2.imwrite('plate_tg.jpg',plate_tg)
    char = segment_characters(plate)
    print('Biển số xe ra: ' + show_results(char))


    label_text_plate = Label(frame_confirm,text=show_results(char),font=('Courier',22),fg='#008B8B')
    label_text_plate.place(x=530,y=210)
    list_plate[0] = show_results(char) 
    # # Hiện khung chứa biển số được cắt
    plate_tg = Image.open('plate_tg.jpg')
    plate_tg = plate_tg.resize((150,150))
    plate_tg = ImageTk.PhotoImage(plate_tg)
   
    
    frame_liensce_plate_exit = Label(frame_confirm,image=plate_tg,borderwidth=3,relief='groove')
    frame_liensce_plate_exit.image = plate_tg
    frame_liensce_plate_exit.place(x=450,y=40)

    
    # Hiện khung chứa biển số được cắt ảnh trắng đen
    contour = Image.open('contour.jpg')
    contour = contour.resize((150,150))
    contour = ImageTk.PhotoImage(contour)
   
    
    frame_liensce_plate_analys_exit = Label(frame_confirm,image=contour,borderwidth=3,relief='groove')
    frame_liensce_plate_analys_exit.image = contour
    frame_liensce_plate_analys_exit.place(x=610,y=40)



def openFileEntrance():
 
    filePath = filedialog.askopenfilename()
   # print(filePath)
    if len(filePath)>0:
        img_entrance = Image.open(filePath)
        img_entrance = img_entrance.resize((250,250))
        test = ImageTk.PhotoImage(img_entrance)
   
    
    label_image_test_entrance = Label(frame_photograph,image=test,borderwidth=3,relief='groove')
    label_image_test_entrance.image = test
    label_image_test_entrance.place(x=10,y=350)


    img = cv2.imread(filePath)
    old_img = img

    # Getting plate prom the processed image
    output_img, plate = detect_plate(img)

    # Cắt khung chứa biển số
    plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
    plate_tg = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)

    cv2.imwrite('plate_tg.jpg',plate_tg)
    char_in = segment_characters(plate)
    print('Biển số xe vào: ' + show_results(char_in))

    
    label_text_plate = Label(frame_confirm,text=show_results(char_in),font=('Courier',22),fg='#008B8B')
    label_text_plate.place(x=110,y=210)
    list_plate[1] = show_results(char_in) 
    # # Hiện khung chứa biển số được cắt
    plate_tg = Image.open('plate_tg.jpg')
    plate_tg = plate_tg.resize((150,150))
    plate_tg = ImageTk.PhotoImage(plate_tg)
   
    
    frame_liensce_plate_entrance = Label(frame_confirm,image=plate_tg,borderwidth=3,relief='groove')
    frame_liensce_plate_entrance.image = plate_tg
    frame_liensce_plate_entrance.place(x=30,y=40)

    
    # Hiện khung chứa biển số được cắt ảnh trắng đen
    contour = Image.open('contour.jpg')
    contour = contour.resize((150,150))
    contour = ImageTk.PhotoImage(contour)
    
    frame_liensce_plate_analys_entrance = Label(frame_confirm,image=contour,borderwidth=3,relief='groove')
    frame_liensce_plate_analys_entrance.image = contour
    frame_liensce_plate_analys_entrance.place(x=190,y=40)


def check_plate(event = 0):
   
    if list_plate[0] == '' or list_plate[1] == '':
        message = "Thiếu dữ liệu hình ảnh!"
        win32api.MessageBox(0, message, 'title')
    else:
        if list_plate[0] == list_plate[1] :
            message = "Biển số xe vào ra hợp lệ!"
            win32api.MessageBox(0, message, 'title')
        else:
            message = "Biển số xe vào ra không hợp lệ!"
            win32api.MessageBox(0, message, 'title')

    #main
  #load the model has been trained before 
model = keras.models.load_model('../PBL5/AI/data/train/character_model.h5',custom_objects={"custom_f1score": custom_f1score})
plate_cascade = cv2.CascadeClassifier('../PBL5/AI/archive/cascade.xml')
list_plate = ["",""]


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




frame_liensce_plate_entrance = Frame(frame_confirm,borderwidth=3,relief='groove',height=150,width=150)
frame_liensce_plate_entrance.place(x=30,y=40)

frame_liensce_plate_analys_entrance = Frame(frame_confirm,borderwidth=3,relief='groove',height=150,width=150)
frame_liensce_plate_analys_entrance.place(x=190,y=40)


frame_liensce_plate_exit = Frame(frame_confirm,borderwidth=3,relief='groove',height=150,width=150)
frame_liensce_plate_exit.place(x=450,y=40)

frame_liensce_plate_analys_exit = Frame(frame_confirm,borderwidth=3,relief='groove',height=150,width=150)
frame_liensce_plate_analys_exit.place(x=610,y=40)

button_check = Button(frame_confirm,fg='#006400',bg='#FFF0F5',font=('Courier',15,'bold'),text='CHECK',command=check_plate)
button_check.place(x=350,y=200)


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

image_frame = Frame(frame_photograph,width=250,height=250,borderwidth=3,relief='groove')
image_frame.place(x=280,y=40)

button_file_entrance = Button(frame_photograph,text="Open Entrance",command=openFileEntrance)
button_file_entrance.place(x=10,y=320)
image_frame_test_entrance = Frame(frame_photograph,width=250,height=250,borderwidth=3,relief='groove')
image_frame_test_entrance.place(x=10,y=350)

button_file = Button(frame_photograph,text="Open Exit",command=openFileExit)
button_file.place(x=300,y=320)
image_frame_test = Frame(frame_photograph,width=250,height=250,borderwidth=3,relief='groove')
image_frame_test.place(x=280,y=350)

show_frame()
mainWindow.mainloop()

root.mainloop()


