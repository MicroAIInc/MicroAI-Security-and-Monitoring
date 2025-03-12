# Extending Agent Capabilities (Remediation & Customization)

MicroAI allows users to extend its security and monitoring capabilities by processing JSON output and implementing custom remediation actions. Users can utilize any programming language to parse data and take appropriate actions based on security alerts. Additionally, MicroAI provides built-in exporters to forward data to preferred remote locations such as HTTP, MQTT, or Redis.

## Custom Remediation Examples

### Filtering Alerts to Relevancy
By analyzing incoming alerts, users can filter out non-critical events and focus on relevant security incidents. This can be done by:
- Identifying alert types (e.g., `MAIAlert`) from MicroAI JSON output.
- Filtering based on severity, category, or keywords.
- Logging only high-priority alerts.

**Example Python Script to Filter Alerts:**

```python
import json
import redis

# Redis connection (update host/port if needed)
redis_host = "localhost"  # Change to your Redis server's IP if needed
redis_port = 5005
redis_channel = "Security_Async_JSON"

# Connect to Redis
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

def process_message(message):
    """Process and filter MAIAlert messages with High/Critical severity."""
    try:
        data = json.loads(message)
        for alert in data.get("feed", []):
            if alert.get("message_type") == "MAIAlert" and alert.get("severity") in ["High", "Critical"]:
                print(f"\n#High/Critical Alert Detected!")
                print(f"Time: {alert['edge_datetime']}")
                print(f"Device: {alert['device_id']}")
                print(f"Alert: {alert['sensor_name']}")
                print(f"Severity: {alert['severity']}")
                print(f"Details: {alert['text_value']}\n")
    except json.JSONDecodeError:
        print("? Error decoding JSON")

def redis_listener():
    """Subscribe to Redis channel and process messages."""
    pubsub = r.pubsub()
    pubsub.subscribe(redis_channel)
    print(f">Subscribed to Redis channel: {redis_channel}")

    for message in pubsub.listen():
        if message["type"] == "message":
            #New Message Received!
            process_message(message["data"])

if __name__ == "__main__":
    redis_listener()
```

### Blocking a Port
If an alert indicates that a suspicious or unauthorized port is open, the agent can dynamically block it. The following script listens for alerts, extracts the port number, kills any process using that port, and permanently blocks the port using `iptables`.

**Example Python Script to Block a Port and Terminate the Associated Process:**

```python
import redis
import json
import subprocess
import os
import re

# Connect to Redis
redis_channel = "Security_Async_JSON"
r = redis.Redis(host='localhost', port=5005, decode_responses=True)

def block_port(port):
    """ Block the port permanently using iptables and kill any process using it """
    
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
    print(f"[INFO] Port {port} blocked permanently.")

def extract_port(text_value):
    """ Extracts port number from 'text_value' field """
    match = re.search(r":(\d{2,5})\b", text_value)
    if match:
        port = int(match.group(1))
        print(f"[DEBUG] Extracted port: {port}")
        return port
    
    match = re.search(r"\b(\d{2,5})\s+(?:ProcessName|Protocol)", text_value)
    if match:
        port = int(match.group(1))
        print(f"[DEBUG] Extracted port: {port}")
        return port
    
    print("[DEBUG] No port found in message!")
    return None

def listen_for_alerts():
    """ Listen to Redis channel for new alerts """
    pubsub = r.pubsub()
    pubsub.subscribe(redis_channel)

    print("[INFO] Listening for MAIAlert messages...")

    for message in pubsub.listen():
        if message["type"] == "message":
            try:
                data = json.loads(message["data"])
                if "feed" in data:
                    for alert in data["feed"]:
                        if alert.get("message_type") == "MAIAlert":
                            text_value = alert.get("text_value", "")
                            print(f"[DEBUG] Received Alert: {text_value}")
                            
                            if "A new listening port" not in text_value:
                                print("[INFO] Alert does not contain 'A new listening port'. Skipping...")
                                continue
                            
                            port = extract_port(text_value)
                            if port:
                                block_port(port)
                            else:
                                print("[WARNING] No valid port found in alert.")
            except json.JSONDecodeError:
                print("[ERROR] Failed to decode JSON message!")

# Start listening for alerts
listen_for_alerts()
```
The output from this script should show the following output on succesfull port blocking.

```cmd
[INFO] Listening for MAIAlert messages...
[DEBUG] Received Alert: A new listening port has been detected! 6666 ProcessName: nc
[DEBUG] Extracted port: 6666
[INFO] Attempting to block port 6666...
[INFO] killing process 1750157 using port 6666...
[INFO] Port 6666 block permanently.
```

### Blocking or Isolating an IP
Blocking or isolating an IP involves taking measures to prevent a specific IP address from accessing a system or network. This action is typically used in response to malicious activity, unauthorized access attempts, or detected attacks originating from a particular IP.

**Example Python Script to Block an IP:**

```python
import redis
import json
import subprocess
import os
import re

# Connect to Redis
redis_channel = "Security_Async_JSON"  # Replace with your actual Redis channel name
r = redis.Redis(host='localhost', port=5005, decode_responses=True)

def block_ip(ip):
    """ Block the given IP using iptables """
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

def listen_for_alerts():
    """ Listen to Redis channel for new alerts """
    pubsub = r.pubsub()
    pubsub.subscribe(redis_channel)

    print("[INFO] Listening for MAIAlert messages...")

    for message in pubsub.listen():
        if message["type"] == "message":
            try:
                data = json.loads(message["data"])  # Parse JSON data
                if "feed" in data:
                    for alert in data["feed"]:
                        if alert.get("message_type") == "MAIAlert":
                            text_value = alert.get("text_value", "")
                            print(f"[DEBUG] Received Alert: {text_value}")
                            
                            # Extract IP address from the alert's text_value
                            ip = extract_ip(text_value)
                            if ip:
                                block_ip(ip)
                            else:
                                print("[WARNING] No valid IP found in alert.")
            except json.JSONDecodeError:
                print("[ERROR] Failed to decode JSON message!")

# Start listening for alerts
listen_for_alerts()
```

The output from this script should show the following output on succesfull IP blocking.

```cmd
[INFO] Listening for MAIAlert messages...
[DEBUG] Received Alert: Abnormal destination: the device transmitted 8 packets to 1.1.1.99:ICMPv4 from 190.168.8.76:ICMPv4
[DEBUG] Extracted IP: 1.1.1.99
[INFO] Attempting to block IP 1.1.1.99
[INFO] IP 1.1.1.9 block permanently
[DEBUG] Received Alert: Abnormal port/protocol: the device received 4 packets on 190.168.8.76:ICMPv4 from 1.1.1.99:ICMPv4
[DEBUG] Extracted IP: 1.1.1.99
[INFO] Attempting to block IP 1.1.1.99
[INFO] IP 1.1.1.9 block permanently
```

### Terminating a malicious Process or Payload
This example is for detecting and terminating any processes or payloads that are identified as malicious on the system. A malicious process or payload may be the result of an exploit, unauthorized access, or other forms of attack, such as ransomware or backdoor scripts.

**Example Python Script to Terminate a malicious Process or Payload:**

```python
import redis
import json
import subprocess
import os
import re

# Connect to Redis
redis_channel = "Security_Async_JSON"
r = redis.Redis(host='localhost', port=5005, decode_responses=True)

def terminate_process(process_name):
    """ Terminate the process by its name """
    
    print(f"[INFO] Attempting to terminate process: {process_name}...")

    # Find the process ID using the process name
    result = subprocess.run(f"pgrep -f {process_name}", shell=True, capture_output=True, text=True)
    pids = result.stdout.strip().split("\n")
    
    # Kill all processes found by pgrep
    for pid in pids:
        if pid.isdigit():
            print(f"[INFO] Terminating process {pid} ({process_name})...")
            os.system(f"sudo kill -9 {pid}")

def extract_process_name(text_value):
    """ Extracts the process name from 'text_value' field """
    # Extract after the last '|' character
    if "|" in text_value:
        process_name = text_value.split("|")[-1]
        print(f"[DEBUG] Extracted process name: {process_name}")
        return process_name
    else:
        print("[DEBUG] No '|' found in message!")
        return text_value  # Return the full string if no '|' is found

def is_relevant_alert(text_value):
    """ Checks if the alert message is relevant for terminating a process """
    # Only check for alerts that mention "Abnormal process detected"
    if "Abnormal process detected" in text_value:
        print(f"[INFO] Processing abnormal process alert: {text_value}")
        return True
    return False

def listen_for_alerts():
    """ Listen to Redis channel for new alerts """
    pubsub = r.pubsub()
    pubsub.subscribe(redis_channel)

    print("[INFO] Listening for MAIAlert messages...")

    for message in pubsub.listen():
        if message["type"] == "message":
            try:
                data = json.loads(message["data"])  # Parse JSON data
                if "feed" in data:
                    for alert in data["feed"]:
                        if alert.get("message_type") == "MAIAlert":
                            text_value = alert.get("text_value", "")
                            print(f"[DEBUG] Received Alert: {text_value}")
                            
                            if not is_relevant_alert(text_value):
                                continue  # Skip this alert if it's not relevant for process termination
                            
                            process_name = extract_process_name(text_value)
                            if process_name:
                                terminate_process(process_name)
                            else:
                                print("[WARNING] No valid process name found in alert.")
            except json.JSONDecodeError:
                print("[ERROR] Failed to decode JSON message!")

# Start listening for alerts
listen_for_alerts()
```
The output from this script should show the following output on succesfull malicious process or payload blocking.

```cmd
[INFO] Listening for MAIAlert messages...
[DEBUG] Received Alert: Abnormal process detected! /usr/bin/bash|ransom00.sh
[INFO] Processing abnormal process alert: Abnormal process detected! /usr/bin/bash|ransom00.sh
[DEBUG] Extracted process name: ransom00.sh...
[INFO] Attempting to terminate process: ransom00.sh...
[INFO] Terminating process 1811071 (ransom00.sh)...
[INFO] Terminating process 1811079 (ransom00.sh)...
```