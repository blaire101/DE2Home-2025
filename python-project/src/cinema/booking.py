from typing import List, Tuple


class Booking:
    def __init__(self, booking_id: str, seats: List[Tuple[int,int]]):
        self.id = booking_id
        self.seats = seats







# Define a list of seat coordinates (row, col), zero-based index:
# (1, 2) → row 0 (B), column 2 → seat B03, etc.

# seats: List[Tuple[int, int]] = [
#     (1, 2),  # B03
#     (1, 3),  # B04
#     (1, 4),  # B05
#     (1, 5),  # B06
# ]
#
# # Create a Booking instance with ID "GC0001" and the above seats
# booking = Booking("GC0001", seats)
#
# # You can then inspect:
# print(booking.id)     # → GC0001
# print(booking.seats)  # → [(1, 2), (1, 3), (1, 4), (1, 5)]
