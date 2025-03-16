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
