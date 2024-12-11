from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import librosa
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import os
import unicodedata

app = Flask(__name__)
CORS(app)  # Enable CORS for the app

@app.route('/')
def upload_form():
    return render_template('upload.html')


model_path = "./models/vgg19_model.h5"# Configuring the upload folder
UPLOAD_FOLDER = 'temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the model (make sure the model path is correct)
model = load_model(model_path)  # Replace with your model path

# List of genres used during training (replace with your actual genre list)
genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
encoder = LabelEncoder()
encoder.fit(genres)

# Function to extract features from the audio file
def extract_features(file_path):
    try:
        # Load the .wav file using librosa
        y, sr = librosa.load(file_path, sr=None, mono=True)
        print(f"Loaded file {file_path} with {y.shape[0]} samples, Sample rate: {sr}")

        # Extract features (Zero Crossing Rate, Spectral Centroid, etc.)
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85))
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)

        # Return the concatenated feature vector
        return np.hstack([mfcc, [zcr, centroid, rolloff]])
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to sanitize filenames and full path to avoid encoding issues
def safe_filename(filename):
    try:
        # Normalize the filename and remove any non-ASCII characters
        sanitized_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
        return sanitized_filename
    except UnicodeEncodeError as e:
        print(f"Error sanitizing filename {filename}: {e}")
        return None

def safe_file_path(file_path):
    """
    Ensure the entire path is safe for saving on the system.
    """
    sanitized_path = os.path.normpath(file_path)  # Normalize the file path
    return sanitized_path

@app.route('/predict', methods=['POST'])
def predict():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

   
    if not file.filename.endswith('.wav'):
        return jsonify({'error': 'Only .wav files are supported'}), 400

    
    safe_filename_value = safe_filename(file.filename)
    if safe_filename_value is None:
        return jsonify({'error': 'Error sanitizing filename'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename_value)
    file_path = safe_file_path(file_path)

    try:
        file.save(file_path)
    except UnicodeEncodeError as e:
        return jsonify({'error': f"Error saving file: {e}"}), 400

    features = extract_features(file_path)
    if features is not None:
        features = features / np.max(features)  
        features = features.reshape(1, -1)  
        prediction = model.predict(features)  
        predicted_genre = encoder.inverse_transform([np.argmax(prediction)])  
        return jsonify({'predicted_genre': predicted_genre[0]})
    else:
        return jsonify({'error': 'Error processing audio file'}), 400

if __name__ == '__main__':
    os.makedirs("temp", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5001)