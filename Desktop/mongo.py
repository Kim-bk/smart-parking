from ast import Return
from asyncio.windows_events import NULL
import re
from pymongo import MongoClient
from datetime import datetime
#data_find = test.find_one({"customer_card":"123456789"})

def connection():
    uri = 'mongodb+srv://hoangdung0203:uVlT3TxinFZ8UBft@cluster0.qozrr.mongodb.net/smart_parking?retryWrites=true&w=majority'
    conn = MongoClient(uri)
    return conn


def createCheckIn(customer_card,license_plate,date_check_in,cut_img,contour_img):
    db_customer = connection()['smart_parking']['customer']
    db_parking = connection()['smart_parking']['customer_parking']
    data_find = db_customer.find_one({"customer_card":customer_card})

    data = {'date_check_in': date_check_in,
            'license_plate':license_plate,
            'customer':data_find,
            'fee':0,
            'date_check_out':'',
            'status':True,
            'cut_img':cut_img,
            'contour_img':contour_img
            }
    kq=db_parking.find_one({"customer": data_find,'status':True})
    if kq != None:
        kq=db_parking.update_one({"customer": data_find,'status':True}, 
                                 {"$set": {"license_plate":data['license_plate'],"date_check_in":data['date_check_in'],"cut_img" : data['cut_img'],"contour_img":data['contour_img']} })
    else:
        db_parking.insert_one(data)


dt = datetime.now()
dt = dt.strftime("%d/%m/%Y %H:%M:%S")  
#createCheckIn("8317128168",'92EA-98765', dt )

def getImageExit(customer_card):
    db_customer = connection()['smart_parking']['customer']
    db_parking = connection()['smart_parking']['customer_parking']
    customer = db_customer.find_one({"customer_card": customer_card})
    kq=db_parking.find_one({"customer": customer,'status':True})
    return kq

def createCheckOut(customer_card,license_plate,date_check_out):
    db_customer = connection()['smart_parking']['customer']
    db_parking = connection()['smart_parking']['customer_parking']
    customer = db_customer.find_one({"customer_card": customer_card})
    kq=db_parking.find_one_and_update({"customer": customer,'license_plate':license_plate,'status':True}, 
                                 {"$set": {"date_check_out": date_check_out,"fee":5000,'status':False}})
    
    return kq
        
dt = datetime.now()
dt = dt.strftime("%d/%m/%Y %H:%M:%S")  
#createCheckOut("22723560168",'92EA-12345', dt )

def findAll():
    db_parking = connection()['smart_parking']['customer_parking']
    list_customer_parking = db_parking.find({'date_check_out':''},{})
    return list_customer_parking   

def getByIdRfid(id_rfid):
    db_customer = connection()['smart_parking']['customer']
    results = db_customer.find_one({'customer_card':id_rfid})
    return results

def getImageExit(customer_card):
    db_customer = connection()['smart_parking']['customer']
    db_parking = connection()['smart_parking']['customer_parking']
    customer = db_customer.find_one({"customer_card": customer_card})
    kq=db_parking.find_one({"customer": customer,'status':True})
    return kq
