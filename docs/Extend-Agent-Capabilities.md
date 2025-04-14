# Extending Agent Capabilities (Remediation & Customization)

MicroAI allows users to extend its security & monitoring capabilities by processing JSON output and implementing custom remediation actions. Users can utilize any programming language to parse data and take appropriate actions based on security alerts. Additionally, MicroAI provides built-in exporters to forward data to preferred remote locations such as HTTP, MQTT, or Redis.

# Output Json payload

The agent generates both synchronous and asynchronous payloads, which are essential for monitoring alerts, notifications, and real-time device updates. By subscribing to these payloads, users can implement custom remediation strategies or automated responses.

For a detailed breakdown of both SYNC and ASYNC payload structures, refer to the [payload documentation](./Sync-and-Async-Payloads.md).

## Custom Remediation Examples

### Configure External Exporter

In order to extend the capabalities of the agent, the alerts and synschronous data needs to be configured to an output based on the selected protocol. The example below shows how this can be configured to use the http protocol.

```json
{
  // ... other fields ...
    "ExternalExporter": {
      "ExternalExporterType": "HTTP", // Update the exporter Type
      "Https_Post_Endpoint": "http://localhost:8000", // Add the desired endpoint
      "Output_Redis_Endpoint": "",
      "Output_MQTT": {
        "Endpoint": "127.0.0.1",
        "Port": 1884,
        "Username": "",
        "Password": "",
        "topic_prefix": "data/"
      }
    }
  // ... other fields ...
}
```

### Filtering Alerts to Relevancy
By analyzing incoming alerts, users can filter out non-critical events and focus on relevant security incidents. This can be done by:
- Identifying alert types (e.g., `MAIAlert`) from MicroAI JSON output.
- Filtering based on severity, category, or keywords.
- Logging only high-priority alerts.

**Example Python Script to Filter Alerts:**

```python
from fastapi import FastAPI, Request
import json

# List of severities to filter
SEVERITIES_TO_FILTER = ["High", "Critical"]  # You can easily change these values

app = FastAPI()

def process_message(message):
    """Process and filter MAIAlert messages with specified severity levels."""
    try:
        data = json.loads(message)
        for alert in data.get("feed", []):
            if alert.get("message_type") == "MAIAlert" and alert.get("severity") in SEVERITIES_TO_FILTER:
                print(f"\n#High/Critical Alert Detected!")
                print(f"Time: {alert['edge_datetime']}")
                print(f"Device: {alert['device_id']}")
                print(f"Alert: {alert['sensor_name']}")
                print(f"Severity: {alert['severity']}")
                print(f"Details: {alert['text_value']}\n")
    except json.JSONDecodeError:
        print("? Error decoding JSON")

@app.post("/")
async def receive_alerts(request: Request):
    """API endpoint to receive alerts and process them."""
    try:
        data = await request.json()  # Parse the JSON data

        if data.get("message_type") == "ASYNC":
            print("[INFO] Processing ASYNC message...")

            for alert in data.get("feed", []):
                msg_type = alert.get("message_type", "")
                if "MAIAlert" in msg_type:
                    process_message(json.dumps(data))  # Process the received message
        return {"status": "success", "message": "Alert processed"}
    
    except json.JSONDecodeError:
        print("[ERROR] Failed to decode JSON message!")
        return {"status": "error", "message": "Invalid JSON"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
The output from this script should show the following output on succesfull filtering on alerts.

```cmd
[INFO] Processing ASYNC message...
 
#High/Critical Alert Detected!
Time: 2025-03-13T12:19:20.386Z
Device: 00:15:5d:02:da:17
Alert: AI-test-U20-2.165.local (192.168.2.187) A new listening port has been detected!
Severity: Critical
Details: A new listening port has been detected! 6011 ProcessName: sshd: c2m@p
```

### Blocking a Port
If an alert indicates that a suspicious or unauthorized port is open, the agent can dynamically block it. The following script listens for alerts, extracts the port number, kills any process using that port, and permanently blocks the port using `iptables`.

**Example Python Script to Block a Port and Terminate the Associated Process:**

```python
from fastapi import FastAPI, Request
import json
import subprocess
import os
import re

app = FastAPI()

def block_port(port):
    """ Block the port using iptables and kill any process using it """
    
    print(f"[INFO] Attempting to block port {port}...")

    # Find process using the port
    result = subprocess.run(f"sudo lsof -i :{port} -t", shell=True, capture_output=True, text=True)
    pids = result.stdout.strip().split("\n")
    
    # Kill all processes using the port
    for pid in pids:
        if pid.isdigit():
            print(f"[INFO] Killing process {pid} using port {port}...")
            os.system(f"sudo kill -9 {pid}")

    # Block the port using iptables
    os.system(f"sudo iptables -A INPUT -p tcp --dport {port} -j DROP")
    os.system(f"sudo iptables -A OUTPUT -p tcp --sport {port} -j DROP")
    print(f"[INFO] Port {port} blocked.")

def extract_port(text_value):
    """ Extracts port number from 'text_value' field """
    match = re.search(r"\b(\d{2,5})\b", text_value)
    if match:
        port = int(match.group(1))
        print(f"[DEBUG] Extracted port: {port}")
        return port
    
    print("[DEBUG] No port found in message!")
    return None

@app.post("/")
async def receive_alerts(request: Request):
    """ API endpoint to receive alerts and process them """
    try:
        data = await request.json()  

        if data.get("message_type") == "ASYNC":
            print("[INFO] Processing ASYNC message...")

            for alert in data.get("feed", []):
                msg_type = alert.get("message_type", "")
                text_value = alert.get("text_value", "")

                if "A new listening port" in text_value:
                    print(text_value)
                    port = extract_port(text_value)
                    if port:
                        block_port(port)
                    else:
                        print("[WARNING] No valid port found in alert.")

        return {"status": "success", "message": "ASYNC alert processed"}
    
    except json.JSONDecodeError:
        print("[ERROR] Failed to decode JSON message!")
        return {"status": "error", "message": "Invalid JSON"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
The output from this script should show the following output on succesfull port blocking.

```cmd
[DEBUG] Received Alert: A new listening port has been detected! 8844 ProcessName: nc
[DEBUG] No IP found after 'to' or 'from' in message!
A new listening port has been detected! 8844 ProcessName: nc
[DEBUG] Extracted port: 8844
[INFO] Attempting to block port 8844...
[INFO] Killing process 2918553 using port 8844...
[INFO] Port 8844 blocked.
```

### Blocking or Isolating an IP
Blocking or isolating an IP involves taking measures to prevent a specific IP address from accessing a system or network. This action is typically used in response to malicious activity, unauthorized access attempts, or detected attacks originating from a particular IP.

**Example Python Script to Block an IP:**

```python
from fastapi import FastAPI, Request
import json
import subprocess
import os
import re

app = FastAPI()

EXCLUDED_IPS = ["1.1.1.3"]  # List of IPs to exclude from blocking

def block_ip(ip):
    """ Block the given IP using iptables """
    if ip in EXCLUDED_IPS:
        print(f"[INFO] Skipping blocking for excluded IP {ip}")
        return
    
    print(f"[INFO] Attempting to block IP {ip}...")

    # Block the IP using iptables
    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
    os.system(f"sudo iptables -A OUTPUT -d {ip} -j DROP")
    print(f"[INFO] IP {ip} blocked permanently.")

def extract_ip(text_value):
    """ Extracts IP addresses that come after the words 'to' or 'from' in the text_value field """
    # Regular expression to find IPs after "to" or "from"
    match = re.findall(r"\b(?:to|from)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", text_value, re.IGNORECASE)
    
    if match:
        # Return the first IP address found after 'to' or 'from'
        print(f"[DEBUG] Extracted IP: {match[0]}")
        return match[0]
    
    print("[DEBUG] No IP found after 'to' or 'from' in message!")
    return None

@app.post("/")
async def receive_alerts(request: Request):
    """ API endpoint to receive alerts and process them """
    try:
        data = await request.json()  # Parse the JSON data

        if data.get("message_type") == "ASYNC":
            print("[INFO] Processing ASYNC message...")

            for alert in data.get("feed", []):
                msg_type = alert.get("message_type", "")
                text_value = alert.get("text_value", "")

                if "MAIAlert" in msg_type:
                    print(f"[DEBUG] Received Alert: {text_value}")
                    
                    # Extract IP address from the alert's text_value
                    ip = extract_ip(text_value)
                    if ip:
                        block_ip(ip)
                    else:
                        print("[WARNING] No valid IP found in alert.")

        return {"status": "success", "message": "ASYNC alert processed"}
    
    except json.JSONDecodeError:
        print("[ERROR] Failed to decode JSON message!")
        return {"status": "error", "message": "Invalid JSON"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

The output from this script should show the following output on succesfull IP blocking.

```cmd
[INFO] Processing ASYNC message...
[DEBUG] Received Alert: Abnormal port/protocol: the device received  2 packets on 192.168.2.187:ICMPv4 from 1.1.1.77:ICMPv4
[DEBUG] Extracted IP: 1.1.1.77
[INFO] Attempting to block IP 1.1.1.77...
[INFO] IP 1.1.1.77 blocked permanently.
```

### Quarantine a malicious Process
This example is for detecting and quratining any processes that are identified as malicious on the system. A malicious process may be the result of an exploit, unauthorized access, or other forms of attack, such as ransomware or backdoor scripts.

**Example Python Script to Qurantine a malicious Process:**

```python
from fastapi import FastAPI, Request
import json
import os
import shutil
import hashlib
from pathlib import Path
import uvicorn

app = FastAPI()

QUARANTINE_FOLDER = "/tmp/quarantine"

# Ensure quarantine folder exists
def create_quarantine_folder():
    if not os.path.exists(QUARANTINE_FOLDER):
        os.makedirs(QUARANTINE_FOLDER)

# Compute SHA-256 hash of the file
def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    except Exception as e:
        print(f"[ERROR] Failed to calculate hash for {file_path}: {e}")
        return None
    return sha256_hash.hexdigest()

# Move the file to quarantine
def quarantine_file(file_path):
    """ Moves the file to the quarantine folder with its hash in the filename """
    if os.path.exists(file_path):
        file_hash = get_file_hash(file_path)
        if file_hash is None:
            print(f"[WARNING] Skipping {file_path} due to hash calculation failure.")
            return

        original_filename = Path(file_path).name
        quarantined_file = os.path.join(QUARANTINE_FOLDER, f"{file_hash}-{original_filename}.quarantine")

        try:
            shutil.move(file_path, quarantined_file)
            print(f"[INFO] File moved to quarantine: {quarantined_file}")
            os.chmod(quarantined_file, 0o444)  # Make file read-only
        except Exception as e:
            print(f"[ERROR] Failed to quarantine {file_path}: {e}")
    else:
        print(f"[WARNING] File does not exist: {file_path}")

@app.post("/")
async def receive_alerts(request: Request):
    """ Receives HTTP alerts and quarantines files based on ASYNC messages """
    try:
        data = await request.json()

        if data.get("message_type") == "ASYNC":
            print("[INFO] Processing ASYNC message...")

            for alert in data.get("feed", []):
                text_value = alert.get("text_value", "")
                print(text_value)

                if "Suspicious file detected" in text_value or "Highly Suspicious file detected" in text_value:  # Check both conditions
                    print(f"[INFO] Alert received: {text_value}")

                    # Extract file path (Ensure correct extraction after the detection phrase)
                    if "Suspicious file detected" in text_value:
                        file_path = text_value.split("Suspicious file detected:")[-1].strip()
                    elif "Highly Suspicious file detected" in text_value:
                        file_path = text_value.split("Highly Suspicious file detected:")[-1].strip()

                    # Extract the path after the message
                    file_path = file_path.split(":")[-1].strip()

                    print(f"[INFO] Extracted file path: {file_path}")

                    # Check if file path exists and quarantine the file
                    if os.path.exists(file_path):
                        quarantine_file(file_path)
                    else:
                        print(f"[WARNING] File path does not exist: {file_path}")

        return {"status": "success", "message": "ASYNC alert processed"}

    except json.JSONDecodeError:
        print("[ERROR] Failed to decode JSON message!")
        return {"status": "error", "message": "Invalid JSON"}


if __name__ == "__main__":
    create_quarantine_folder()  # Ensure quarantine folder is ready
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
The output from this script should show the following output on succesfully quaratining a process.

```cmd
[INFO] Alert received: Highly Suspicious file detected (Ransomware patterns): /home/Remediation/Ransomware.exe
[INFO] Extracted file path: /home/Remediation/Ransomware.exe
[INFO] File moved to quarantine: /tmp/quarantine/5cb2ffb84bd5bbb3a1ad7c587ec883e1fc3446ff5c7cc88ab63f959e67af2ea6-Ransomware.exe.quarantine
```

### Terminating a malicious Process or Payload
This example is for detecting and terminating any processes or payloads that are identified as malicious on the system. A malicious process or payload may be the result of an exploit, unauthorized access, or other forms of attack, such as ransomware or backdoor scripts.

**Example Python Script to Terminate a malicious Process or Payload:**

```python
from fastapi import FastAPI, Request
import json
import subprocess
import os

app = FastAPI()

EXCLUDED_PROCESSES = ["sh","bash","python3"]  # Processes to exclude from termination

def terminate_process(process_name):
    """ Terminate the process by its name unless it's excluded """
    if process_name in EXCLUDED_PROCESSES:
        print(f"[INFO] Skipping termination for excluded process: {process_name}")
        return
    
    print(f"[INFO] Attempting to terminate process: {process_name}...")
    result = subprocess.run(f"pgrep -f {process_name}", shell=True, capture_output=True, text=True)
    pids = result.stdout.strip().split("\n")
    
    for pid in pids:
        if pid.isdigit():
            print(f"[INFO] Terminating process {pid} ({process_name})...")
            os.system(f"sudo kill -9 {pid}")

def extract_process_name(text_value):
    """ Extracts the process name from the alert """
    if "|" in text_value:
        process_name = text_value.split("|")[-1]
        print(f"[DEBUG] Extracted process name: {process_name}")
        return process_name
    return text_value  # Return full string if no '|' is found

@app.post("/")
async def receive_alerts(request: Request):
    """ API endpoint to receive alerts and process them """
    try:
        data = await request.json()  

        if data.get("message_type") == "ASYNC":
            print("[INFO] Processing ASYNC message...")

            for alert in data.get("feed", []):
                msg_type = alert.get("message_type", "")
                text_value = alert.get("text_value", "")


                if "Abnormal process detected" in text_value:
                    print(text_value)
                    process_name = extract_process_name(text_value)

                    if process_name in EXCLUDED_PROCESSES:
                        print(f"[INFO] Skipping remediation for excluded process: {process_name}")
                    elif process_name:
                        terminate_process(process_name)
                    else:
                        print("[WARNING] No valid process name found in alert.")

        return {"status": "success", "message": "ASYNC alert processed"}
    
    except json.JSONDecodeError:
        print("[ERROR] Failed to decode JSON message!")
        return {"status": "error", "message": "Invalid JSON"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
The output from this script should show the following output on succesfull malicious process or payload blocking.

```cmd
[INFO] Processing ASYNC message...
Abnormal process detected! /usr/bin/ransom.sh|ransom.sh
[DEBUG] Extracted process name: ransom.sh
[INFO] Attempting to terminate process: ransom.sh...
[INFO] Terminating process 2883186 (ransom.sh)...
[INFO] Terminating process 2883198 (ransom.sh)...
```