# from flask import Flask, jsonify, render_template_string, request, redirect, url_for
# import os
# import uuid
# from pydub import AudioSegment
# import requests
# from groq import Groq

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# client = Groq(api_key=os.environ.get("transcription_key"))

# def transcribe_audio(file_path):
#     with open(file_path, 'rb') as audio_file:
#         transcription = client.audio.transcriptions.create(
#             file=(file_path, audio_file.read()),
#             model="whisper-large-v3",
#             prompt="A user will list out a series of topics, specified either by number or by name. Topics may include '463', '220', '525', '528', 'Research', 'Jobs', 'Grad School', '523 TA', '533 TA', '414 TA', and 'Other'. For each topic, a user will specify what tasks need to be done. The user may also specify whether this is an important task, and the due date of the task if there is one. Output a JSON file where the keys are the topics. Each key's value will include a 'tasks' dictionary, in which you append relevant annotated information about the subtasks for each task. Also need to include an 'important' flag and a date string.",  # Optional
#             response_format="json",  # Optional
#             language="en",  # Optional
#             temperature=0.0  # Optional
#         )
    
#     print(transcription)
#     return transcription.text

# @app.route('/fetch-transcription', methods=['POST'])
# def index():
#     if request.method == 'POST':
#         if 'audio' not in request.files:
#             return jsonify({'error': 'No file part'}), 400
        
#         file = request.files['audio']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
        
#         # Save the file temporarily
#         unique_filename = f"{uuid.uuid4().hex}.wav"
#         file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
#         file.save(file_path)
        
#         # Call the transcription function
#         result = transcribe_audio(file_path)

#         # Clean up the file after processing
#         os.remove(file_path)
        
#         # Return the transcription result
#         if result:
#             return jsonify({'transcription': result}), 200
#         else:
#             return jsonify({'error': 'Error transcribing audio'}), 400

#     # Render a simple HTML template for audio upload and recording
#     html_template = '''
#     <!doctype html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <title>Record Audio</title>
#         <script>
#             let mediaRecorder;
#             let audioChunks = [];

#             async function startRecording() {
#                 const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
#                 mediaRecorder = new MediaRecorder(stream);

#                 mediaRecorder.ondataavailable = event => {
#                     audioChunks.push(event.data);
#                 };

#                 mediaRecorder.onstop = async () => {
#                     const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
#                     const formData = new FormData();
#                     formData.append('audio', audioBlob, 'recording.wav');
                    
#                     fetch('/', {
#                         method: 'POST',
#                         body: formData
#                     }).then(response => response.text()).then(data => {
#                         document.getElementById('result').innerText = data;
#                         if (data) {
#                             document.getElementById('listButton').style.display = 'block';
#                         }
#                     });

#                     audioChunks = [];
#                 };

#                 mediaRecorder.start();
#             }

#             function stopRecording() {
#                 mediaRecorder.stop();
#             }
#         </script>
#     </head>
#     <body>
#         <h1>Record or Upload an Audio File</h1>
#         <button onclick="startRecording()">Start Recording</button>
#         <button onclick="stopRecording()">Stop Recording</button>
#         <form method="POST" enctype="multipart/form-data">
#             <input type="file" name="audio" accept="audio/*">
#             <button type="submit">Upload</button>
#         </form>
#         <p id="result"></p>
#         <button id="listButton" style="display: none;" onclick="listEvents()">List Events</button>
#     </body>
#     </html>
#     '''
#     return render_template_string(html_template)

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000, debug=True)