import psutil
import time
from datetime import datetime

print("====================================")
print("       MEMORY MONITORING SYSTEM")
print("====================================")

# Get total memory information
memory = psutil.virtual_memory()

total_ram = memory.total / (1024 ** 3)

print(f"Total RAM: {total_ram:.2f} GB")
print("\nStarting memory monitoring...\n")

try:
    while True:
        # Get the latest memory information
        memory = psutil.virtual_memory()

        # Convert bytes into GB
        total = memory.total / (1024 ** 3)
        used = memory.used / (1024 ** 3)
        available = memory.available / (1024 ** 3)

        # Get memory usage percentage
        usage_percent = memory.percent

        # Get current time
        current_time = datetime.now().strftime("%H:%M:%S")

        # Display memory information
        print(f"[{current_time}]")
        print(f"Total RAM:     {total:.2f} GB")
        print(f"Used RAM:      {used:.2f} GB")
        print(f"Available RAM: {available:.2f} GB")
        print(f"RAM Usage:     {usage_percent:.2f}%")

        # Check memory usage
        if usage_percent > 80:
            print("WARNING: High RAM usage!")

        print("------------------------------------")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nMemory Monitoring Stopped.")
