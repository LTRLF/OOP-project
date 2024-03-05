from typing import Union
import uvicorn
from fastapi import FastAPI

class Controller:
    def __init__(self, name):
        self.__name = name
        self.__user_list = []
        self.__guest_list = []
        self.__flight_list = []
        self.__flight_instance_list = []
        self.__admin_list = []
        self.__airport_list = []

    def add_flight_instance_list(self, flight_instance):
        self.__flight_instance_list.append(flight_instance)

    def search_flight(self, departure, destination, departure_date, total_passenger, promocode = None):
        flight_list = {}
        for that_flight in self.__flight_instance_list:
            airplane = that_flight.airplane
            if that_flight.departure.name == departure and that_flight.destination.name == destination and that_flight.departure_date == departure_date:
                if (airplane.total_seat - (that_flight.count_reserverd_seat_type("hot_seat") + that_flight.count_reserverd_seat_type("standard_seat"))) >= total_passenger:
                    #remaining_hot_seat = airplane.count_seat_type("hot_seat") - that_flight.count_reserverd_seat_type("hot_seat")
                    remaining_std_seat = airplane.count_seat_type("standard_seat") - that_flight.count_reserverd_seat_type("standard_seat")
                    
                    if remaining_std_seat > 0:
                        lowest_price = airplane.seat_list["standard_seat"][0].price
                    else:
                        lowest_price = airplane.seat_list["standard_seat"][0].price

                    total_lowest_price = lowest_price * total_passenger
                    total_discount_price = total_lowest_price
                    if promocode is not None:
                        for that_promocode in Promocode.promocode_list:
                            if that_promocode.code == promocode:
                                discount_price =  lowest_price - (lowest_price * (that_promocode.discount/100))
                                break
                        total_discount_price = discount_price * total_passenger
                        flight_list[that_flight.flight_instance_no] = [departure, destination, departure_date, float(total_lowest_price), float(total_discount_price)]
                    else:
                        flight_list[that_flight.flight_instance_no] = [departure, destination, departure_date, float(total_lowest_price)]

        return flight_list

    def add_admin(self, admin):
        self.__admin_list.append(admin)

    def add_user(self, user):
        self.__user_list.append(user)

    def select_seat(self, flight_instance_no):
        flight_instance = self.search_flight_instance_by_flight_instance_no(flight_instance_no)
        seat_list = flight_instance.airplane.seat_list["hot_seat"] + flight_instance.airplane.seat_list["standard_seat"]
        reserved_seat_list = flight_instance.reserved_seat_list["hot_seat"] + flight_instance.reserved_seat_list["standard_seat"]
        seat_detail = {}
        available_seat = []
        for seat in seat_list:
            #dictionary
            seat_detail[seat.row + seat.column] = [seat.seat_type, seat.price]
            available_seat.append(seat.row + seat.column)
            for reserved_seat in reserved_seat_list:
                if (seat.row + seat.column) == (reserved_seat.row + reserved_seat.column):
                    available_seat.remove(reserved_seat.row + reserved_seat.column)
        select_seat_data = {"seat_detail":seat_detail, "available_seat":available_seat}
        return select_seat_data
    
    def search_user_by_user_id(self, user_id):
        for user in self.__user_list:
            if user.user_id == user_id:
                return user
            
    def price_summary(self, user_id, booking_no):
        user = self.search_user_by_user_id(user_id)
        booking = user.search_booking_by_number(booking_no)
        passengers = booking.passenger
        price_summary = 0

        for passenger in passengers:    
            boarding_pass = passenger.boarding_pass
            luggages = boarding_pass.luggage_list

            for luggage in luggages:
                price_summary += luggage.price

            seat = boarding_pass.seat
            price_summary += seat.price

        return price_summary

    def search_flight_instance_by_flight_instance_no(self, flight_instance_no):
        for flight_instance in self.__flight_instance_list:
            if flight_instance.flight_instance_no == flight_instance_no:
                return flight_instance
            
    def fill_info_and_select_package(self, user_id, flight_instance_no, gender, tel_no, name, birth_date, citizen_id, package = None):
        flight = self.search_flight_instance_by_flight_instance_no(flight_instance_no)
        user = self.search_user_by_user_id(user_id)
        
        booking = Booking(Booking.booking_no, flight.destination, flight.departure, flight.departure_date, flight.departure_time, flight.destination_date, flight.destination_time)
        Booking.booking_number += 1
        passenger = Passenger(gender, tel_no, name, birth_date, citizen_id)
        boardingpass = Boardingpass(flight.destination, flight.departure, flight.departure_date, flight.departure_time, flight.destination_date, flight.destination_time, flight.gate, flight.flight_no)

        if package != None:
            if package == 'big':
                price = 200
            elif package == 'medium':
                price = 100
            else:
                price = 50
            luggage = Luggage(package, Luggage.luggage_id, price)
            Luggage.luggage_number += 1
            boardingpass.add_luggage(luggage)
            

        boardingpass.add_seat(Seat("1","C","Hot Seat",1500))
        passenger.add_boardingpass(boardingpass)
        booking.add_passenger(passenger)
        user.add_booking(booking)
        return booking
    
    @property
    def flight_instance_list(self):
        return self.__flight_instance_list

class Admin:
    def __init__(self, admin_id):
        self.__admin_id = admin_id

    def add_flight_instance(self, flight_instance):
        controller.add_flight_instance_list(flight_instance)

    def add_promocode(self, code):
        Promocode.promocode_list.append(code)

class Guest:
    def __init__(self, guest_id):
        self.__guest_id = guest_id

class User(Guest):
    def __init__(self, email, user_id):
        self.__email = email
        self.__user_id = user_id
        self.__booking_list = []
    
    def view_account_detail(self):
        account_detail = []
        booking_info_list = []
        for that_booking in self.__booking_list:
            booking_info = []
            booking_info.append(that_booking.booking_no)
            booking_info.append(that_booking.departure.name)
            booking_info.append(that_booking.destination.name)
            booking_info.append(that_booking.departure_date)
            booking_info.append(that_booking.departure_time)
            booking_info.append(that_booking.arriving_date)
            booking_info.append(that_booking.arriving_time)
            booking_info_list.append(booking_info)
        
        account_detail.append(self.__email)
        account_detail.append(self.__user_id)
        account_detail.append(booking_info_list)
        return account_detail
            
    @property
    def user_id(self):
        return self.__user_id

    def add_booking(self, booking):
        if isinstance(booking, Booking):
            self.__booking_list.append(booking)

    def search_booking_by_number(self, booking_number):
        for booking in self.__booking_list:
            if isinstance(booking, Booking) and booking_number == booking.booking_no:
                return booking

class Promocode:
    promocode_list = []

    def __init__(self, code, discount, expire_date):
        self.__code = code
        self.__discount = discount
        self.__expire_date = expire_date
        Promocode.promocode_list.append(self)
     
    @property
    def code(self):
        return self.__code

    @property
    def discount(self):
        return self.__discount

    @property
    def expire_date(self):
        return self.__expire_date

class Booking:
    booking_number = 1
    def __init__(self, booking_no, destination, departure, departure_date, departure_time, arriving_date, arriving_time):
        self.__booking_no = Booking.booking_number
        self.__passenger_list = []
        self.__destination = destination
        self.__departure = departure
        self.__departure_date = departure_date
        self.__departure_time = departure_time
        self.__arriving_date = arriving_date
        self.__arriving_time = arriving_time
        self.__booking_status = None
        self.__payment = None 

    def update_booking_status(self):
        pass
    
    def update_payment(self):
        pass

    def add_passenger(self, passenger):
        self.__passenger_list.append(passenger)

    def search_passenger_by_citizen_id(self, citizen_id):
        for passenger in self.__passenger_list:
            if citizen_id == passenger.citizen_id:
                return passenger

    @property
    def passenger(self):
        return self.__passenger_list

    @property
    def booking_no(self):
        return self.__booking_no

    @property
    def destination(self):
        return self.__destination

    @property
    def departure(self):
        return self.__departure
    
    @property
    def departure_date(self):
        return self.__departure_date

    @property
    def departure_time(self):
        return self.__departure_time

    @property
    def arriving_date(self):
        return self.__arriving_date
    
    @property
    def arriving_time(self):
        return self.__arriving_time

class Payment:
    def pay(self):
        return True

class MobileBanking(Payment):
    def __init__ (self):
        self.__account_no = None
        self.__status = False
    
    def pay(self, account_no):
        self.__account_no = account_no
        self.__status = True
        return True

    @property
    def status(self):
        return self.__status

class Card(Payment):
    def __init__ (self):
        self.__card_no = None
        self.__security_code = None
        self.__status = False
    
    def pay(self, card_no, security_code):
        self.__card_no = card_no
        self.__security_code = security_code
        self.__status = True

    @property
    def status(self):
        return self.__status

class Transaction:
    __id = 1000000
    def __init__(self, booking, amount, payment_method: Payment): 
        self.__booking = booking
        self.__amount = amount
        self.__payment_method = payment_method
        self.__transaction_id = Transaction.__id
        self.__status = False
        Transaction.__id += 1
    
    def show_payment(self):
        return {
                "transaction_id": self.__transaction_id,
                "amount": self.__amount,
                "status" : True
                }

class Passenger:
    def __init__(self, gender, tel_no, name, birth_date, citizen_id):
        self.__gender = gender
        self.__tel_no = tel_no
        self.__name = name
        self.__birth_date = birth_date
        self.__citizen_id = citizen_id
        self.__boardingpass = None

    def add_boardingpass(self, boardingpass):
        self.__boardingpass = boardingpass
    
    @property
    def citizen_id(self):
        return self.__citizen_id

    @property
    def boarding_pass(self):
        return self.__boardingpass

class Boardingpass:
    def __init__(self, destination, departure, departure_date, departure_time, destination_date, destination_time, gate, flight_no):
        self.__destination = destination
        self.__departure = departure
        self.__departure_date = departure_date
        self.__departure_time = departure_time
        self.__destination_date = destination_date
        self.__destination_time = destination_time
        self.__gate = gate
        self.__flight_no = flight_no
        self.__luggage_list = []
        self.__seat = None

    def add_luggage(self, luggage):
        self.__luggage_list.append(luggage)

    def add_seat(self, seat):
        self.__seat = seat
    
    @property
    def seat(self):
        return self.__seat
    
    @property
    def luggage_list(self):
        return self.__luggage_list


class Luggage:
    luggage_number = 1
    def __init__(self, package, luggage_id, price):
        self.__owner = None
        self.__package = package
        self.__luggage_id = Luggage.luggage_number
        self.__price = price


    def set_owner(self, owner):
        self.__owner = owner

    @property
    def luggage_id(self):
        return self.__luggage_id

    @property
    def price(self):
        return self.__price

class Airport:
    def __init__(self, name):
        self.__name = name
        self.__current_airplane_list = []

    def get_current_airplane(self):
        return self.__current_airplane_list
    
    @property
    def name(self):
        return self.__name

class Flight:
    def __init__(self, departure, destination, flight_no):
        self.__departure = departure
        self.__destination = destination
        self.__flight_no = flight_no

    @property
    def departure(self):
        return self.__departure
    @property
    def destination(self):
        return self.__destination

    @property
    def flight_no(self):
        return self.__flight_no

class Flight_instance(Flight):
    def __init__(self, departure, destination, flight_no, flight_instance_no, departure_date, departure_time, destination_date, destination_time, airplane, gate):
        super().__init__(departure, destination, flight_no)
        self.__flight_instance_no = flight_instance_no
        self.__departure_date = departure_date
        self.__departure_time = departure_time
        self.__destination_date = destination_date
        self.__destination_time = destination_time
        self.__airplane = airplane
        self.__gate = gate
        self.__reserved_seat_list = {"hot_seat":[], "standard_seat":[]}

    @property
    def flight_instance_no(self):
        return self.__flight_instance_no
        
    @property
    def departure_date(self):
        return self.__departure_date
    @property
    def destination_date(self):
        return self.__destination_date
    @property
    def departure_time(self):
        return self.__departure_time
    @property
    def destination_time(self):
        return self.__destination_time

    @property
    def airplane(self):
        return self.__airplane

    @property
    def gate(self):
        return self.__gate

    @property
    def reserved_seat_list(self):
        return self.__reserved_seat_list

    def add_reserved_seat(self, reserved_seat, seat_type):
        self.reserved_seat_list[seat_type].append(reserved_seat)

    def count_reserverd_seat_type(self, seat_type):
        return len(self.__reserved_seat_list[seat_type])

class Airplane:
    def __init__(self, airplane_id, total_seat):
        self.__airplane_id = airplane_id
        self.__total_seat = total_seat
        self.__seat_list = {"hot_seat":[], "standard_seat":[]}

    @property
    def seat_list(self):
        return self.__seat_list
    @property
    def total_seat(self):
        return self.__total_seat

    def add_seat(self, seat, seat_type):
        self.__seat_list[seat_type].append(seat)
    
    def count_seat_type(self, seat_type):
        return len(self.__seat_list[seat_type])

class Seat:
    def __init__(self, row, column, seat_type, price):
        self.__row = row
        self.__column = column
        self.__seat_type = seat_type
        self.__price = price

    @property
    def row(self):
        return self.__row
    @property
    def column(self):
        return self.__column

    @property
    def seat_type(self):
        return self.__seat_type

    @property
    def price(self):
        return self.__price

class ReservedSeat(Seat):
    def __init__(self, row, column):
        super().__init__(row, column, None , None)
    
    
controller = Controller('AirAsia')

airplane1 = Airplane('001', 18)
airplane2 = Airplane('002', 6)
airplane3 = Airplane('003', 6)
airplane4 = Airplane('004', 6)
airplane5 = Airplane('005', 6)

airport1 = Airport('Chiangmai')
airport2 = Airport('Bangkok')
airport3 = Airport('Hatyai')

user1 = User('kwai@gmail', '00001')
user2 = User('kai@gmail', '00002')

admin1 = Admin('A')

airplane1.add_seat(Seat("1", "A", "Hot Seat", 1500), "hot_seat")
airplane1.add_seat(Seat("1", "B", "Hot Seat", 1500), "hot_seat")
airplane1.add_seat(Seat("1", "C", "Hot Seat", 1500), "hot_seat")
airplane1.add_seat(Seat("2", "A", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("2", "B", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("2", "C", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("3", "A", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("3", "B", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("3", "C", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("4", "A", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("4", "B", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("4", "C", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("5", "A", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("5", "B", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("5", "C", "Standard Seat", 1000), "standard_seat")
airplane1.add_seat(Seat("6", "A", "Hot Seat", 1500), "hot_seat")
airplane1.add_seat(Seat("6", "B", "Hot Seat", 1500), "hot_seat")
airplane1.add_seat(Seat("6", "C", "Hot Seat", 1500), "hot_seat")

airplane2.add_seat(Seat("1", "A", "Hot Seat", 1500), "hot_seat")
airplane2.add_seat(Seat("1", "B", "Hot Seat", 1500), "hot_seat")
airplane2.add_seat(Seat("1", "C", "Hot Seat", 1500), "hot_seat")
airplane2.add_seat(Seat("2", "A", "Standard Seat", 1000), "standard_seat")
airplane2.add_seat(Seat("2", "B", "Standard Seat", 1000), "standard_seat")
airplane2.add_seat(Seat("2", "C", "Standard Seat", 1000), "standard_seat")

airplane3.add_seat(Seat("1", "A", "Hot Seat", 1500), "hot_seat")
airplane3.add_seat(Seat("1", "B", "Hot Seat", 1500), "hot_seat")
airplane3.add_seat(Seat("1", "C", "Hot Seat", 1500, ), "hot_seat")
airplane3.add_seat(Seat("2", "A", "Standard Seat", 1000), "standard_seat")
airplane3.add_seat(Seat("2", "B", "Standard Seat", 1000), "standard_seat")
airplane3.add_seat(Seat("2", "C", "Standard Seat", 1000), "standard_seat")

airplane4.add_seat(Seat("1", "A", "Hot Seat", 1500), "hot_seat")
airplane4.add_seat(Seat("1", "B", "Hot Seat", 1500), "hot_seat")
airplane4.add_seat(Seat("1", "C", "Hot Seat", 1500), "hot_seat")
airplane4.add_seat(Seat("2", "A", "Standard Seat", 1000), "standard_seat")
airplane4.add_seat(Seat("2", "B", "Standard Seat", 1000), "standard_seat")
airplane4.add_seat(Seat("2", "C", "Standard Seat", 1000), "standard_seat")

airplane5.add_seat(Seat("1", "A", "Hot Seat", 1500), "hot_seat")
airplane5.add_seat(Seat("1", "B", "Hot Seat", 1500), "hot_seat")
airplane5.add_seat(Seat("1", "C", "Hot Seat", 1500, ), "hot_seat")
airplane5.add_seat(Seat("2", "A", "Standard Seat", 1000), "standard_seat")
airplane5.add_seat(Seat("2", "B", "Standard Seat", 1000), "standard_seat")
airplane5.add_seat(Seat("2", "C", "Standard Seat", 1000), "standard_seat")

controller.add_admin(admin1)
controller.add_user(user1)
admin1.add_flight_instance(Flight_instance(airport1, airport2, "F00001", "FI00001", "25-02-2024", "9:00", "25-02-2024", "10:20", airplane1, "1"))
admin1.add_flight_instance(Flight_instance(airport2, airport1, "F00001", "FI00002", "25-02-2024", "17:45", "25-02-2024", "19:05", airplane2, "1"))
admin1.add_flight_instance(Flight_instance(airport1, airport2, "F00001", "FI00003", "25-02-2024", "22:35", "25-02-2024", "23:55", airplane3, "1"))
admin1.add_flight_instance(Flight_instance(airport3, airport1, "F00001", "FI00004", "25-02-2024", "05:20", "25-02-2024", "06:45", airplane4, "1"))
admin1.add_flight_instance(Flight_instance(airport2, airport3, "F00001", "FI00005", "25-02-2024", "14:15", "25-02-2024", "16:20", airplane5, "1"))

admin1.add_promocode(Promocode('A1000', 10,'25-02-2029'))
admin1.add_promocode(Promocode('A2000', 10,'25-01-2029'))
admin1.add_promocode(Promocode('A3000', 10,'25-06-2029'))
admin1.add_promocode(Promocode('B1000', 20,'25-09-2029'))
admin1.add_promocode(Promocode('B2000', 20,'25-12-2029'))
admin1.add_promocode(Promocode('B3000', 20,'25-07-2029'))
admin1.add_promocode(Promocode('C1000', 30,'25-08-2029'))
admin1.add_promocode(Promocode('C2000', 30,'25-09-2029'))
admin1.add_promocode(Promocode('C3000', 30,'25-10-2029'))

#TODO seacrh flgiht
# print(controller.search_flight(airport3, airport1, "25-02-2024", 1))

#TODO select seat
# print(controller.select_seat("FI00001"))

#TODO promocode testcase
# print(Promocode.promocode_list)

#TODO view_account_detail
controller.fill_info_and_select_package('00001', 'FI00003', 'male', '0980111111', 'mark', '01/10/20', '19090021434941', 'big')
controller.fill_info_and_select_package('00001', 'FI00003', 'male', '0980111111', 'mark', '01/10/20', '19090021434941', 'big')

# for result in user1.view_account_detail() :
#     if type(result) is list : 
#         i = 1
#         for result2 in result :
#             print("  ", i , "." , result2)
#             i = i + 1
#     else :
#         print(result)

#TODO ReservedSeat testcase
# controller.flight_instance_list[0].add_reserved_seat(ReservedSeat("1", "A"))
# print(controller.select_seat("FI00001"))

#TODO price summary
# แตกเพราะ boooking_no ในระบบเป็น 1 ไม่ใช่ B00001
# controller.fill_info_and_select_package('00001', 'FI00003', 'male', '0980111111', 'mark', '01/10/20', '110111011923', 'big')
# print(controller.price_summary('00001', 1))


app = FastAPI()

#TODO search_flight FastAPI
# @app.get("/search_flight")
# def search_flight(departure : str, destination : str, departure_date : str, total_passenger : int, promocode : Union[str, None] = None):
    # return controller.search_flight(departure, destination, departure_date, total_passenger, promocode = None)
    # return "Hi"

# if __name__ == "__main__":
    # uvicorn.run("test1:app", host = "127.0.0.1", port = 8000, log_level = "info")

#TODO view_account_info FastAPI
# @app.get("/view_account_detail")
# def view_account_info(user_id : str):
    # user = controller.search_user_by_user_id(user_id)
    # return user.view_account_detail()


#TODO ReservedSeat FastAPI
# @app.get("/select_seat")
# def select_seat(flight_instance_no:str):
#     return controller.select_seat(flight_instance_no)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# if __name__ == "__main__":
#     uvicorn.run("test1:app", host="127.0.0.1", port=8000, log_level="info")

# # TODO fill_info testcase
# temp = controller.fill_info_and_select_package('00001', 'FI00003', 'male', '0980111111', 'mark', '01/10/20', '19090021434941', 'big')
# print(temp.destination.name)

# #TODO fill_info FastAPI
# app = FastAPI()

# @app.get("/fill_info_and_select_package")
# def select_seat(user_id:str, flight_instance_no:str, gender:str, tel_no:str, name:str, birth_date:str, citizen_id:str, package:str = None):
#     return controller.fill_info_and_select_package(user_id, flight_instance_no, gender, tel_no, name, birth_date, citizen_id, package = None)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# if __name__ == "__main__":
#     uvicorn.run("test1:app", host="127.0.0.1", port=8000, log_level="info")

#TODO price summary
# @app.get("/price_summary")
# def price_summary(user_id:str, booking_no:int):
#     return controller.price_summary(user_id, booking_no)

# if __name__ == "__main__":
#     uvicorn.run("test1:app", host="127.0.0.1", port=8000, log_level="info")
