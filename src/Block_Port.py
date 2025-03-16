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
