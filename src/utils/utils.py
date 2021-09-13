import time


def set_start_time(time: float):
    """
    Sets global startup_time to the inputted time.
    """
    global startup_time
    startup_time = time


def get_uptime() -> float:
    """
    Returns uptime in seconds.
    """
    return time.perf_counter() - startup_time
