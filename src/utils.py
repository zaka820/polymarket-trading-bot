# Utility Helper Functions

from datetime import datetime


def get_current_time():
    """
    Returns the current UTC date and time in the
    format of 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def add(a, b):
    """
    Returns the sum of a and b.
    """  
    return a + b


def subtract(a, b):
    """
    Returns the difference of a and b.
    """  
    return a - b


# Additional utility functions can be added here...