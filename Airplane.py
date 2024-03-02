class Controller:
    def __init__(self, name):
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
            
    def search_flight(self, departure, destination, date, total_passenger, promocode):
        pass

    def add_admin(self, admin):
        self.__admin_list.append(admin)

    def select_seat(self, flight_instance_no):
        flight_instance = self.search_fight_instance_by_number(flight_instance_no)
        seat_list = flight_instance.airplane.seat_list
        reserved_seat_list = flight_instance.reserved_seat_list
        seat_detail = {}
        available_seat = []
        for seat in seat_list:
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

class Promocode:
    def __init__(self, code, genre, expire_date):
     self.__code = code
     self.__genre = genre
     self.__expire_date = expire_date


class Admin:
    def __init__(self, admin_id):
        self.__admin_id = admin_id

    def add_flight(self):
        pass

    def add_promocode(self):
        pass

class Guest:
    def __init__(self, guest_id):
        self.__guest_id = guest_id

class User(Guest):
    def __init__(self, email, user_id):
        self.__email = email
        self.__user_id = user_id
        self.__booking_list = []

class Booking:

    def __init__(self, booking_no, passenger_list, destination, departure, departure_date_time, arriving_date_time):
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

class Payment:
    def __init__(self, user_id, amount, transaction_id, payment_genre, payment_status):
        self.__user_id = user_id
        self.__amount = amount
        self.__transaction_id = transaction_id
        self.__payment_genre = payment_genre
        self.__payment_status = payment_status

class MobileBanking(Payment):
    def __init__ (self, account):
        self.__account = account
    
    def paid_by_mobilebanking(self):
        pass
    
class Card(Payment):
    def __init__ (self, card_no):
        self.__card_no = card_no

    def paid_by_card(self):
        pass

class CreditCard(Card):
    def __init__ (self, card_limit):
        self.__card_limit = card_limit

class DebitCard(Card):
    def __init__ (self, balance):
        self.__balance = balance   

class Passenger:
    def __init__(self, gender, tel_no, name, birth_date, citizen_id, boarding_pass):
        self.__gender = gender
        self.__tel_no = tel_no
        self.__name = name
        self.__birth_date = birth_date
        self.__citizen_id = citizen_id
        self.__boarding_pass = boarding_pass

class BoardingPass:
    def __init__(self, destination, departure, departure_date_time, arriving_date_time, gate, flight_no, luggage_list):
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
    def __init__(self, departure, destination, flight_no):
        self.__departure = departure
        self.__destination = destination
        self.__flight_no = flight_no

class FlightInstance(Flight):
    def __init__(self, departure, destination, flight_no, flight_instance_no, departure_date, departure_time, destination_date, destination_time, airplane, gate):
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
    def airplane(self):
        return self.__airplane
    
    @property
    def reserved_seat_list(self):
        return self.__reserved_seat_list
    
    def add_reserved_seat(self,reserved_seat):
        self.reserved_seat_list.append(reserved_seat)

class Airplane:
    def __init__(self, airplane_id, total_seat):
        self.__airplane_id = airplane_id
        self.__total_seat = total_seat
        self.__seat_list = []

    
    @property
    def seat_list(self):
        return self.__seat_list

    def add_seat(self, seat):
        self.__seat_list.append(seat)

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

airplane1 = Airplane('001', 6)
airplane2 = Airplane('002', 6)
airplane3 = Airplane('003', 6)

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