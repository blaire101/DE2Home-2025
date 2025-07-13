# tests/conftest.py

import pytest


from cinema.seatmap import SeatMap


@pytest.fixture
def small_map():
    return SeatMap(rows=4, cols=5)