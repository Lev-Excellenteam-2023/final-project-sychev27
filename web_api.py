from flask import Flask, request, jsonify
from datetime import datetime
import os
import uuid
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'pptx'}


@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle file upload requests.

    Returns a JSON response containing the UID (unique identifier) of the uploaded file.

    Returns:
        A JSON response containing the UID if the upload is successful, or an error message with a 400 status code.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file attached'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Generate a unique filename
    original_filename = file.filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    uid = str(uuid.uuid4().hex)
    new_filename = f"{original_filename}_{timestamp}_{uid}"

    # Save the file to the uploads folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

    return jsonify({'uid': uid}), 200


@app.route('/status/<uid>', methods=['GET'])
def status(uid):
    """
    Retrieve the status of an uploaded file.

    Args:
        uid (str): The UID (unique identifier) of the uploaded file.

    Returns:
        A JSON response containing the status, filename, timestamp, and explanation of the uploaded file,
        or a 'not found' message with a 404 status code if the file is not found.
    """
    # Check if the file exists
    uploads = os.listdir(app.config['UPLOAD_FOLDER'])
    outputs = os.listdir(app.config['OUTPUT_FOLDER'])
    matching_upload_files = [filename for filename in uploads if uid in filename]
    matching_output_files = [filename for filename in outputs if uid in filename]

    if not matching_upload_files and not matching_output_files:
        return jsonify({
            'status': 'not found',
            'filename': None,
            'timestamp': None,
            'explanation': None
        }), 404

    # Get details from the matching file
    matching_file = matching_upload_files[0] if matching_upload_files else matching_output_files[0]
    original_filename, timestamp, _ = matching_file.split('_')
    if matching_output_files:
        # Assuming you have a JSON file named 'data.json' in the outputs folder
        file_path = 'outputs/' + matching_output_files[0]

        # Read the JSON file and load its content into a dictionary
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Access the value using the key
        explanation = data['explanation']
    else:
        explanation = None

    return jsonify({
        'status': 'done' if matching_output_files else 'pending',
        'filename': original_filename,
        'timestamp': timestamp,
        'explanation': explanation
    }), 200


if __name__ == '__main__':
    app.run()