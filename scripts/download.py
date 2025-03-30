import requests
import zipfile
import io
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # Load .env file if exists

SEC_URL = "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"

def download_submissions():
    os.makedirs("data", exist_ok=True)

    email = os.getenv('SEC_EMAIL', 'default@example.com')  # Fallback email
    headers = {"User-Agent": f"tonybaby16 {email}"}  # Updated User-Agent
    
    try:
        print(f"Downloading SEC data at {datetime.utcnow().isoformat()}")
        response = requests.get(SEC_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall("data")
        
        print("Download successful")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

if __name__ == "__main__":
    download_submissions()