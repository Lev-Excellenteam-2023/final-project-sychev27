
import asyncio
import time
import os
import json
from handling_presentations import extract_text_from_presentation
from handling_api import api_request

CONTENT = "Text below from presentation slide give me a short explanation about this topic\n"
UPLOADS_FOLDER = 'uploads'
OUTPUTS_FOLDER = 'outputs'


async def handle_file(file_path):
    """
    Handle a presentation file.

    Args:
        file_path (str): The path to the presentation file.

    Returns:
        None
    """
    file_name = os.path.basename(file_path)
    extracted_text = extract_text_from_presentation(file_path)
    results = await asyncio.gather(*(api_request(CONTENT, extracted_text[i]) for i in range(2)))

    # Prepare JSON object with results and file information
    result_json = {
        'file_name': file_name,
        'explanation': results
    }

    # Create output file path
    output_file_path = os.path.join(OUTPUTS_FOLDER, file_name.replace('pptx', 'json'))

    # Write results to JSON file
    with open(output_file_path, 'w') as output_file:
        output_file.write(json.dumps(result_json))

    print(f"Handled file: {file_name}")


async def monitor_uploads_folder():
    """
    Monitor the uploads folder for new presentation files and handle them.

    Returns:
        None
    """
    while True:
        # Check for files in the uploads folder
        files = os.listdir(UPLOADS_FOLDER)

        if files:
            # Handle each file found
            for file_name in files:
                parts_of_file_name = file_name.split('_')
                file_path = os.path.join(UPLOADS_FOLDER, file_name)

                # Debug print
                print(F"File with the path {file_path} will be handling")

                # Exclude certain file and process only .pptx files
                if parts_of_file_name[0].lower().endswith('.pptx') and file_name != 'exclude.pptx':
                    await handle_file(file_path)

                # Remove the file from the uploads folder
                os.remove(file_path)

                # Pause for 15 seconds between iterations
                await asyncio.sleep(10)


if __name__ == '__main__':
    # Create the outputs folder if it doesn't exist
    if not os.path.exists(OUTPUTS_FOLDER):
        os.makedirs(OUTPUTS_FOLDER)

    loop = asyncio.get_event_loop()
    loop.create_task(monitor_uploads_folder())
    loop.run_forever()


