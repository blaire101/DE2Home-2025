from cinema.system import CinemaBookingSystem


def test_init_cinema_booking_system():
    # Simple initialization test
    cinema = CinemaBookingSystem("Inception", 2, 3)
    assert cinema.title == "Inception"
    assert cinema.map.rows == 2
    assert cinema.map.cols == 3
    # free_count should equal total seats initially
    assert cinema.map.free_count() == 2 * 3
