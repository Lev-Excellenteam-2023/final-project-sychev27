from flask import Flask, request, jsonify
from datetime import datetime
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}


@app.route('/upload', methods=['POST'])
def upload():
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
    # Check if the file exists
    uploads = os.listdir(app.config['UPLOAD_FOLDER'])
    matching_files = [filename for filename in uploads if uid in filename]

    if not matching_files:
        return jsonify({
            'status': 'not found',
            'filename': None,
            'timestamp': None,
            'explanation': None
        }), 404

    # Get details from the matching file
    matching_file = matching_files[0]
    original_filename, timestamp, _ = matching_file.split('_')
    explanation = 'Some processed output' if is_processed(matching_file) else None

    return jsonify({
        'status': 'done' if is_processed(matching_file) else 'pending',
        'filename': original_filename,
        'timestamp': timestamp,
        'explanation': explanation
    }), 200


def is_processed(filename):
    # Example function to determine if a file is processed
    # You can modify this based on your actual processing logic
    return True


if __name__ == '__main__':
    app.run()