from typing import Dict
from cinema.booking import Booking


class BookingManager:
    def __init__(self):
        self._counter = 0
        self._bookings: Dict[str, Booking] = {}

    def new_id(self) -> str:
        self._counter += 1
        return f"GC{self._counter:04d}"  # Pad with zeros on the left (zero-fill)

    def add(self, seats) -> str:
        bid = self.new_id()
        self._bookings[bid] = Booking(bid, seats)
        return bid

    def get(self, booking_id: str) -> Booking:
        return self._bookings.get(booking_id)
