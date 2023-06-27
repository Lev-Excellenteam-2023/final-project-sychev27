import os
import subprocess
import time
from handling_presentations import extract_text_from_presentation
from handling_api import api_request
from web_api import app
from client import WebApiClient

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Start the Web API
api_process = subprocess.Popen(['python', 'web_api.py'])

# Wait for the Web API to start
time.sleep(2)

# Start the Explainer
explainer_process = subprocess.Popen(['python', 'explainer.py'])

# Wait for the Explainer to start
time.sleep(2)

# Create an instance of the Web API client
client = WebApiClient('http://localhost:5000')

# Define the path to the sample presentation
sample_presentation_path = '../Tests.pptx'

# Upload the sample presentation
uid = client.upload(sample_presentation_path)
print(f"Uploaded file with UID: {uid}")

# Wait for the processing to complete
time.sleep(5)

# Check the status of the uploaded presentation
status = client.status(uid)
if status.is_done():
    print("Upload processing is done")
    print("Explanation:", status.explanation)
else:
    print("Upload is still pending")

# Stop the Explainer
explainer_process.terminate()

# Stop the Web API
api_process.terminate()

# Print the contents of the outputs folder
output_files = os.listdir(app.config['OUTPUT_FOLDER'])
print("Output files in the outputs folder:")
for file_name in output_files:
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], file_name)
    print(file_path)

# Clean up the uploads and outputs folders
uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
for file_name in uploaded_files:
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    os.remove(file_path)

output_files = os.listdir(app.config['OUTPUT_FOLDER'])
for file_name in output_files:
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], file_name)
    os.remove(file_path)