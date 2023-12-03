import os
from flask import Flask, request, jsonify, send_file
import sys

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    filename = request.args.get("filename")
    recording_directory = "/home/azureuser/jitsi/jitsi-meet-cfg/jibri/recordings/"

    matching_files = []
    directories_searched = []

    # Traverse the recording_directory and search for files with similar names
    for root, _, files in os.walk(recording_directory):
        directories_searched.append(root)
        for file in files:
            if filename in file:
                file_path = os.path.join(root, file)
                matching_files.append(file_path)

    if not matching_files:
        return "No matching files found", 404

    # Generate a list of dictionaries containing file information (name, size, and path)
    file_info = []
    for file_path in matching_files:
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        directory = os.path.dirname(file_path)
        file_info.append({"name": file_name, "size_bytes": file_size, "directory": directory})

    # Generate download URLs for all matching files
    download_urls = [f"https://recordings.convenevc.com:8443/download_file?path={file_path}" for file_path in matching_files]

    response_data = {
        "file_info": file_info,
        "download_urls": download_urls,
        "directories_searched": directories_searched,
    }

    return jsonify(response_data)

@app.route("/download_file", methods=["GET"])
def download_file():
    file_path = request.args.get("path")

    if not os.path.exists(file_path):
        return "File not found", 404

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

