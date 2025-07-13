from cinema.seatmap import SeatMap


def test_free_count_initial(small_map):
    assert small_map.free_count() == 20


def test_allocate_default_centered():
    sm = SeatMap(3, 5)
    seats = sm.allocate_default(3)
    # should pick middle row, middle columns: row 0 -> A
    assert len(seats) == 3
    assert sm.free_count() == 12


def test_allocate_custom_overflow():
    sm = SeatMap(2, 3)
    # fill first row completely
    sm.allocate_custom('A01', 3)    # A01 -> (0,0), A02 -> (0,1), A03 -> (0,2)

    # now custom in B w
    seats = sm.allocate_custom('B02', 3)   # only two seats allocated in row B ：  (1, 1), (1, 2)
    assert len(seats) == 2
    assert seats == [(1, 1), (1, 2)]


