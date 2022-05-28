from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTime, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
import sys
import cv2
import numpy as np
from PIL import ImageQt
import os
from flask import Flask,request, render_template

from threading import Thread
import sys
import requests
# Process database with mongodb
from datetime import datetime

from mongo import createCheckIn,findAll,createCheckOut,getByIdRfid


# AI code 
import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
import keras
from tensorflow.python.saved_model import loader_impl
from tensorflow.python.keras.saving.saved_model import load as saved_model_load
from sklearn.metrics import f1_score 

from Desktop.mongo import getPlatebyRfid 


def detect_plate(self, img, pos): # the function detects and perfors blurring on the number plate.
    plate_img = img.copy()
    roi = img.copy()
    plate_rect = plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.2, minNeighbors = 7) # detects numberplates and returns the coordinates and dimensions of detected license plate's contours.
    for (x,y,w,h) in plate_rect:
        roi_ = roi[y:y+h, x:x+w, :] # extracting the Region of Interest of license plate for blurring.
        plate = roi[y:y+h, x:x+w, :]
        cv2.rectangle(plate_img, (x+2,y), (x+w-3, y+h-5), (51,181,155), 3) # finally representing the detected contours by drawing rectangles around the edges.
         
        if pos == 'entrance':
            path = '../PBL5/detect/entrance_detect.jpg'
            cv2.imwrite(path, plate_img)
            self.lblImgEntrance.setPixmap(QtGui.QPixmap(path))
        if pos == 'exit':
            path = '../PBL5/detect/exit_detect.jpg'
            cv2.imwrite(path, plate_img)
            self.lblImgExit.setPixmap(QtGui.QPixmap(path))
        
    try:
        return plate_img, plate # returning the processed image.
    except UnboundLocalError:   return '0'


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

            # plt.figure(4)
            # cv2.rectangle(ii, (intX,intY), (intWidth+intX, intY+intHeight), (50,21,200), 2)
            # plt.imshow(ii, cmap='gray')

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
            
    # arbitrary function that stores sorted list of character indeces
    indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
    img_res_copy = []
    for idx in indices:
        img_res_copy.append(img_res[idx])# stores character images according to their index
    img_res = np.array(img_res_copy)

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
    dimensions = [LP_WIDTH/6, LP_WIDTH/2, LP_HEIGHT/10, 2*LP_HEIGHT/3]
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
    characters = '0123456789ABCDEFGHKLMNPSTUVXYZ'
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


def show_error_messagebox(err = ''):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    if err == 'wrong_plate':
        msg.setText("Biển số xe ra không đúng !")
    else:
        msg.setText("Không phát hiện được biển số xe vui lòng chụp lại !")
    msg.setWindowTitle("Warning MessageBox")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()

def show_success_messagebox():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Nhận dạng biển số thành công !")
    msg.setWindowTitle("Success MessageBox")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()


def reset(self, pos = ''):
    if pos == 'entrance':
        self.lblImgEntrance.clear()
        self.lblCutPlateIn.clear()
        self.txtPlateIn.clear()
        self.lblGrayIn.clear()

    elif pos == 'exit':
        self.lblImgExit.clear()
        self.txtPlateOut.clear()
        self.lblCutOut.clear()
        self.lblGrayOut.clear()

    else:
        self.lblImgEntrance.clear()
        self.lblImgExit.clear()
        self.lblCutPlateIn.clear()
        self.lblGrayIn.clear()
        self.lblGrayOut.clear()
        self.txtPlateIn.clear()
        self.txtPlateOut.clear()
        self.lblCutOut.clear()

def process_liscense(self, img, pos):
    # Getting plate prom the processed image
    try:
        _, plate = detect_plate(self, img, pos)
        if plate == '0':
            rs = '0'
        else:
            # Cắt khung chứa biển số
            plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
            plate_tg = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
            cv2.imwrite('plate_cut.jpg',plate_tg)
            char = segment_characters(plate)
            rs = show_results(char)
    except TypeError:  rs = '0'
    except ValueError: rs = '0'
    return rs


#Show cam esp32 vs webcam
class VideoThread(QThread):
    change_pixmap_signal1 = pyqtSignal(np.ndarray)
    change_pixmap_signal2 = pyqtSignal(np.ndarray)
 
    def run(self):
        cap_esp32_entrance = cv2.VideoCapture("http://192.168.43.26:81/stream")
        cap_esp32_exit = cv2.VideoCapture("http://192.168.43.115:81/stream")
     
        while True:
            ret1, cv_img1 = cap_esp32_entrance.read()
            ret2, cv_img2 = cap_esp32_exit.read()
            if  ret2  :
                self.change_pixmap_signal1.emit(cv_img1)
                self.change_pixmap_signal2.emit(cv_img2)
          
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()

        #Load the ui file 
        uic.loadUi("../PBL5/Desktop/ui-main.ui", self)
        self.txtPlateIn.setEnabled(False)
        self.txtPlateOut.setEnabled(False)

        #Edit width columns in table
        self.tbData.setColumnWidth(0,120)
        self.tbData.setColumnWidth(1,220)
        self.tbData.setColumnWidth(2,250)
        self.tbData.setColumnWidth(3,200)
        self.tbData.setColumnWidth(4,200)
        
        #Event
        self.btnEntrance.clicked.connect(self.btnEntrance_clicked)
        self.btnExit.clicked.connect(self.btnExit_clicked)
        # self.btnScreenshot_Entrance.clicked.connect(self.capture_entrance)
      
        self.btnScreenshot_Exit.clicked.connect(self.capture_exit)
        self.load_table()

        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal1.connect(self.update_image_entrance)
        self.thread.change_pixmap_signal2.connect(self.update_image_exit)
        # start the thread
        self.thread.start()
        #Show app
        self.show()
    
        app_ = Flask(__name__)
        # Gửi data lên server để esp lấy về
        @app_.route("/rfid", methods=["GET"])
        def send_string():
            if request.method == "GET":  # if we make a post request to the endpoint, look for the image in the request body
                if(getByIdRfid(id_rfid_vao)!=None):
                    #Code chụp ảnh và lưu biển số xe vào db ở đây 
                    self.capture_entrance(id_rfid_vao)
                    #*********
                    print("Da chup")
                    check ="True"
                    requests.post("http://192.168.43.65:7350", check)
                    return check
                else:
                    print("Cut")
                    check ="False"
                    requests.post("http://192.168.43.65:7350", check)
                    return check
                    
        @app_.route("/send-id", methods=["POST"])
        def get_id():
            if request.method == "POST":  # if we make a post request to the endpoint, look for the image in the request body
                data = request.get_data()
                global id_rfid_vao
                id = str(data)
                print(id[2:-1])
                id_rfid_vao = id[2:-1]
                return data
            # Gui data lên server để esp lấy về
        @app_.route("/rfid-ra", methods=["GET"])
        def send_string_ra():
            if request.method == "GET":  # if we make a post request to the endpoint, look for the image in the request body
                if(getByIdRfid(id_rfid_ra)!=None):
                    #Code chụp ảnh và lấy biển số xe ra
                    self.capture_exit(id_rfid_ra)
                    #***************
                    #Sau đó:
                    #if(Check biển số xe ra):
                    print("Da chup")
                    check ="True"
                    requests.post("http://192.168.43.65:7350", check)
                    return check
                else:
                    print("Cut")
                    check ="False"
                    requests.post("http://192.168.43.65:7350", check)
                    return check

        @app_.route("/update-sensor-ra", methods=["POST"])
        def get_id_ra():
            if request.method == "POST":  # if we make a post request to the endpoint, look for the image in the request body
                data = request.get_data()
                global id_rfid_ra
                id = str(data)
                print(id[2:-1])
                id_rfid_ra = id[2:-1]
                return data
        kwargs = {'host': '192.168.43.65', 'port': 7350, 'threaded': True, 'use_reloader': False, 'debug': False}
        flaskThread = Thread(target=app_.run, daemon=True, kwargs=kwargs).start()
        #load clock
        self.display_time()

    @pyqtSlot(np.ndarray)
    def display_time(self):
        while True:
            QApplication.processEvents()
            dt = datetime.now()
            # print(dt)
            if dt.hour < 10:
                if dt.minute < 10:
                    self.txtTime.setText('0%s:0%s:%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                elif dt.second < 10:
                    self.txtTime.setText('0%s:%s:0%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                elif dt.second <10 and dt.minute <10:
                    self.txtTime.setText('0%s:0%s:0%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                else:
                    self.txtTime.setText('0%s:%s:%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
        
            elif dt.minute < 10:
                if dt.hour < 10:
                    self.txtTime.setText('0%s:0%s:%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                elif dt.second < 10:
                    self.txtTime.setText('%s:0%s:0%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                elif dt.second < 10 and dt.hour < 10:
                    self.txtTime.setText('0%s:0%s:0%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                else:  
                    self.txtTime.setText('%s:0%s:%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))

            elif dt.second < 10:
                if dt.hour < 10:
                    self.txtTime.setText('0%s:%s:0%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                elif dt.minute < 10:
                    self.txtTime.setText('%s:0%s:0%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                elif dt.hour < 10 and dt.minute < 10:
                    self.txtTime.setText('0%s:0%s:0%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
                else:
                    self.txtTime.setText('%s:%s:0%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))
            
            else:
                self.txtTime.setText('%s:%s:%s  -  %s/%s/%s' %(dt.hour, dt.minute, dt.second, dt.day, dt.month, dt.year))


    def load_table(self):
        list = findAll()
        people =[]
        for item in list:
            data_item = {
                "Card":item["customer"]["customer_card"],
                "Name":item["customer"]["name"],
                "Phone_Number":item["customer"]["number_phone"],
                "Booking_Date":item["date_check_in"],
                "Lisence_Plate":item["license_plate"],
            }
            people.append(data_item)
       # people = [{"ID": "1", "Card": "100221", "Name": "Hoang Kim", "Phone Number": "0935740126" ,"Booking Date": "16/05/2022", "Lisence Plate": "43D92646" }]
        row = 0
        self.tbData.setRowCount(len(people))
        for person in people:
            self.tbData.setItem(row, 0, QtWidgets.QTableWidgetItem(person["Card"]))
            self.tbData.setItem(row, 1, QtWidgets.QTableWidgetItem(person["Name"]))
            self.tbData.setItem(row, 2, QtWidgets.QTableWidgetItem(person["Phone_Number"]))
            self.tbData.setItem(row, 3, QtWidgets.QTableWidgetItem(person["Booking_Date"]))
            self.tbData.setItem(row, 4, QtWidgets.QTableWidgetItem(person["Lisence_Plate"]))

            row = row + 1
                 
    def capture_entrance(self, id_rfid_vao):
        dt = datetime.now()
        dt = dt.strftime("%d/%m/%Y %H:%M:%S")  

        reset(self, 'entrance')
        image = ImageQt.fromqpixmap(self.lblCamEntrance.pixmap())
        path_capture_entrance = '../PBL5/capture/img-' + str(dt.day) + str(dt.month) + str(dt.year) + str(dt.hour) + str(dt.minute) + str(dt.second)+ '.jpg' 
        image.save(path_capture_entrance) 
        # get the absolute path in your computer
        img = cv2.imread(path_capture_entrance)
        char = process_liscense(self, img, 'entrance')

        if char == '0' or len(char) < 8:
            os.remove(path_capture_entrance)
            show_error_messagebox()
        else:
            # self.lblImgEntrance.setPixmap(QtGui.QPixmap(path_capture_entrance))
            print('Biển số xe vào: ' + str(len(char)))

            ##### Create data
            createCheckIn(id_rfid_vao,str(char),dt)

            # Hiện khung chứa biển số được cắt
            self.lblCutPlateIn.setPixmap(QtGui.QPixmap("plate_cut.jpg"))
            list_plate[0] = char

            # Hiện khung chứa biển số được cắt ảnh trắng đen
            self.lblGrayIn.setPixmap(QtGui.QPixmap("contour.jpg"))
            self.txtPlateIn.setText(char)

    def capture_exit(self):
        dt = datetime.now()
        dt = dt.strftime("%d/%m/%Y %H:%M:%S") 

        reset(self,'exit')
        image = ImageQt.fromqpixmap(self.lblCamExit.pixmap())
        dt = datetime.now()
        path_capture_exit = '../PBL5/capture/img-' + str(dt.day) + str(dt.month) + str(dt.year) + str(dt.hour) + str(dt.minute) + str(dt.second)+ '.jpg' 
        image.save(path_capture_exit) 
        # get the absolute path in your computer
        img = cv2.imread(path_capture_exit)
        char = process_liscense(self, img, 'exit')

        if char == '0' or len(char) < 8:
            os.remove(path_capture_exit)
            show_error_messagebox()
        else:
            if getPlatebyRfid(id_rfid_ra) != None:
                print('Biển số xe ra: ' + str(len(char)))
                ########## data
                createCheckOut(id_rfid_ra,str(char),dt)
                    
                # Hiện khung chứa biển số được cắt
                self.lblCutOut.setPixmap(QtGui.QPixmap("plate_cut.jpg"))
                list_plate[0] = char

                # Hiện khung chứa biển số được cắt ảnh trắng đen
                self.lblGrayOut.setPixmap(QtGui.QPixmap("contour.jpg"))
                self.txtPlateOut.setText(char)
            else:
                os.remove(path_capture_exit)
                show_error_messagebox('wrong_plate')

    def update_image_entrance(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.lblCamEntrance.setPixmap(qt_img)
      
       
    def update_image_exit(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.lblCamExit.setPixmap(qt_img)
       
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def btnExit_clicked(self):
        reset(self, 'exit')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)JPG Files (*.jpg);;PNG Files (*.png)", options=options)
        if fileName:
            # print(fileName)
            img = cv2.imread(fileName)
            char = process_liscense(self, img, 'exit')
            if char == '0' or len(char) < 8:
               show_error_messagebox()
            else: 
               # self.lblImgExit.setPixmap(QtGui.QPixmap(fileName))
                print('Biển số xe ra: ' + char)

                # Hiện khung chứa biển số được cắt
                self.lblCutOut.setPixmap(QtGui.QPixmap("plate_cut.jpg"))
                list_plate[0] = char
            
                # Hiện khung chứa biển số được cắt ảnh trắng đen
                self.lblGrayOut.setPixmap(QtGui.QPixmap("contour.jpg"))
                self.txtPlateOut.setText(char)
        
    def btnEntrance_clicked(self):
        reset(self, 'entrance')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)JPG Files (*.jpg);;PNG Files (*.png)", options=options)
        if fileName:
            # print(fileName)
            img = cv2.imread(fileName)
            char = process_liscense(self, img, 'entrance')

            if char == '0' or len(char) < 8:
                show_error_messagebox()
            else: 
              #  self.lblImgEntrance.setPixmap(QtGui.QPixmap(fileName))
                print('Biển số xe vào: ' + char)
                # Hiện khung chứa biển số được cắt
                self.lblCutPlateIn.setPixmap(QtGui.QPixmap("plate_cut.jpg"))
                list_plate[0] = char
            
                # Hiện khung chứa biển số được cắt ảnh trắng đen
                self.lblGrayIn.setPixmap(QtGui.QPixmap("contour.jpg"))

                self.txtPlateIn.setText(char)

if __name__ == "__main__":
    #Init variables for AI
    #Load the model has been trained before 
    model = keras.models.load_model('../PBL5/AI/data_test/character_model.h5',custom_objects={"custom_f1score": custom_f1score})
    plate_cascade = cv2.CascadeClassifier('../PBL5/AI/archive/cascade.xml')
    list_plate = ["",""]
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()