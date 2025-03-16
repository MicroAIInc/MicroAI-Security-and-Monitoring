from fastapi import FastAPI, Request
import json
import subprocess
import os
import re


SEVERITIES_TO_FILTER = ["High", "Critical"]  # List of severities to filter
EXCLUDED_IPS = ["1.1.1.3"]  # List of IPs to exclude from blocking
EXCLUDED_PROCESSES = ["sh", "bash", "python3"]  # Processes to exclude from termination

app = FastAPI()

def process_high_severity_alert(alert):
    """Process and filter MAIAlert messages with specified severity levels."""
    if alert.get("message_type") == "MAIAlert" and alert.get("severity") in SEVERITIES_TO_FILTER:
        print(f"\n#High/Critical Alert Detected!")
        print(f"Time: {alert['edge_datetime']}")
        print(f"Device: {alert['device_id']}")
        print(f"Alert: {alert['sensor_name']}")
        print(f"Severity: {alert['severity']}")
        print(f"Details: {alert['text_value']}\n")

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

def extract_port(text_value):
    """ Extracts port number from 'text_value' field """
    match = re.search(r"\b(\d{2,5})\b", text_value)
    if match:
        port = int(match.group(1))
        print(f"[DEBUG] Extracted port: {port}")
        return port
    
    print("[DEBUG] No port found in message!")
    return None

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

def extract_process_name(text_value):
    """ Extracts the process name from the alert """
    if "|" in text_value:
        process_name = text_value.split("|")[-1].strip()
        print(f"[DEBUG] Extracted process name: {process_name}")
        return process_name
    return text_value  # Return full string if no '|' is found

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

@app.post("/")
async def receive_alerts(request: Request):
    """Unified API endpoint to receive and process all types of alerts."""
    try:
        data = await request.json()  # Parse the JSON data

        if data.get("message_type") == "ASYNC":
            print("[INFO] Processing ASYNC message...")

            for alert in data.get("feed", []):
                # Process high severity alerts
                process_high_severity_alert(alert)
                
                msg_type = alert.get("message_type", "")
                text_value = alert.get("text_value", "")
                
                # Process IP blocking alerts
                if "MAIAlert" in msg_type:
                    # Process for IP blocking
                    print(f"[DEBUG] Received Alert: {text_value}")
                    ip = extract_ip(text_value)
                    if ip:
                        block_ip(ip)
                
                # Process port blocking alerts
                if "A new listening port" in text_value:
                    print(text_value)
                    port = extract_port(text_value)
                    if port:
                        block_port(port)
                
                # Process suspicious process alerts
                if "Abnormal process detected" in text_value:
                    print(text_value)
                    process_name = extract_process_name(text_value)
                    if process_name and process_name not in EXCLUDED_PROCESSES:
                        terminate_process(process_name)
                    elif process_name in EXCLUDED_PROCESSES:
                        print(f"[INFO] Skipping remediation for excluded process: {process_name}")

        return {"status": "success", "message": "Alert processed"}
    
    except json.JSONDecodeError:
        print("[ERROR] Failed to decode JSON message!")
        return {"status": "error", "message": "Invalid JSON"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)