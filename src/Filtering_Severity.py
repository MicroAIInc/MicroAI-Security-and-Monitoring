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
