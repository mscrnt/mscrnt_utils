# **mscrnt_utils**
A collection of **utility scripts** for various projects, designed to be **modular, reusable, and easy to integrate** into different workflows.

## **Overview**
The **mscrnt_utils** repository provides **helpful tools** for different use cases, including:
- **Docker monitoring** (e.g., for DIAMBRA training environments)
- **Automation scripts**
- **Data processing utilities** *(to be added later)*
- **General-purpose functions for various projects*

The repository is structured **modularly**, allowing users to:
1. **Clone the entire repo** if they need everything.
2. **Download specific files or folders** if they only need a particular utility.

---

## **Installation**
### **Option 1: Clone the Entire Repository**
For full access to all utilities:
```bash
git clone https://github.com/mscrnt/mscrnt_utils.git
cd mscrnt_utils
```
Then install dependencies if required:
```bash
pip install -r diambra/monitoring/requirements.txt
```

### **Option 2: Clone a Specific Folder**
If you only need a specific folder, use [`git sparse-checkout`](https://git-scm.com/docs/git-sparse-checkout):

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/mscrnt/mscrnt_utils.git
cd mscrnt_utils
git sparse-checkout set diambra/monitoring
```
This will **only download** `diambra/monitoring/` without pulling the entire repo.

### **Option 3: Download a Single File**
To download just **one file**, use `wget` or `curl`:
```bash
wget https://raw.githubusercontent.com/mscrnt/mscrnt_utils/main/diambra/monitoring/monitor.py
```
or
```bash
curl -O https://raw.githubusercontent.com/mscrnt/mscrnt_utils/main/diambra/monitoring/monitor.py
```

---

## **Folder Structure**
The utilities are **organized by category**:

```
mscrnt_utils/
│── readme.md
│── diambra/
│   ├── monitoring/
│   │   ├── monitor.py  # Docker monitoring script for DIAMBRA training
│   │   ├── requirements.txt
│   │   ├── readme.md
```
- **`diambra/monitoring/`** → Scripts related to DIAMBRA training (e.g., Docker monitoring)

---

## **Usage**
### **1. Running a Utility**
Once you have the file(s), navigate to the directory and run:
```bash
python diambra/monitoring/monitor.py -m 3
```
_(Runs the Docker monitoring script with `min_stage=3`.)_

### **2. Importing into Your Own Projects**
To use utilities in your own Python scripts, import them as needed:

```python
from diambra.monitoring.monitor import DockerMonitor

monitor = DockerMonitor(min_stage=3)
monitor.start_monitoring()
```

