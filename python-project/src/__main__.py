# src/__main__.py
import logging
from config import setup_logging
from cinema.system import CinemaBookingSystem
import sys


def main():
    setup_logging()

    # Prompt and log the raw header input
    header = input(
        "Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n> "
    )
    logging.info(f"Received header input: {header}")

    parts = header.split()
    # Validate: exactly 3 parts, title, rows and cols integers in 1–26 / 1–50
    try:
        if len(parts) != 3:
            raise ValueError
        title = parts[0]
        rows = int(parts[1])
        cols = int(parts[2])
        if not (1 <= rows <= 26 and 1 <= cols <= 50):
            raise ValueError
    except ValueError:
        logging.error(f"Invalid header format: {header}")
        print(
            "Invalid input. Expected format: Title Rows SeatsPerRow (Rows 1–26, SeatsPerRow 1–50)"
        )
        sys.exit(1)

    logging.info(f"Initializing system with title={title}, rows={rows}, cols={cols}")
    system = CinemaBookingSystem(title, rows, cols)
    system.run()


main()
