import requests
from datetime import datetime


class Status:
    def __init__(self, status, filename, timestamp, explanation):
        """
        Represents the status of an upload.

        :param status: The status of the upload.
        :param filename: The original filename of the upload.
        :param timestamp: The timestamp of the upload.
        :param explanation: The explanation or output of the upload.
        """
        self.status = status
        self.filename = filename
        self.timestamp = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
        self.explanation = explanation

    def is_done(self):
        """
        Checks if the status is 'done'.

        :return: True if the status is 'done', False otherwise.
        """
        return self.status == 'done'


class WebApiClient:
    def __init__(self, base_url):
        """
        Represents a client for interacting with a web API.

        :param base_url: The base URL of the web API.
        """
        self.base_url = base_url

    def upload(self, file_path):
        """
        Uploads a file to the web API.

        :param file_path: The path of the file to upload.
        :return: The UID (unique identifier) of the upload.
        :raises Exception: If the upload fails with a non-200 status code.
        """
        url = f"{self.base_url}/upload"
        files = {'file': open(file_path, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            return response.json().get('uid')
        else:
            raise Exception(f"Upload failed with status code {response.status_code}")

    def status(self, uid):
        """
        Retrieves the status of an upload from the web API.

        :param uid: The UID (unique identifier) of the upload.
        :return: A Status object representing the status of the upload.
        :raises Exception: If the status retrieval fails with a non-200 status code.
        """
        url = f"{self.base_url}/status/{uid}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Status(data['status'], data['filename'], data['timestamp'], data['explanation'])
        else:
            raise Exception(f"Status retrieval failed with status code {response.status_code}")
