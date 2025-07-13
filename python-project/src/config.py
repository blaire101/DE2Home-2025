import logging
import os


def setup_logging():
    """
    Configure logging for the Cinema Booking System:
    - Logs are written to ``<project_root>/logs/booking.log``
    """
    # Determine project root (parent of src/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(base_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, 'booking.log')

    handlers = [
        logging.FileHandler(log_path),
        logging.StreamHandler(),
    ]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=handlers,
    )
