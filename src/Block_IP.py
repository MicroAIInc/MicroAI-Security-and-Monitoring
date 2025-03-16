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
