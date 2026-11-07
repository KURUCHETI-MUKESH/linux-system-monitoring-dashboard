import psutil
import time
from datetime import datetime

print("====================================")
print("         DISK MONITORING SYSTEM")
print("====================================")

# Get disk information
disk = psutil.disk_usage('/')

# Convert bytes into GB
total_disk = disk.total / (1024 ** 3)
used_disk = disk.used / (1024 ** 3)
free_disk = disk.free / (1024 ** 3)

print(f"Total Disk Space: {total_disk:.2f} GB")
print(f"Used Disk Space:  {used_disk:.2f} GB")
print(f"Free Disk Space:  {free_disk:.2f} GB")

print("\nStarting disk monitoring...\n")

try:
    while True:

        # Get latest disk information
        disk = psutil.disk_usage('/')

        total = disk.total / (1024 ** 3)
        used = disk.used / (1024 ** 3)
        free = disk.free / (1024 ** 3)

        usage_percent = disk.percent

        # Get system uptime
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time

        # Convert uptime into hours
        uptime_hours = uptime_seconds / 3600

        current_time = datetime.now().strftime("%H:%M:%S")

        print(f"[{current_time}]")
        print(f"Total Disk: {total:.2f} GB")
        print(f"Used Disk: {used:.2f} GB")
        print(f"Free Disk: {free:.2f} GB")
        print(f"Disk Usage: {usage_percent:.2f}%")
        print(f"System Uptime: {uptime_hours:.2f} hours")

        # Check disk usage
        if usage_percent > 80:
            print("WARNING: Disk space is running low!")

        print("------------------------------------")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nDisk Monitoring Stopped.")
