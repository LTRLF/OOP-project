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

    def search_flight_instance_by_number(self, number):
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

    def add_user(self, user):
        self.__user_list.append(user)

    def select_seat(self, flight_instance_no):
        flight_instance = self.search_flight_instance_by_number(flight_instance_no)
        seat_list = flight_instance.airplane.seat_list
        reserved_seat_list = flight_instance.reserved_seat_list
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
        if len(user_id) == 5 and type(user_id) == str:
            for user in self.__user_list:
                if user.user_id == user_id:
                    return user
        else:
            return "Error"

    def search_flight_instance_by_flight_instance_no(self, flight_instance_no):
        if len(flight_instance_no) == 7 and type(flight_instance_no) == str:
            for flight_instance in self.__flight_instance_list:
                if flight_instance.flight_instance_no == flight_instance_no:
                    return flight_instance
        else:
            return "Error"
            
    def fill_info_and_select_package(self, user_id, flight_no, gender, tel_no, name, birth_date, citizen_id, package = None):
        flight = self.search_flight_instance_by_flight_instance_no(flight_no)
        user = self.search_user_by_user_id(user_id)
        booking = Booking(Booking.booking_no, flight.destination, flight.departure, flight.departure_date, flight.departure_time, flight.destination_date, flight.destination_time)
        Booking.booking_number += 1
        passenger = Passenger(gender, tel_no, name, birth_date, citizen_id)
        boardingpass = Boardingpass(flight.destination, flight.departure, flight.departure_date, flight.departure_time, flight.destination_date, flight.destination_time, flight.gate, flight.flight_no)

        if package != None:
            luggage = Luggage(package, Luggage.luggage_id)
            Luggage.luggage_number += 1
            boardingpass.add_luggage(luggage)
    
        passenger.add_boardingpass(boardingpass)
        booking.add_passenger(passenger)
        user.add_booking(booking)
        return booking

    def pay_for_ticket(self, user_id, booking_no, citizen_id, row, column):
        # controller1 = Controller('Earn')
        # booking1 = Booking('B00001', 'Chaingmai', 'Bangkok', '18-01-24', '21-01-24', '07.30', '08.45')
        # user1 = User('kwai@gmail','00001')
        # controller1.add_user(user1)
        # boarding_pass1 = Boardingpass('Chaingmai', 'Bangkok', '18-01-24', '21-01-24', '07.30', '08.45', 'gateB', 'FI00001', '1', 'C')
        # passenger1 = Passenger('Male', '0123456789', 'David', '18-01-99', '1100012345001', boarding_pass1)
        # booking1.add_passenger(passenger1) 
        # user1.add_booking(booking1)
        # seat3 = Seat("1","C","Hot Seat",1500)
        # boarding_pass1.add_seat_list(seat3)
        
        user = controller1.search_user_by_user_id(user_id)
        booking = user.search_booking_by_number(booking_no)
        passenger = booking.search_passenger_by_citizen_id(citizen_id)
        boarding_pass = passenger.boarding_pass
        seat = boarding_pass.search_seat_by_row_column(row, column)
        price = seat.price
        print(price)
        trans1 = Transaction(booking1, 1500, MobileBanking)
        print(trans1.show_payment())

    
    @property
    def flight_instance_list(self):
        return self.__flight_instance_list

class Admin:
    def __init__(self, admin_id):
        self.__admin_id = admin_id

    # def add_flight_instance(self, flight_instance):
    #     Controller.add_flight_instance_by_controller(flight_instance)

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
        return booking_info_list

    @property
    def user_id(self):
        return self.__user_id

    def add_booking(self, booking):
        self.__booking_list.append(booking)

    def search_booking_by_number(self, booking_number):
        for booking in self.__booking_list:
            if isinstance(booking, Booking) and booking_number == booking.booking_no:
                return booking

class Promocode:
    promocode_list = []

    def __init__(self, code, type, expire_date):
        self.__code = code
        self.__type = type
        self.__expire_date = expire_date
        Promocode.promocode_list.append(self)
     
    @property
    def promocode_no(self):
        return self.__code
    # def check_promocode(self, input_code):
    #     if input_code == self.__code:
    #         return True

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

    def add_passenger(self, passenger):
        if isinstance(passenger, Passenger):
            self.__passenger_list.append(passenger)

    def search_passenger_by_citizen_id(self, citizen_id):
        for passenger in self.__passenger_list:
            if citizen_id == passenger.citizen_id:
                return passenger

class Payment:
    def __init__(self, user_id, amount, transaction_id, payment_type, payment_status):
        self.__user_id = user_id
        self.__amount = amount
        self.__transaction_id = transaction_id
        self.__payment_type = payment_type
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
                "status": True
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
    def boarding_pass(self):
        return self.__boarding_pass

    @property 
    def citizen_id(self):
        return self.__citizen_id

class Boardingpass:
    def __init__(self, destination, departure, departure_date, departure_time, destination_date, destination_time, gate, flight_no, row, column):
        self.__destination = destination
        self.__departure = departure
        self.__departure_date = departure_date
        self.__departure_time = departure_time
        self.__destination_date = destination_date
        self.__destination_time = destination_time
        self.__gate = gate
        self.__flight_no = flight_no
        self.__row = row
        self.__column = column
        self.__seat_list = []
        self.__luggage_list = []
        self.__show_seat = None
    
    def set_showseat(self, seat):
        self.__show_seat = seat

    def search_seat_by_row_column(self, row, column):
        for seat in self.__seat_list:
            if seat.row == row and seat.column == column:
                return seat
                
    def add_luggage(self, luggage):
        self.__luggage_list.append(luggage)
        
    def add_seat_list(self, seat):
        if isinstance(seat, Seat):
            self.__seat_list.append(seat)

    @property
    def row(self):
        return self.__row

    @property
    def column(self):
        return self.__column

class Luggage:
    luggage_number = 1
    def __init__(self, package, luggage_id):
        self.__owner = None
        self.__package = package
        self.__luggage_id = luggage_id

    def set_owner(self, owner):
        self.__owner = owner

    def luggage_id(self):
        return self.__luggage_id

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
        self.__reserved_seat_list = []

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
    def add_reserved_seat(self, reserved_seat):
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
    
class Test:
    def __init__(self):
        pass


    
controller = Controller('AirAsia')

airplane1 = Airplane('001', 6)
airplane2 = Airplane('002', 6)
airplane3 = Airplane('003', 6)

airport1 = Airport('Chaingmai')
airport2 = Airport('Bangkok')

user1 = User('kwai@gmail', '00001')
user2 = User('kai@gmail', '00002')

admin1 = Admin('A')

airplane1.add_seat(Seat("1", "A", "Hot Seat", 1500))
airplane1.add_seat(Seat("1", "B", "Hot Seat", 1500))
airplane1.add_seat(Seat("1", "C", "Hot Seat", 1500, ))
airplane1.add_seat(Seat("2", "A", "Standard Seat", 1000))
airplane1.add_seat(Seat("2", "B", "Standard Seat", 1000))
airplane1.add_seat(Seat("2", "C", "Standard Seat", 1000))

airplane2.add_seat(Seat("1", "A", "Hot Seat", 1500))
airplane2.add_seat(Seat("1", "B", "Hot Seat", 1500))
airplane2.add_seat(Seat("1", "C", "Hot Seat", 1500))
airplane2.add_seat(Seat("2", "A", "Standard Seat", 1000))
airplane2.add_seat(Seat("2", "B", "Standard Seat", 1000))
airplane2.add_seat(Seat("2", "C", "Standard Seat", 1000))

controller.add_admin(admin1)
controller.add_user(user1)
controller.add_flight_instance_list(Flight_instance(airport1, airport2, "F00001", "FI00001", "25-02-2024", "9:00", "25-02-2024", "10:20", airplane1, "1"))
controller.add_flight_instance_list(Flight_instance(airport2, airport1, "F00001", "FI00002", "25-02-2024", "17:45", "25-02-2024", "19:05", airplane2, "2"))
controller.add_flight_instance_list(Flight_instance(airport1, airport2, "F00001", "FI00003", "25-02-2024", "22:35", "25-02-2024", "23:55", airplane3, "3"))

trans1 = Transaction(booking1, 1500, MobileBanking)
trans2 = Transaction(booking2, 2000, Card)


#TODO fill_info testcase
#temp = controller.fill_info_and_select_package('00001', 'FI00003', 'male', '0980111111', 'mark', '01/10/20', '19090021434941', 'big')
#print(temp.destination.name)

#TODO promocode testcase
#admin1.add_promocode('little')
#print(Promocode.promocode_list)

#TODO ReservedSeat testcase
#controller.flight_instance_list[0].add_reserved_seat(ReservedSeat("1", "A"))
#print(controller.select_seat("FI00001"))

#TODO view_account_detail
# controller.fill_info_and_select_package('00001', 'FI00003', 'male', '0980111111', 'mark', '01/10/20', '19090021434941', 'big')
# controller.fill_info_and_select_package('00001', 'FI00003', 'male', '0980111111', 'mark', '01/10/20', '19090021434941', 'big')
# print(user1.view_account_detail())

#TODO show_payment
# print(trans1.show_payment())
# print(trans2.show_payment())

#TODO pay_for_ticket
#print(controller.pay_for_ticket('00001', 'B00001', '1100012345001', '1', 'C'))
