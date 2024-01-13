from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy_utils import create_database, database_exists
from datetime import datetime

Base = declarative_base()

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_type = Column(String, nullable=False)
    reservations = relationship('Reservation', back_populates='room')

class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    spa_package = Column(String)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    room = relationship('Room', back_populates='reservations')

class ReservationManager:
    def __init__(self, engine=None):
        self.engine = engine or create_engine('sqlite:///:memory:')
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def make_reservation(self, check_in, check_out, room_type, spa_package):
        check_in_date, check_out_date = self.convert_to_dates(check_in, check_out)

        room = self.get_or_create_room(room_type)

        reservation = Reservation(
            check_in=check_in_date,
            check_out=check_out_date,
            spa_package=spa_package,
            room=room
        )
        self.session.add(reservation)
        self.session.commit()

        self.display_reservations()
        print("\nReservation successful:")
        print(f"Room Type: {room_type}\nCheck-in: {check_in}\nCheck-out: {check_out}\nSpa Package: {spa_package}")

    def convert_to_dates(self, check_in, check_out):
        return datetime.strptime(check_in, '%Y-%m-%d').date(), datetime.strptime(check_out, '%Y-%m-%d').date()

    def get_or_create_room(self, room_type):
        room = self.session.query(Room).filter_by(room_type=room_type).first()
        if not room:
            room = Room(room_type=room_type)
            self.session.add(room)
        return room

    def display_reservations(self):
        reservations = self.session.query(Reservation).all()
        if reservations:
            print("\nExisting Reservations:")
            for res in reservations:
                print(f"Reservation ID: {res.id}, Room Type: {res.room.room_type}, Check-in: {res.check_in}, Check-out: {res.check_out}, Spa Package: {res.spa_package}")
        else:
            print("\nNo existing reservations.")