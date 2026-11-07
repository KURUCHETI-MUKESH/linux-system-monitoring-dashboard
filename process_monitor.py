import psutil
import time
from datetime import datetime

print("========================================")
print("          PROCESS MONITORING SYSTEM")
print("========================================")

try:
    while True:

        # Get all running processes
        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "username", "status", "memory_percent"]
        ):
            try:
                process_info = process.info

                processes.append({
                    "pid": process_info["pid"],
                    "name": process_info["name"] or "Unknown",
                    "username": process_info["username"] or "Unknown",
                    "status": process_info["status"] or "Unknown",
                    "memory": process_info["memory_percent"] or 0
                })

            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                continue

        # Sort processes by memory usage
        processes.sort(
            key=lambda x: x["memory"],
            reverse=True
        )

        # Display current time
        current_time = datetime.now().strftime("%H:%M:%S")

        print("\n========================================")
        print(f"Time: {current_time}")
        print(f"Total Processes: {len(processes)}")
        print("========================================")

        print(
            f"{'PID':<10}"
            f"{'PROCESS NAME':<22}"
            f"{'STATUS':<15}"
            f"{'MEMORY %':<10}"
        )

        print("-" * 57)

        # Display top 10 memory-consuming processes
        for process in processes[:10]:

            print(
                f"{process['pid']:<10}"
                f"{process['name'][:20]:<22}"
                f"{process['status']:<15}"
                f"{process['memory']:.2f}%"
            )

        print("\nRefreshing in 5 seconds...")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nProcess Monitoring Stopped.")
