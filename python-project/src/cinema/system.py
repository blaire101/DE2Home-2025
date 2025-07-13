import logging
from cinema.seatmap import SeatMap
from cinema.manager import BookingManager

logger = logging.getLogger(__name__)


class CinemaBookingSystem:
    def __init__(self, title: str, rows: int, cols: int):
        self.title = title
        self.map = SeatMap(rows, cols)
        self.manager = BookingManager()

    def run(self) -> None:
        while True:
            avail = self.map.free_count()
            print()
            print(f"Welcome to GC Cinemas")
            print(f"[1] Book tickets for {self.title} ({avail} seats available)")
            print(f"[2] Check bookings")
            print(f"[3] Exit")
            choice = input("Please enter your selection:\n> ").strip()
            if choice == '1':
                self.book_flow()
            elif choice == '2':
                self.check_flow()
            elif choice == '3':
                print("\nThank you for using GC Cinemas system. Bye!")
                logger.info(f"Thank you for using GC Cinemas system. Bye!")
                break
            else:
                print("\nInvalid selection. Please enter 1, 2, or 3.")
                continue

    def book_flow(self) -> None:
        while True:
            val = input("\nEnter number of tickets to book, or enter blank to go back to main menu:\n> ").strip()
            if val == '':
                return
            num = int(val)
            if num > self.map.free_count():
                print(f"\nSorry, there are only {self.map.free_count()} seats available.")
            else:
                break

        allocated = self.map.allocate_default(num)
        bid = self.manager.add(seats=allocated)

        print(f"\nSuccessfully reserved {num} {self.title} tickets.")
        print(f"Booking id: {bid}")
        self.map.render(highlight=allocated)

        while True:
            pos = input("Enter blank to accept seat selection, or enter new seating position:\n> ").strip()
            if pos == '':
                print(f"\nBooking id: {bid} confirmed.")
                return
            # reset allocated seats before custom
            for r, c in allocated:
                self.map.grid[r][c] = False
            allocated = self.map.allocate_custom(pos, num)
            # update booking record
            booking = self.manager.get(bid)
            booking.seats = allocated
            print(f"\nBooking id: {bid}")
            self.map.render(highlight=allocated)
        logger.info(f"Booking {bid}: {allocated}")

    def check_flow(self) -> None:
        while True:
            bid = input("\nEnter booking id, or enter blank to go back to main menu:\n> ").strip()
            if bid == '':
                return
            booking = self.manager.get(bid)
            if not booking:
                print("\nBooking id not found.")
            else:
                print(f"\nBooking id: {bid}")
                self.map.render(highlight=booking.seats)
