import string
from typing import List, Tuple


class SeatMap:
    def __init__(self, rows: int, cols: int):
        if rows < 1 or rows > 26 or cols < 1 or cols > 50:
            raise ValueError("Rows must be 1-26 and seats per row 1-50")
        self.rows = rows
        self.cols = cols
        self.grid = [[False] * cols for _ in range(rows)]

    def render(self, highlight: List[Tuple[int, int]] = None) -> None:
        """
        Render the current seat map to the console.
        - Empty seats are shown as '.'
        - Occupied seats are shown as '#'
        - Highlighted seats (currently selected in this booking) are shown as 'o'
        Example output:
            SCREEN
        -------------
        C . . . . .
        B . # o o .
        A . . # . .
          1 2 3 4 5
        :param highlight: A list of (row, col) tuples indicating seats to highlight (current selection).
                          Example: [(1, 2), (1, 3)] means seats B3 and B4 are highlighted.
        """
        highlight_set = set(highlight or [])
        print("Selected seats:\n")
        print("        SCREEN")
        print("-" * (self.cols * 2 + 3))
        for r in range(self.rows - 1, -1, -1):
            row_label = string.ascii_uppercase[r]  # 0 -> A, 1 -> 'B'
            chars = []
            for c in range(self.cols):
                if (r, c) in highlight_set:
                    chars.append("o")
                elif self.grid[r][c]:    # If the seat occupied
                    chars.append("#")
                else:
                    chars.append(".")
            print(f"{row_label} {' '.join(chars)}")
        col_nums = " ".join(str(i + 1) for i in range(self.cols))
        print(f"  {col_nums}\n")

    def free_count(self) -> int:
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.grid[r][c]:  # If the seat is free
                    count += 1
        return count

    def _find_intervals_in_row(self, row: int) -> List[Tuple[int, int]]:
        """
        Identify all contiguous empty seat intervals in the specified row.
        For example, if the row (where '.' = empty, '#' = occupied):
            . . # # . . . # . .
        (index) 0 1 2 3 4 5 6 7 8 9
        The function will return:
            [(0, 1), (4, 6), (8, 9)]
        Args:
            row (int): The row index to check.
        Returns:
            List[Tuple[int, int]]
        """
        intervals = []
        start = None
        for c in range(self.cols):
            if not self.grid[row][c]:
                if start is None:
                    start = c
            else:
                if start is not None:
                    intervals.append((start, c - 1))
                    start = None
        if start is not None:
            intervals.append((start, self.cols - 1))
        return intervals

    def _best_block_in_row(self, row: int, count: int) -> int:
        """
        Find the starting column index of the most centered contiguous block of empty seats
        that can accommodate 'count' seats in the specified row.
        This function looks at all empty intervals in the row
        and selects the block that is closest to the center of the row.
        Example:
            Suppose row has 10 seats (index 0-9) and looks like:
                . . # # . . . # . .
            Empty intervals from _find_intervals_in_row:
                [(0, 1), (4, 6), (8, 9)]
            If count = 2, the function will compute distance of possible blocks' centers to the row center (index 4.5),
            and choose the most centered one.
        Args:
            row (int): The row index to evaluate.
            count (int): The number of seats needed in the block.
        Returns:
            int: The starting column index of the chosen block.
        """
        mid = (self.cols - 1) / 2  # center position of the row (zero-indexed).
        best_start, best_dist = None, None

        for start, end in self._find_intervals_in_row(row):
            length = end - start + 1
            if length < count:
                continue
            # try each possible starting position within this interval
            for s in range(start, (end - count + 1) + 1):
                # calculates the center seat position of the block starting at s
                center = s + (count - 1) / 2
                # calculate the distance from the row's center
                dist = abs(center - mid)
                if best_start is None or dist < best_dist:
                    best_start, best_dist = s, dist
        if best_start is None:
            raise ValueError(f"No block of {count} seats free in row {row}")
        return best_start

    def allocate_default(self, num: int) -> List[Tuple[int, int]]:
        """
        - Start from the furthest row from the screen (row 0), and move forward.
        - In each row, try to find a contiguous block of seats as centered as possible.
        - If not enough seats in the current row, overflow to the next row.
        Args:
            num (int): Number of seats to allocate.
        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples for allocated seats.
        Example:
            suppose grid is 3x5 and empty, num=3:
            It will allocate 3 seats in row 0 (furthest from screen), centered as much as possible.
        """
        # defensive programming: make sure there are enough free seats
        if num > self.free_count():
            raise ValueError("Not enough seats")
        allocated = []
        remaining = num
        # Iterate over each row starting from the back (furthest from screen)
        for r in range(self.rows):
            if remaining <= 0:
                break
            free_seats_in_row = sum(1 for c in range(self.cols) if not self.grid[r][c])
            take = min(remaining, free_seats_in_row)
            if take <= 0:
                continue
            # Find the best (most centered) starting position for this block, Mark seats as taken and add them to the allocated list
            try:
                start = self._best_block_in_row(r, take)
            except ValueError:
                continue
            for c in range(start, start + take):
                self.grid[r][c] = True
                allocated.append((r, c))
            remaining -= take
        return allocated

    def allocate_custom(self, start_label: str, num: int) -> List[Tuple[int, int]]:
        """
        Allocate seats starting from the specified position, filling to the right,
        and overflow into rows closer to the screen if necessary.
        Example:
            Suppose the seating grid is 3 rows (A=0, B=1, C=2) and 5 seats per row:
            . . . . .    <- A (row 0)
            . . . . .    <- B (row 1)
            . . . . .    <- C (row 2)
            If user inputs start_label = 'B03' and num = 4:
            - Seats allocated: B03 B04 B05
            - Then overflow to C: C03 (or center-most 4-block if needed)
        Args:
            start_label (str): The starting seat label, e.g. 'B03'.
            num (int): The number of seats to allocate.
        Returns:
            List[Tuple[int, int]]: List of (row_index, col_index) for allocated seats.
        """
        # Parse row and column from label
        r = string.ascii_uppercase.index(start_label[0])  # e.g. 'B' -> 1
        c = int(start_label[1:]) - 1  # e.g. '03' -> 2 (0-indexed)

        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            raise ValueError(f"Invalid start position '{start_label}'")

        allocated = []
        remaining = num

        # 1. Fill in current row from start column to the right
        for cc in range(c, self.cols):
            if remaining == 0:
                break
            if not self.grid[r][cc]:
                self.grid[r][cc] = True
                allocated.append((r, cc))
                remaining -= 1

        # 2. If not enough seats, overflow into next rows (closer to screen)
        if remaining > 0:
            for rr in range(r + 1, self.rows):
                if remaining == 0:
                    break
                # count how many free seats in this row
                free = sum(1 for cc in range(self.cols) if not self.grid[rr][cc])
                take = min(remaining, free)
                if take <= 0:
                    continue
                # Find best block in this row
                try:
                    start2 = self._best_block_in_row(rr, take)
                except ValueError:
                    continue
                for cc in range(start2, start2 + take):
                    self.grid[rr][cc] = True
                    allocated.append((rr, cc))
                remaining -= take

        return allocated


