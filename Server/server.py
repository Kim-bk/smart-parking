from datetime import datetime
from flask import Flask, request, render_template
import logging
import os
import io
import base64
import socket
import PIL.Image as Image
import requests
import cv2 as cv
import numpy as np
from urllib.request import urlopen

app = Flask(__name__)


@app.before_request
def log_request_info():
    logging.info('Headers: %s', request.headers)
    logging.info('Body: %s', request.get_data())


# Lấy ảnh từ server về
@app.route("/upload-image", methods=["POST"])
def upload_image():
    if request.method == "POST":  # if we make a post request to the endpoint, look for the image in the request body
        image_raw_bytes = request.get_data()  # get the whole body
        igm = Image.open(io.BytesIO(image_raw_bytes))
        igm.show()
        date = datetime.date(datetime.now())
        datetimenow = datetime.time(datetime.now())
        save_path = 'D:/PBL5/' + str(date)
        isExist = os.path.exists(save_path)
        if not isExist:
            os.makedirs(save_path)
            save_location = (
                os.path.join(save_path, str(datetimenow.hour) + "_" + str(datetimenow.minute) + "_" + str(
                    datetimenow.second) + ".jpg"))  # save to the same folder as the flask app live in
            f = open(save_location, 'wb+')  # wb for write byte data in the file instead of string
            f.write(image_raw_bytes)
            f.close()
            print("Image saved")
        else:
            save_location = (
                os.path.join(save_path, str(datetimenow.hour) + "_" + str(datetimenow.minute) + "_" + str(
                    datetimenow.second) + ".jpg"))  # save to the same folder as the flask app live in
            f = open(save_location, 'wb+')  # wb for write byte data in the file instead of string
            f.write(image_raw_bytes)
            f.close()
            print("Image saved")
        return image_raw_bytes
    return "if you see this, that is bad request method"


# Gui data lên server để esp lấy về
@app.route("/rfid", methods=["GET"])
def send_string():
    if request.method == "GET":  # if we make a post request to the endpoint, look for the image in the request body
        data = "True"
        requests.post("http://192.168.43.65:7350", data)
        return data


if __name__ == '__main__':
    str_input = input("Nhap chuc nang :")
    app.run(host='0.0.0.0', port= 7350)
    if str_input == "Chup anh":
        upload_image()
    if str_input == "Gui ":
        send_string()















