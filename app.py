import streamlit as st
import psutil
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Linux System Monitor",
    page_icon="🖥️",
    layout="wide"
)

# ----------------------------------
# CUSTOM DASHBOARD TITLE
# ----------------------------------

st.title("🖥️ Linux System Monitoring Dashboard")

st.write(
    "Monitor CPU, RAM, disk usage, system uptime "
    "and running processes."
)

st.caption(
    f"Last updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

# ----------------------------------
# REFRESH BUTTON
# ----------------------------------

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

# ----------------------------------
# COLLECT SYSTEM INFORMATION
# ----------------------------------

cpu_usage = psutil.cpu_percent(interval=0.5)

memory = psutil.virtual_memory()

total_ram = memory.total / (1024 ** 3)
used_ram = memory.used / (1024 ** 3)
available_ram = memory.available / (1024 ** 3)
ram_percent = memory.percent

disk = psutil.disk_usage("/")

total_disk = disk.total / (1024 ** 3)
used_disk = disk.used / (1024 ** 3)
free_disk = disk.free / (1024 ** 3)
disk_percent = disk.percent

boot_time = psutil.boot_time()
uptime_seconds = time.time() - boot_time

days = int(uptime_seconds // 86400)
hours = int((uptime_seconds % 86400) // 3600)
minutes = int((uptime_seconds % 3600) // 60)

uptime = f"{days} days, {hours} hours, {minutes} minutes"

# ----------------------------------
# SYSTEM OVERVIEW
# ----------------------------------

st.header("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "CPU Usage",
    f"{cpu_usage:.1f}%"
)

col2.metric(
    "RAM Usage",
    f"{ram_percent:.1f}%",
    f"{used_ram:.2f} GB used"
)

col3.metric(
    "Disk Usage",
    f"{disk_percent:.1f}%",
    f"{used_disk:.2f} GB used"
)

col4.metric(
    "System Uptime",
    uptime
)

# ----------------------------------
# MEMORY INFORMATION
# ----------------------------------

st.divider()

st.header("🧠 RAM Monitoring")

ram_col1, ram_col2 = st.columns(2)

with ram_col1:
    st.write(f"Total RAM: {total_ram:.2f} GB")
    st.write(f"Used RAM: {used_ram:.2f} GB")
    st.write(f"Available RAM: {available_ram:.2f} GB")

    if ram_percent > 80:
        st.warning("High RAM usage detected!")
    else:
        st.success("RAM usage is normal.")

with ram_col2:
    ram_data = pd.DataFrame({
        "Memory": ["Used", "Available"],
        "Size": [used_ram, available_ram]
    })

    ram_chart = px.pie(
        ram_data,
        names="Memory",
        values="Size",
        title="RAM Distribution",
        hole=0.5
    )

    st.plotly_chart(ram_chart, use_container_width=True)

# ----------------------------------
# DISK INFORMATION
# ----------------------------------

st.divider()

st.header("💾 Disk Monitoring")

disk_col1, disk_col2 = st.columns(2)

with disk_col1:
    st.write(f"Total Disk: {total_disk:.2f} GB")
    st.write(f"Used Disk: {used_disk:.2f} GB")
    st.write(f"Free Disk: {free_disk:.2f} GB")

    if disk_percent > 80:
        st.warning("Disk space is running low!")
    else:
        st.success("Disk usage is normal.")

with disk_col2:
    disk_data = pd.DataFrame({
        "Storage": ["Used", "Free"],
        "Size": [used_disk, free_disk]
    })

    disk_chart = px.pie(
        disk_data,
        names="Storage",
        values="Size",
        title="Disk Space Distribution",
        hole=0.5
    )

    st.plotly_chart(disk_chart, use_container_width=True)

# ----------------------------------
# CPU INFORMATION
# ----------------------------------

st.divider()

st.header("⚙️ CPU Monitoring")

st.metric("Current CPU Usage", f"{cpu_usage:.1f}%")

st.progress(int(cpu_usage))

if cpu_usage > 80:
    st.warning("High CPU usage detected!")
else:
    st.success("CPU usage is normal.")

# ----------------------------------
# PROCESS MONITORING
# ----------------------------------

st.divider()

st.header("📋 Running Processes")

processes = []

for process in psutil.process_iter(
    ["pid", "name", "username", "status", "memory_percent"]
):
    try:
        info = process.info

        processes.append({
            "PID": info["pid"],
            "Process Name": info["name"] or "Unknown",
            "Username": info["username"] or "Unknown",
            "Status": info["status"] or "Unknown",
            "Memory Usage (%)": round(
                info["memory_percent"] or 0, 2
            )
        })

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):
        continue

process_df = pd.DataFrame(processes)

if not process_df.empty:

    process_df = process_df.sort_values(
        by="Memory Usage (%)",
        ascending=False
    )

    st.write(f"Total Processes: {len(process_df)}")

    st.dataframe(
        process_df.head(10),
        use_container_width=True,
        hide_index=True
    )

    process_chart = px.bar(
        process_df.head(10),
        x="Process Name",
        y="Memory Usage (%)",
        title="Top 10 Memory-Consuming Processes"
    )

    st.plotly_chart(
        process_chart,
        use_container_width=True
    )

else:
    st.info("No process information available.")

# ----------------------------------
# FOOTER
# ----------------------------------

st.divider()

st.caption(
    "Linux System Monitoring Dashboard | "
    "Built with Python, Streamlit, Psutil and Plotly"
)
