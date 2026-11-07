import psutil
from datetime import datetime

# ----------------------------------
# SYSTEM HEALTH CONFIGURATION
# ----------------------------------

WARNING_LIMIT = 80
CRITICAL_LIMIT = 90

LOG_FILE = "health_alerts.log"


# ----------------------------------
# CHECK RESOURCE STATUS
# ----------------------------------

def check_status(value):

    if value > CRITICAL_LIMIT:
        return "CRITICAL"

    elif value > WARNING_LIMIT:
        return "WARNING"

    else:
        return "HEALTHY"


# ----------------------------------
# SAVE ALERTS TO LOG FILE
# ----------------------------------

def save_alert(message):

    with open(LOG_FILE, "a") as file:
        file.write(message + "\n")


# ----------------------------------
# COLLECT SYSTEM INFORMATION
# ----------------------------------

def monitor_system():

    cpu_usage = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    ram_usage = memory.percent

    disk = psutil.disk_usage("/")
    disk_usage = disk.percent

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    resources = {
        "CPU": cpu_usage,
        "RAM": ram_usage,
        "DISK": disk_usage
    }

    print("\n====================================")
    print("        SYSTEM HEALTH REPORT")
    print("====================================")

    print(f"Date and Time: {current_time}")

    print("\nResource Usage:")

    alerts = []

    for name, value in resources.items():

        status = check_status(value)

        print(
            f"{name:<8}: {value:6.2f}% | {status}"
        )

        if status != "HEALTHY":

            message = (
                f"[{current_time}] "
                f"{name} usage is {value:.2f}% "
                f"- {status}"
            )

            alerts.append(message)

    print("\n====================================")
    print("          HEALTH SUMMARY")
    print("====================================")

    if alerts:

        for alert in alerts:
            print("ALERT:", alert)
            save_alert(alert)

        print("\nSystem requires attention.")

    else:
        print("All monitored resources are healthy.")

    print("\nHealth check completed.")


# ----------------------------------
# PROGRAM ENTRY POINT
# ----------------------------------

if __name__ == "__main__":

    try:
        monitor_system()

    except KeyboardInterrupt:
        print("\nHealth check stopped.")

    except Exception as error:
        print("An error occurred:", error)
