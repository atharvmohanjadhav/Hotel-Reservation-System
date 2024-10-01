import mysql.connector
from datetime import datetime
# Establish a connection to the database
conn = mysql.connector.connect(
    host="localhost",
    user="****",
    password="****",
    database="your database name"
)

cursor = conn.cursor()
class Hotel:
    def __init__(self):
        self.cursor = conn.cursor()
        self.menu()
    def menu(self):
        print("Welcome to our Hotel !!")
        choice = input("Press 1 to Check Available Rooms")

        if choice == "1":
            self.rooms_status()
            choice1 = input("Press 2 To Reserve Your Room")
            if choice1 == "2":
                self.reservation()
            else:
                exit()
        else:
            exit()
    def rooms_status(self):
        cursor.execute("SELECT RoomId, room_number, room_type ,price_per_night FROM Rooms WHERE is_available = True")
        rooms = cursor.fetchall()
        print("Available Rooms")
        for i in rooms:
            print(f"Room_Number:{i[1]}, Room_Type:{i[2]}, Price_Per_Night:{i[3]}")
    def reservation(self):
        f_name = str(input("Enter Your First Name:"))
        l_name = str(input("Enter Your Last Name:"))
        phone = str(input("Enter Your Mobile Number:"))
        email = str(input("Enter Your EmailId:"))
        aadhar = str(input("Enter Your Aadhar Number:"))
        adress = str(input("Enter Your Adress:"))
        #inserting records into guest
        cursor.execute("INSERT INTO guest (first_name,last_name,phone,email,aadhar_number,adress) VALUES (%s,%s,%s,%s,%s,%s)",(f_name,l_name,phone,email,aadhar,adress),multi=True)
        #print(cursor.rowcount,"Record Inserted")
        conn.commit()

        #insert records into reservation table
        room_no = input("Select Which room number you want to reserve:")
        check_in_date = input("Enter resrvation date(YY-MM-DD):")
        check_out_date = input("Enter date up to which you want to stay(YY-MM-DD):")
        status = "Reserved"

        # fetching room id and room price
        cursor.execute(f"SELECT RoomId,price_per_night FROM Rooms WHERE room_number = {room_no}")
        rooms = cursor.fetchall()
        room_id = rooms[0][0]
        price = rooms[0][1]

        #fetching guest id
        cursor.execute(f"SELECT GuestId FROM guest where aadhar_number = {aadhar}")
        guest = cursor.fetchall()
        guest_id = guest[0][0]

        from datetime import datetime
        date_format = "%Y-%m-%d"
        a = datetime.strptime(check_out_date, date_format)
        b = datetime.strptime(check_in_date, date_format)
        delta = a - b
        total_price = (delta.days) * int(price)

        cursor.execute(f"insert into reservation(GuestId,RoomId,check_in_date,check_out_date,reservation_status,total_price) values (%s,%s,%s,%s,%s,%s)",
                       (guest_id,room_id,check_in_date,check_out_date,status,total_price))
        conn.commit()
        print("Your Total Cost is: ", total_price)
        print("To Reserve Your Room plaese make payment")
        ammount = str(input("Enter ammount that you will pay:"))
        payment_type = str(input("Your payment method(Cash/Online/Credit Card): "))
        payment_date = check_in_date
        cursor.execute(f"SELECT ReservationId FROM reservation where GuestId = {guest_id}")
        reservation = cursor.fetchall()
        reservation_id = reservation[0][0]
        cursor.execute("insert into payment(ReservationId,ammount,payment_type,payment_date) values (%s,%s,%s,CURDATE())",
                       (reservation_id,ammount,payment_type))
        conn.commit()
        print("Your Reserved Succesfully !")
        print("Thank You !")


        cursor.execute(f"update rooms set is_available = False where room_number = {room_no}")
        conn.commit()


h = Hotel()
