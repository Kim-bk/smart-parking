import matplotlib.pyplot as plt
import numpy as np
import cv2
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

def show_results():
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


if __name__ == "__main__":
    #load the model has been trained before 
    model = keras.models.load_model('../License-Plate-Recognition/data/train/character_model.h5',custom_objects={"custom_f1score": custom_f1score})

     # Loads the data required for detecting the license plates from cascade classifier.
    #plate_cascade = cv2.CascadeClassifier('../License-Plate-Recognition/images/annotation/cascade.xml')
    plate_cascade = cv2.CascadeClassifier('../License-Plate-Recognition/archive/cascade.xml')
 
    img = cv2.imread('../License-Plate-Recognition/images/oto/82.jpg')
    #img = cv2.imread('../License-Plate-Recognition/images/oto/462.jpg')
    #img = cv2.imread('../License-Plate-Recognition/images/CarTGMT/AEONTP_6S81U5_checkin_2020-1-13-16-18bx9UOV6rY5.jpg')
    old_img = img

    # Getting plate prom the processed image
    output_img, plate = detect_plate(img)

    plt.figure(1)
    output_img_tg = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
    ax = plt.subplot(111)
    ax.imshow(output_img_tg)
    plt.axis('off')
 


    plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
    # plt.figure(figsize=(1,6))
    plt.figure(2)
    plate_tg = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
    ax = plt.subplot(111)
    ax.imshow(plate_tg)
    plt.title("Cắt khung chứa biển số")
    plt.axis('off')



    char = segment_characters(plate)
    plt.figure(5)
   
    for i in range(len(char)):
        plt.subplot(1, len(char) , i+1)
        plt.imshow(char[i], cmap='gray')
        plt.axis('off')
 

    print(show_results())
    # Segmented characters and their predicted value.
    plt.figure(6)
    for i,ch in enumerate(char):
        img = cv2.resize(ch, (28,28), interpolation=cv2.INTER_AREA)
        plt.subplot(3,4,i+1)
        plt.imshow(img,cmap='gray')
        plt.title(f'Ký tự dự đoán: {show_results()[i]}')


    plate_number = show_results()
    output_img, plate = detect_plate(old_img, plate_number)
    plt.figure(7)
    display(output_img, 'Nhận dạng ký tự của biển số xe')

    plt.show()



