class Controller:
    def __init__(self,name):
        self.__name=name
        self.__user_list = []
        self.__guest_list = []
        self.__promocode_list = []
        self.__flight_list = []
        self.__flightinstance_list = []
        self.__admin_list = []
        self.__airport_list = []

    def search_flight(self,departure,destination,date,total_passenger,promocode = None):
        pass

    def add_admin(self,admin):
        self.__admin_list.append(admin)

    def add_flight_instance_list(self,flight_instance):
        self.__flightinstance_list.append(flight_instance)
    
    def add_user(self,user):
        self.__user_list.append(user)
    
    def search_user_by_user_id(self,user_id):
        for user in self.__user_list:
            if user.user_id == user_id:
                return user

    def search_flightinstance_by_flightinstance_no(self,flightinstance_no):
        for flightinstance in self.__flightinstance_list:
            if flightinstance.flight_instance_no == flightinstance_no:
                return flightinstance
            
    def fill_info_and_select_package(self,user_id,flight_no, gender, tel_no, name, birth_date, citizen_id, package = None):
        flight = self.search_flightinstance_by_flightinstance_no(flight_no)
        user = self.search_user_by_user_id(user_id)
        booking = Booking(Booking.booking_no, flight.destination, flight.departure, flight.departure_date, flight.departure_time, flight.destination_date, flight.destination_time)
        passenger = Passenger(gender, tel_no, name, birth_date, citizen_id)
        boardingpass = Boardingpass(flight.destination, flight.departure, flight.departure_date, flight.departure_time, flight.destination_date, flight.destination_time, flight.gate, flight.flight_no)

        if package != None:
            luggage = Luggage(package, Luggage.luggage_id)
            Luggage.luggage_id += 1
            boardingpass.add_luggage(luggage)
    
        passenger.add_boardingpass(boardingpass)
        booking.add_passenger(passenger)
        user.add_booking(booking)
        return booking
    
            
            
            

class Promocode:

    def __init__(self,code,discount):
        self.__code = code
        self.__discount = discount 
        self.__exprire_date = None


class Admin:
    def __init__(self,admin_id):
        self.__admin_id = admin_id

    def add_flight(self):
        pass
    def add_promocode(self):
        pass

class Guest:
    def __init__(self,guest_id):
        self.__guest_id = guest_id

class User(Guest):
    def __init__(self,email,user_id):
        self.__email = email
        self.__user_id = user_id
        self.__booking_list = []
    
    @property
    def user_id(self):
        return self.__user_id

    def add_booking(self,booking):
        self.__booking_list.append(booking)


class Booking:
    booking_no = 0
    def __init__(self,booking_no,destination,departure,departure_date,departure_time,arriving_date,arriving_time):
        self.__booking_no = Booking.booking_no
        self.__passenger_list = []
        self.__destination = destination
        self.__departure = departure
        self.__departure_date = departure_date
        self.__departure_time = departure_time
        self.__arriving_date = arriving_date
        self.__arriving_time = arriving_time
        self.__booking_status = None
        self.__payment = None 
    @property
    def booking_no(self):
        return self.__booking_no

    @property
    def passenger_list(self):
        return self.__passenger_list

    @property
    def destination(self):
        return self.__destination

    @property
    def departure(self):
        return self.__departure


    def update_booking_status(self):
        pass
    
    def update_payment(self):
        pass

    def add_passenger(self,passenger):
        self.__passenger_list.append(passenger)

class Payment:
    def __init__(self,user_id,amount,transaction_id,payment_genre,payment_status):
        self.__user_id = user_id
        self.__amount = amount
        self.__transaction_id = transaction_id
        self.__payment_genre = payment_genre
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
    def __init__(self,gender,tel_no,name,birth_date,citizen_id):
        self.__gender = gender
        self.__tel_no = tel_no
        self.__name = name
        self.__birth_date = birth_date
        self.__citizen_id = citizen_id
        self.__boardingpass = None

    def add_boardingpass(self,boardingpass):
        self.__boardingpass = boardingpass

class Boardingpass:
    def __init__(self,destination,departure,departure_date,departure_time,destination_date,destination_time,gate,flight_no):
        self.__destination = destination
        self.__departure = departure
        self.__departure_date = departure_date
        self.__departure_time = departure_time
        self.__destination_date = destination_date
        self.__destination_time = destination_time
        self.__gate = gate
        self.__flight_no = flight_no
        self.__luggage_list = []
        self.__show_seat = None
    
    def set_showseat(self,seat):
        self.__show_seat = seat

    def add_luggage(self,luggage):
        self.__luggage_list.append(luggage)


class Luggage:
    luggage_id = 1
    def __init__(self,package,luggage_id):
        self.__owner = None
        self.__package = package
        self.__luggage_id = luggage_id

    def set_owner(self,owner):
        self.__owner = owner
    
class Airport:
    def __init__(self,name):
        self.__name = name
        self.__current_airplane_list = []

    def get_current_airplane(self):
        return self.__current_airplane_list
    
    @property
    def name(self):
        return self.__name

class Flight:
    def __init__(self,departure,destination,flight_no):
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

class FlightInstance(Flight):
    def __init__(self,departure,destination,flight_no,flight_instance_no,departure_date,departure_time,destination_date,destination_time,airplane,gate):
        super().__init__(departure,destination,flight_no)
        self.__flight_instance_no = flight_instance_no
        self.__departure_date = departure_date
        self.__departure_time = departure_time
        self.__destination_date = destination_date
        self.__destination_time = destination_time
        self.__airplane = airplane
        self.__gate = gate
        self.__show_seat_list = []
        


    @property
    def flight_instance_no(self):
        return self.__flight_instance_no

    @property
    def departure_date(self):
        return self.__departure_date

    @property
    def departure_time(self):
        return self.__departure_time

    @property
    def destination_date(self):
        return self.__destination_date
    
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
    def show_seat_list(self):
        return self.__show_seat_list

class Airplane:
    def __init__(self,airplane_id,total_seat):
        self.__airplane_id = airplane_id
        self.__total_seat = total_seat
        self.__seat_list = []
    
    def add_seat(self,seat):
        self.__seat_list = seat
    
    @property
    def total_seat(self):
     return self.__total_seat

class Seat:
    def __init__(self,row,column,seat_genre,price):
        self.__row = row
        self.__column = column
        self.__seat_genre = seat_genre
        self.__price = price
        
class ShowSeat(Seat):
    def __init__(self,row,column,seat_genre,price):
        super().__init__(row,column,seat_genre,price)
        self.__is_available = True

controller = Controller('Airasia')



airplane1 = Airplane('001',60)
airplane2 = Airplane('002',100)
airplane3 = Airplane('003',200)

airport1 = Airport('Chaingmai')
airport2 = Airport('Bangkok')

user1 = User('1@gmail','00001')
user2 = User('2@gmail','00002')

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

controller.add_user(user1)
controller.add_flight_instance_list(FlightInstance(airport1,airport2,"F00001","FI00001","25-02-2024","9:00","25-02-2024","10:20",airplane1,"1"))
controller.add_flight_instance_list(FlightInstance(airport1,airport2,"F00001","FI00002","25-02-2024","17:45","25-02-2024","19:05",airplane2,"2"))
controller.add_flight_instance_list(FlightInstance(airport1,airport2,"F00001","FI00003","25-02-2024","22:35","25-02-2024","23:55",airplane3,"3"))

temp = controller.fill_info_and_select_package('00001','FI00001','male','0980111111','mark','01/10/20','19090021434941','big')
print(temp.departure.name)

