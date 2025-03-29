import requests
import zipfile
import io
import os
from datetime import datetime

SEC_SUBMISSIONS_URL = "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"

def download_sec_submissions():
    # Create data directory if not exists
    os.makedirs("../data", exist_ok=True)
    
    print("Downloading SEC submissions.zip...")
    response = requests.get(SEC_SUBMISSIONS_URL, headers={"User-Agent": "Your Name your.email@example.com"})
    response.raise_for_status()
    
    # Extract the zip file
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall("../data")
    
    print(f"Download complete at {datetime.now().isoformat()}")

if __name__ == "__main__":
    download_sec_submissions()