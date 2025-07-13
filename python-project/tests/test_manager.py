from cinema.manager import BookingManager


def test_booking_id_increment():
    mgr = BookingManager()
    id1 = mgr.new_id()
    id2 = mgr.new_id()
    assert id1.startswith('GIC') and id2.startswith('GIC')
    assert int(id2[3:]) == int(id1[3:]) + 1