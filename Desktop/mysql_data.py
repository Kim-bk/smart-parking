from mysql.connector import connect, Error
from datetime import datetime

def createCheckIn(customer_card,license_plate,date_check_in):
    try:
        with connect(
            host="localhost",
            user="root",
            password="120301200201",
            database="parking_smart",
        ) as connection:
            print(connection)
            cursor = connection.cursor()
            cursor.execute("select *from customer where customer_card = '"+ customer_card+"' ")
            customer = cursor.fetchall()[0]
            dt = datetime.now()
            dt = dt.strftime("%d/%m/%Y %H:%M:%S") 
            data = {'date_check_in': date_check_in,
                'license_plate':license_plate,
                'customer':customer,
                'fee':0,
                'date_check_out':'',
                'status':True}
            cursor.execute("insert into customer_parking(date_check_in,license_plate,id_customer,fee,status) values ('"+data['date_check_in'] +"','"+data['license_plate'] +"','"+data['customer'][0]+"',0,True) ")
    except Error as e:
        print(e)
dt = datetime.now()
dt = dt.strftime("%d/%m/%Y %H:%M:%S") 
#createCheckIn('22723560168','73E-98765',dt)

def createCheckOut(customer_card,license_plate,date_check_out):   
    try:
        with connect(
            host="localhost",
            user="root",
            password="120301200201",
            database="parking_smart",
        ) as connection:
            print(connection)
            cursor = connection.cursor()
            cursor.execute("select *from customer where customer_card = '"+customer_card+"'")
            customer = cursor.fetchall()[0]
            kq = cursor.execute("update customer_parking set status = 0, fee=5000 , date_check_out='"+date_check_out+"' where license_plate = '"+license_plate+"' and id_customer ='"+ customer[0]+"' and status = 1 ")
            if kq == None:
                return 0
            return 1
    except Error as e:
        print(e)

dt = datetime.now()
dt = dt.strftime("%d/%m/%Y %H:%M:%S") 
#createCheckOut("22723560168",'43E-12345', dt )


def findAll():
    try:
        with connect(
            host="localhost",
            user="root",
            password="120301200201",
            database="parking_smart",
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("select *from customer_parking where status = 1 ")
            list =cursor.fetchall()
            results = []
            for item in list:
                cursor.execute("select *from customer where id = '"+item[6]+"' ")
                customer =cursor.fetchall()[0]
                data = {
                    "Card":customer[5],
                    "Name":customer[2],
                    "Phone_Number":customer[3],
                    "Booking_Date":item[1],
                    "Lisence_Plate":item[4],
                }
                results.append(data)
                
            return results
    except Error as e:
        print(e)
findAll()

def getByIdRfid(id_rfid):
    try:
        with connect(
            host="localhost",
            user="root",
            password="120301200201",
            database="parking_smart",
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("select *from customer where customer_card = '"+id_rfid+"' ")
            customer =cursor.fetchall()
            print(len(customer))
            if len(customer) == 0:
                return 0
            return 1
    except Error as e:
        print(e)
    
