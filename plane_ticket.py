class Controller:
    def __init__(self,name):
        self.__name = name
        self.__user_list = []
        self.__guest_list = []
        self.__promocode_list = []
        self.__flight_list = []
        self.__flight_instance_list = []
        self.__admin_list = []
        self.__airport_list = []

    def add_flight_instance_list(self, flight_instance):
        self.__flight_instance_list.append(flight_instance)

    def search_fight_instance_by_number(self, number):
        for flight_instance in self.__flight_instance_list:
            if number == flight_instance.flight_instance_no:
                return flight_instance

    def search_flight(self, departure, destination, departure_date, total_passenger, promocode = None):
        for that_flight in self.__flight_instance_list:
            if that_flight.departure_location == departure and that_flight.destination_location == destination and that_flight.departure_date == departure_date:
                if (that_flight.total_seat - that_flight.count_reserved_list) >= total_passenger:
                    return that_flight

    def add_admin(self, admin):
        self.__admin_list.append(admin)

    def select_seat(self, flight_instance_no):
        flight_instance = self.search_fight_instance_by_number(flight_instance_no)
        seat_list = flight_instance.airplane.seat_list
        reserved_seat_list = flight_instance.reserved_seat_list
        seat_detail = {}
        available_seat = []
        for seat in seat_list:
            #dictionary
            seat_detail[seat.row + seat.column] = [seat.seat_type,seat.price]
            available_seat.append(seat.row + seat.column)
            for reserved_seat in reserved_seat_list:
                if (seat.row + seat.column) == (reserved_seat.row + reserved_seat.column):
                    available_seat.remove(reserved_seat.row + reserved_seat.column)
        select_seat_data = {"seat_detail":seat_detail,"available_seat":available_seat}
        return select_seat_data
    
    @property
    def flight_instance_list(self):
        return self.__flight_instance_list

class Admin:
    def __init__(self,admin_id):
        self.__admin_id 

    def add_flight(self):
        pass
    def add_promocode(self):
        pass

class Guest:
    def __init__(self,guest_id):
        self.__guest_id = guest_id

class User(Guest):
    def __init__(self,email,user_id,):
        self.__email = email
        self.__user_id = user_id
        self.__booking_list = []
    
    def view_account_detail(self, ):
        booking_info_list = []
        for that_booking in self.__booking_list:
            booking_info = []
            booking_info.append(that_booking.booking_no)
            booking_info.append(that_booking.departure)
            booking_info.append(that_booking.destination)
            booking_info.append(that_booking.departure_date_time)
            booking_info.append(that_booking.arriving_date_time)
            booking_info_list.append(booking_info)
        return booking_info_list

    @property
    def user_id(self):
        return self.__user_id

class Promocode:
    def __init__(self, code, type, expire_date):
     self.__code = code
     self.__type = type
     self.__expire_date = expire_date

    @property
    def promocode_no(self):
        return self.__code
    # def check_promocode(self, input_code):
    #     if input_code == self.__code:
    #         return True

class Booking:
    def __init__(self, booking_no, destination, departure, departure_date_time, arriving_date_time):
        self.__booking_no = booking_no
        self.__passenger_list = []
        self.__destination = destination
        self.__departure = departure
        self.__departure_date_time = departure_date_time
        self.__arriving_date_time = arriving_date_time
        self.__booking_status = None
        self.__payment = None 

    def update_booking_status(self):
        pass
    
    def update_payment(self):
        pass

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
    def departure_date_time(self):
        return self.__departure_date_time
    @property
    def arriving_date_time(self):
        return self.__arriving_date_time

class Payment:
    def __init__(self,user_id,amount,transaction_id,payment_type,payment_status):
        self.__user_id = user_id
        self.__amount = amount
        self.__transaction_id = transaction_id
        self.__payment_type = payment_type
        self.__payment_status = payment_status

class MobileBanking(Payment):
    def __init__ (self,account):
        self.__account = account
    
    def paid_by_mobilebanking(self):
        pass
    
class Card(Payment):
    def __init__ (self,card_no):
        self.__card_no = card_no

    def paid_by_card(self):
        pass

class CreditCard(Card):
    def __init__ (self,card_limit):
        self.__card_limit = card_limit

class DebitCard(Card):
    def __init__ (self,balance):
        self.__balance = balance   

class Passenger:
    def __init__(self, gender, tel_no, name, birth_date, citizen_id, boarding_pass):
        self.__gender = gender
        self.__tel_no = tel_no
        self.__name = name
        self.__birth_date = birth_date
        self.__citizen_id = citizen_id
        self.__boarding_pass = boarding_pass

class Boardingpass:
    def __init__(self, destination, departure, departure_date_time, arriving_date_time, gate, flight_no):
        self.__destination = destination
        self.__departure = departure
        self.__departure_date_time = departure_date_time
        self.__arriving_date_time = arriving_date_time
        self.__gate = gate
        self.__flight_no = flight_no
        self.__luggage_list = []

class Luggage:
    def __init__(self, owner, package, luggage_id):
        self.__owner = owner
        self.__package = package
        self.__luggage_id = luggage_id
    
class Airport:
    def __init__(self, name):
        self.__name = name
        self.__current_airplane_list = []

    def get_current_airplane(self):
        return self.__current_airplane_list

class Flight:
    def __init__(self,departure, destination, flight_no):
        self.__departure = departure
        self.__destination = destination
        self.__flight_no = flight_no

    @property
    def departure_location(self):
        return self.__departure
    @property
    def destination_location(self):
        return self.__destination

class FlightInstance(Flight):
    def __init__(self, departure, destination, flight_no, flight_instance_no, departure_date, departure_time, destination_date, destination_time, airplane,gate):
        super().__init__(departure, destination, flight_no)
        self.__flight_instance_no = flight_instance_no
        self.__departure_date = departure_date
        self.__departure_time = departure_time
        self.__destination_date = destination_date
        self.__destination_time = destination_time
        self.__airplane = airplane
        self.__gate = gate
        self.__reserved_seat_list = []

    @property
    def flight_instance_no(self):
        return self.__flight_instance_no
     
    @property
    def departure(self):
        return self.__departure
    @property
    def destination(self):
        return self.__destination
    @property
    def flight_no(self):
        return self.__flight_no

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
    def add_reserved_seat(self,reserved_seat):
        self.reserved_seat_list.append(reserved_seat)

    def count_reserverd_seats(self):
        return len(self.__reserved_seat_list)

class Airplane:
    def __init__(self, airplane_id, total_seat):
        self.__airplane_id = airplane_id
        self.__total_seat = total_seat
        self.__seat_list = []

    @property
    def seat_list(self):
        return self.__seat_list
    @property
    def total_seat(self):
        return self.__total_seat

    def add_seat(self, seat):
        self.__seat_list.append(seat)

class Seat:
    def __init__(self,row,column,seat_type,price):
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

airplane1 = Airplane('001',6)
airplane2 = Airplane('002',6)
airplane3 = Airplane('003',6)

airport1 = Airport('Chaingmai')
airport2 = Airport('Bangkok')

user1 = User('kwai@gmail','00001')
user2 = User('kai@gmail','00002')

airplane1.add_seat(Seat("1","A","Hot Seat",1500))
airplane1.add_seat(Seat("1","B","Hot Seat",1500))
airplane1.add_seat(Seat("1","C","Hot Seat",1500,))
airplane1.add_seat(Seat("2","A","Standard Seat",1000))
airplane1.add_seat(Seat("2","B","Standard Seat",1000))
airplane1.add_seat(Seat("2","C","Standard Seat",1000))

airplane2.add_seat(Seat("1","A","Hot Seat",1500))
airplane2.add_seat(Seat("1","B","Hot Seat",1500))
airplane2.add_seat(Seat("1","C","Hot Seat",1500))
airplane2.add_seat(Seat("2","A","Standard Seat",1000))
airplane2.add_seat(Seat("2","B","Standard Seat",1000))
airplane2.add_seat(Seat("2","C","Standard Seat",1000))

controller.add_flight_instance_list(FlightInstance(airport1,airport2,"F00001","FI00001","25-02-2024","9:00","25-02-2024","10:20",airplane1,"1"))
controller.add_flight_instance_list(FlightInstance(airport1,airport2,"F00001","FI00002","25-02-2024","17:45","25-02-2024","19:05",airplane2,"2"))
controller.add_flight_instance_list(FlightInstance(airport1,airport2,"F00001","FI00003","25-02-2024","22:35","25-02-2024","23:55",airplane3,"3"))

# สร้าง ReservedSeat
controller.flight_instance_list[0].add_reserved_seat(ReservedSeat("1","A"))

print(controller.select_seat("FI00001"))

print("hi")
