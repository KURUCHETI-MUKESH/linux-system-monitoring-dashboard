
import streamlit as st
import psutil
import pandas as pd
import plotly.express as px
import time

from datetime import datetime
from streamlit_autorefresh import st_autorefresh


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Linux System Monitor",
    page_icon="🖥️",
    layout="wide"
)

# Refresh every 5 seconds
st_autorefresh(
    interval=5000,
    key="system_monitor_refresh"
)


# ==========================================
# 2. DASHBOARD DESIGN
# ==========================================

st.title("🖥️ Linux System Monitoring Dashboard")

st.write(
    "Real-time monitoring of CPU, memory, "
    "disk usage, uptime and running processes."
)

st.caption(
    f"Last updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)


# ==========================================
# 3. SIDEBAR SETTINGS
# ==========================================

st.sidebar.title("⚙️ Dashboard Settings")

st.sidebar.write("Configure system alert thresholds.")

warning_limit = st.sidebar.slider(
    "Warning Threshold (%)",
    min_value=50,
    max_value=95,
    value=80
)

critical_limit = st.sidebar.slider(
    "Critical Threshold (%)",
    min_value=warning_limit + 1,
    max_value=100,
    value=max(90, warning_limit + 1)
)

st.sidebar.info("Dashboard refresh interval: 5 seconds")


# ==========================================
# 4. HEALTH STATUS FUNCTION
# ==========================================

def get_status(value):

    if value > critical_limit:
        return "CRITICAL"

    elif value > warning_limit:
        return "WARNING"

    return "HEALTHY"


# ==========================================
# 5. INITIALIZE SESSION HISTORY
# ==========================================

if "metrics_history" not in st.session_state:
    st.session_state.metrics_history = []

if "alert_history" not in st.session_state:
    st.session_state.alert_history = []

if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = {}


# ==========================================
# 6. COLLECT SYSTEM INFORMATION
# ==========================================

cpu_usage = psutil.cpu_percent(interval=0.2)

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

uptime = f"{days}d {hours}h {minutes}m"

current_time = datetime.now()


# ==========================================
# 7. STORE METRIC HISTORY
# ==========================================

metrics_record = {
    "Time": current_time,
    "CPU Usage": cpu_usage,
    "RAM Usage": ram_percent,
    "Disk Usage": disk_percent
}

st.session_state.metrics_history.append(metrics_record)

# Keep only the latest 120 readings
st.session_state.metrics_history = (
    st.session_state.metrics_history[-120:]
)

history_df = pd.DataFrame(
    st.session_state.metrics_history
)


# ==========================================
# 8. SYSTEM OVERVIEW
# ==========================================

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


# ==========================================
# 9. CPU MONITORING
# ==========================================

st.divider()

st.header("⚙️ CPU Monitoring")

cpu_col1, cpu_col2 = st.columns(2)

with cpu_col1:

    st.metric("Current CPU Usage", f"{cpu_usage:.2f}%")

    st.progress(min(int(cpu_usage), 100))

    cpu_status = get_status(cpu_usage)

    if cpu_status == "CRITICAL":
        st.error("Critical CPU usage!")

    elif cpu_status == "WARNING":
        st.warning("High CPU usage detected!")

    else:
        st.success("CPU usage is normal.")

with cpu_col2:

    st.subheader("CPU Usage History")

    fig_cpu = px.line(
        history_df,
        x="Time",
        y="CPU Usage",
        title="CPU Usage Over Time",
        markers=True
    )

    fig_cpu.update_layout(
        yaxis_title="CPU Usage (%)",
        xaxis_title="Time",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(fig_cpu, use_container_width=True)


# ==========================================
# 10. RAM MONITORING
# ==========================================

st.divider()

st.header("🧠 RAM Monitoring")

ram_col1, ram_col2 = st.columns(2)

with ram_col1:

    st.metric("Total RAM", f"{total_ram:.2f} GB")
    st.metric("Used RAM", f"{used_ram:.2f} GB")
    st.metric("Available RAM", f"{available_ram:.2f} GB")

    ram_status = get_status(ram_percent)

    if ram_status == "CRITICAL":
        st.error("Critical RAM usage!")

    elif ram_status == "WARNING":
        st.warning("High RAM usage detected!")

    else:
        st.success("RAM usage is normal.")

with ram_col2:

    st.subheader("RAM Usage History")

    fig_ram = px.line(
        history_df,
        x="Time",
        y="RAM Usage",
        title="RAM Usage Over Time",
        markers=True
    )

    fig_ram.update_layout(
        yaxis_title="RAM Usage (%)",
        xaxis_title="Time",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(fig_ram, use_container_width=True)

    ram_data = pd.DataFrame({
        "Memory": ["Used", "Available"],
        "Size": [used_ram, available_ram]
    })

    fig_ram_pie = px.pie(
        ram_data,
        names="Memory",
        values="Size",
        title="RAM Distribution",
        hole=0.5
    )

    st.plotly_chart(fig_ram_pie, use_container_width=True)


# ==========================================
# 11. DISK MONITORING
# ==========================================

st.divider()

st.header("💾 Disk Monitoring")

disk_col1, disk_col2 = st.columns(2)

with disk_col1:

    st.metric("Total Disk", f"{total_disk:.2f} GB")
    st.metric("Used Disk", f"{used_disk:.2f} GB")
    st.metric("Free Disk", f"{free_disk:.2f} GB")

    disk_status = get_status(disk_percent)

    if disk_status == "CRITICAL":
        st.error("Critical disk usage!")

    elif disk_status == "WARNING":
        st.warning("Disk space is running low!")

    else:
        st.success("Disk usage is normal.")

with disk_col2:

    disk_data = pd.DataFrame({
        "Storage": ["Used", "Free"],
        "Size": [used_disk, free_disk]
    })

    fig_disk = px.pie(
        disk_data,
        names="Storage",
        values="Size",
        title="Disk Space Distribution",
        hole=0.5
    )

    st.plotly_chart(fig_disk, use_container_width=True)


# ==========================================
# 12. SYSTEM HEALTH ALERTS
# ==========================================

st.divider()

st.header("🚨 System Health Alerts")

resources = {
    "CPU": cpu_usage,
    "RAM": ram_percent,
    "Disk": disk_percent
}

for resource, value in resources.items():

    status = get_status(value)

    if status != "HEALTHY":

        last_alert = st.session_state.last_alert_time.get(
            resource, 0
        )

        # Avoid repeating the same alert every 5 seconds
        if time.time() - last_alert >= 60:

            alert = {
                "Time": current_time,
                "Resource": resource,
                "Usage (%)": round(value, 2),
                "Status": status,
                "Message": f"{resource} usage is {status}"
            }

            st.session_state.alert_history.append(alert)

            st.session_state.last_alert_time[resource] = time.time()

        if status == "CRITICAL":
            st.error(f"{resource} usage is critical: {value:.2f}%")

        else:
            st.warning(f"{resource} usage is high: {value:.2f}%")

    else:
        st.success(f"{resource}: Healthy ({value:.2f}%)")


# ==========================================
# 13. ALERT HISTORY
# ==========================================

st.subheader("Alert History")

if st.session_state.alert_history:

    alert_df = pd.DataFrame(
        st.session_state.alert_history
    )

    st.dataframe(
        alert_df.iloc[::-1],
        use_container_width=True,
        hide_index=True
    )

    alert_csv = alert_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Alert History",
        data=alert_csv,
        file_name="system_alert_history.csv",
        mime="text/csv"
    )

else:

    st.info("No alerts generated. All monitored resources are healthy.")


# ==========================================
# 14. PROCESS MONITORING
# ==========================================

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

    search = st.text_input(
        "Search Process by Name"
    )

    if search:
        process_df = process_df[
            process_df["Process Name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        process_df.head(20),
        use_container_width=True,
        hide_index=True
    )

    process_chart = px.bar(
        process_df.head(10),
        x="Process Name",
        y="Memory Usage (%)",
        title="Top Memory-Consuming Processes"
    )

    st.plotly_chart(
        process_chart,
        use_container_width=True
    )

    process_csv = process_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Process Report",
        data=process_csv,
        file_name="process_report.csv",
        mime="text/csv"
    )

else:

    st.info("No process information available.")


# ==========================================
# 15. DOWNLOAD METRICS REPORT
# ==========================================

st.divider()

st.header("📥 Download System Reports")

metrics_csv = history_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download CPU, RAM and Disk History",
    data=metrics_csv,
    file_name="system_metrics_history.csv",
    mime="text/csv"
)


# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.caption(
    "Linux System Monitoring Dashboard | "
    "Python | Streamlit | Psutil | Pandas | Plotly"
)

st.caption(
    "Developed by Kurucheti Mukesh"
)

