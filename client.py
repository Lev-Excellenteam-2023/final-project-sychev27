import requests
from datetime import datetime

class Status:
    def __init__(self, status, filename, timestamp, explanation):
        self.status = status
        self.filename = filename
        self.timestamp = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
        self.explanation = explanation

    def is_done(self):
        return self.status == 'done'

class WebApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        url = f"{self.base_url}/upload"
        files = {'file': open(file_path, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            return response.json().get('uid')
        else:
            raise Exception(f"Upload failed with status code {response.status_code}")

    def status(self, uid):
        url = f"{self.base_url}/status/{uid}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Status(data['status'], data['filename'], data['timestamp'], data['explanation'])
        else:
            raise Exception(f"Status retrieval failed with status code {response.status_code}")

# Usage example
client = WebApiClient('http://localhost:5000')  # Replace with the actual base URL of your web app

# Upload example
file_path = '/path/to/file.txt'  # Replace with the path of the file you want to upload
uid = client.upload(file_path)
print(f"Uploaded file with UID: {uid}")

# Status example
#uid = 'your-uid-here'  # Replace with the actual UID you want to check
#status = client.status(uid)
#if status.is_done():
   # print("Upload processing is done")
#else:
    #print("Upload is still pending")

# Other methods can be added to the Status class based on your needs