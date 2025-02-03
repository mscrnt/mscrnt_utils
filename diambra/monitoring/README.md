# **Docker Container Log Monitor**
A **Docker container monitoring script** that tracks **stage progression** and **game completion logs** for reinforcement learning environments. This script is particularly useful for monitoring **DIAMBRA-based training environments**.

📌 **Part of the [`mscrnt_utils`](https://github.com/mscrnt/mscrnt_utils) repository.**  

---

## **Features**
✅ **Monitors Docker containers in real-time**  
✅ **Tracks specific game-related log outputs** (`stage progression`, `game completion`)  
✅ **Supports automatic logging with file rotation**  
✅ **Color-coded console output** for easy readability  
✅ **Threaded execution for concurrent container monitoring**  
✅ **Supports argument-based configuration (`min_stage`)**  

---

## **Installation**
Ensure you have the following installed:
- **Python 3.10+**
- **Docker** (with running containers)
- **Required Python packages** (`pip install -r requirements.txt`)

### **1. Clone the Repository**
To get the entire **mscrnt_utils** repository:
```bash
git clone https://github.com/mscrnt/mscrnt_utils.git
cd mscrnt_utils/diambra/monitoring
```

#### **OR**: Clone only the monitoring utility using `sparse-checkout`:
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/mscrnt/mscrnt_utils.git
cd mscrnt_utils
git sparse-checkout set diambra/monitoring
cd diambra/monitoring
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Usage**
This script follows logs of running **Docker containers** and detects specific outputs related to **stage progression** and **game completion**.

### **Run Monitoring**
```bash
python monitor.py -m <MINIMUM_STAGE>
```
- `-m` or `--min_stage` → Specifies the **minimum stage level** to start monitoring.
  - `0` → Monitoring **disabled**.
  - `> 0` → Only tracks logs **from that stage onward**.

#### **Example:**
```bash
python monitor.py -m 3
```
_(Monitors logs starting **from stage 3**.)_

---

## **How It Works**
### **1. `monitor.py`**
- **Fetches running Docker containers**
- **Scans past logs** (if `initial_scan=True`)
- **Follows real-time logs** using `docker logs -f`
- **Processes log entries** to detect:
  - **Stage progressions** (e.g., "Moving to stage X")
  - **Game completions** (e.g., "Game completed!")
- **Logs outputs to console & file**
- **Periodically prints status** _(every 60 seconds)_

### **2. Logging and Output**
- **Console Output**
  - ✅ **Stage progress** → **White**
  - ✅ **Game completed** → **Yellow**
  - ✅ **Info logs** → **Cyan**
  - ✅ **Errors** → **Red**
- **File Logging**
  - Stored in `./output/logs/monitor.log`
  - Uses **rotating log files** _(max 5MB per file, 2 backups)_

---

## **Stopping the Monitor**
To **gracefully stop monitoring**, press:
```bash
CTRL+C
```
This will:
- **Save all logs**
- **Stop active monitoring threads**
- **Exit the script safely**

---

## **Example Output**
```bash
[INFO] Active containers: agent1, agent2
[DEBUG] agent1 reached stage 3 of 10
[DEBUG] agent2 (1) Game completed!
[INFO] *** Currently monitoring statuses for 2 containers ***
[INFO] *** 3 Game(s) Completed! ***
```

