"""Can be used to measure average execution time of
parse_and_print() function. The function is imported
from a selected module.
"""

from importlib import import_module
import numpy as np
import time
from typing import Callable


def execution_time(function: Callable, args=tuple(), kwargs=dict()):
    """Measure execution time in seconds. If the function has arguments
    they should be provided in args and kwargs parameters.
    """
    start_time = time.time()
    function(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time


if __name__ == "__main__":
    module_name = input("Enter the name of the module to test: ")
    try:
        module = import_module(module_name)
    except ImportError:
        print(f"Couldn't import '{module_name}' module")
        exit()
    time_logs = [execution_time(module.parse_and_print) for i in range(100)]
    print(*map("--- {} seconds ---".format, time_logs), sep="\n")
    print(f"=== {np.array(time_logs).mean()} seconds ===")
