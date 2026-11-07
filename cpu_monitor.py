
import psutil
import time
from datetime import datetime

print("================================")
print("       CPU MONITORING SYSTEM")
print("================================")

# Get CPU core information
physical_cores = psutil.cpu_count(logical=False)
logical_cores = psutil.cpu_count(logical=True)

print(f"Physical CPU Cores: {physical_cores}")
print(f"Logical CPU Cores: {logical_cores}")

# Get CPU frequency
frequency = psutil.cpu_freq()

if frequency:
    print(f"CPU Frequency: {frequency.current:.2f} MHz")

print("\nStarting CPU monitoring...\n")

try:
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)

        current_time = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{current_time}] "
            f"CPU Usage: {cpu_usage}%"
        )

        time.sleep(1)

except KeyboardInterrupt:
    print("\nCPU Monitoring Stopped.")
