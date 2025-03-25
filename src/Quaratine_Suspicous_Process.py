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