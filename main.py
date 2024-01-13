import click
from Manager.reservation_manager import ReservationManager, Base
from sqlalchemy import create_engine

@click.command()
@click.option('--check-in', prompt='Check-in date (YYYY-MM-DD)', help='Check-in date')
@click.option('--check-out', prompt='Check-out date (YYYY-MM-DD)', help='Check-out date')
@click.option('--room-type', prompt='Room type', help='Type of room')
@click.option('--spa-package', prompt='Spa package', help='Spa package')
@click.option('--database-url', default='sqlite:///reservations.db', help='Database URL')
def main(check_in, check_out, room_type, spa_package, database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    reservation_manager = ReservationManager(engine)
    reservation_manager.make_reservation(check_in, check_out, room_type, spa_package)

if __name__ == '__main__':
    main()