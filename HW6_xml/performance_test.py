import time
import numpy as np
from xmlparser import main


time_logs = []
for i in range(10):
    start_time = time.time()
    main()
    time_logs.append(time.time() - start_time)
for exec_time in time_logs:
    print(f"--- {exec_time} seconds ---")
print(f"=== {np.array(time_logs).mean()} seconds ===")
