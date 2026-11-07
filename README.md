
A Python-based Linux system monitoring project that tracks CPU usage, RAM utilization, disk space, system uptime, and running processes through an interactive Streamlit dashboard.

## Project Overview

The Linux System Monitoring Dashboard collects system performance information using Python and the Psutil library. It presents important metrics and visualizations through a web-based dashboard built with Streamlit and Plotly.

The project also includes a separate health-checking script that identifies high CPU, RAM, and disk usage and records alerts in a log file.

## Features

- Automatic dashboard refresh every 5 seconds.
- Real-time CPU usage monitoring and history chart.
- RAM usage monitoring and history chart.
- Disk space monitoring.
- System uptime monitoring.
- Running process monitoring.
- Process search and filtering.
- Configurable warning and critical thresholds.
- Integrated system health alerts.
- Alert history with CSV export.
- Downloadable CPU, RAM and disk metrics reports.
- Downloadable process reports.

## Technologies Used

- Python
- Linux / Ubuntu / WSL2
- Streamlit
- Streamlit Autorefresh
- Psutil
- Pandas
- Plotly
- Git and GitHub

## Project Structure

```text
linux-system-monitor/
│
├── app.py
├── cpu_monitor.py
├── memory_monitor.py
├── disk_monitor.py
├── process_monitor.py
├── health_check.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── images/
    ├── dashboard_overview.png
    └── process_monitoring.png
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/KURUCHETI-MUKESH/linux-system-monitoring-dashboard.git
cd linux-system-monitoring-dashboard
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Run Individual Monitoring Programs

CPU monitoring:

```bash
python cpu_monitor.py
```

Memory monitoring:

```bash
python memory_monitor.py
```

Disk and uptime monitoring:

```bash
python disk_monitor.py
```

Process monitoring:

```bash
python process_monitor.py
```

System health checker:

```bash
python health_check.py
```

## Health Alert Thresholds

| Resource | Healthy | Warning | Critical |
|---|---|---|---|
| CPU | 80% or below | Above 80% to 90% | Above 90% |
| RAM | 80% or below | Above 80% to 90% | Above 90% |
| Disk | 80% or below | Above 80% to 90% | Above 90% |

These are configurable example thresholds used by this project, not universal operating-system standards.

## Screenshots

### Dashboard Overview

![Dashboard Overview](images/dashboard_overview.png)

### CPU and RAM History

![CPU and RAM History](images/CPUmetrics_history.png,RAMmetrics_history.png)

### System Health Alerts

![System Health Alerts](images/system_alerts.png)

### Process Monitoring

![Process Monitoring](images/process_monitoring.png)

## Learning Outcomes

- Practiced Linux commands and terminal operations.
- Used Python to collect system performance information.
- Worked with the Psutil library.
- Built an interactive dashboard using Streamlit.
- Created visualizations using Plotly.
- Implemented system health checks and alert logging.
- Practiced Git and GitHub project management.

## Platform Notes

This project was developed and tested in Ubuntu running through WSL2 on Windows. System readings, available resources, disk information, and uptime can differ between WSL2 and a native Linux installation.

## Author

**Kurucheti Mukesh**

GitHub: https://github.com/KURUCHETI-MUKESH

