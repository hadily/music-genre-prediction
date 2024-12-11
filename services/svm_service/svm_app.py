from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np 
import librosa
import os
from flask_cors import CORS

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'models', 'genre_model.pkl')

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})


# model_path = "./models/genre_model.pkl"
with open(model_path, 'rb') as f:
    # model = pickle.load(f)
    model = f.read()

# @app.route('/', methods=['GET'])
# def get():
#    return("hello svm_model")

# @app.route('/')
# def upload_form():
#     return render_template('upload.html')

@app.route('/')
def index():
    return "Welcome to the Music Genre Prediction App! Use /predict for predictions."

def extract_features(file_path):
    """Extracts features from the audio file using Mel-spectrogram."""
    try:
        y, sr = librosa.load(file_path, mono=True)
    
        # Generate Mel-spectrogram with reduced number of mel bins to match the expected feature size
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=40, fmax=8000)  # Reduce n_mels to 40
        
        # Convert to decibels
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # If necessary, downsample the spectrogram to reduce the feature vector length
        # Flatten the spectrogram to create a feature vector
        mel_spec_db_flattened = mel_spec_db.flatten()
        
        # If the flattened vector has more than 1280 features, trim it; if less, pad it
        target_size = 1280
        if len(mel_spec_db_flattened) > target_size:
            mel_spec_db_flattened = mel_spec_db_flattened[:target_size]
        elif len(mel_spec_db_flattened) < target_size:
            mel_spec_db_flattened = np.pad(mel_spec_db_flattened, (0, target_size - len(mel_spec_db_flattened)), 'constant')
    
        return mel_spec_db_flattened
    except Exception as e:
        print(f"Error during feature extraction: {e}")
        raise

@app.route('/predict', methods=['POST'])
def predict_genre():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # print(f"Received file: {file.filename}")  # Log file name
    
    # Save the file temporarily
    file_path = os.path.join("temp", file.filename)
    #os.makedirs("temp", exist_ok=True)

    # print(f"Saved file at: {file_path}")  # Log the file path
    
    try:        
        file.save(file_path)

        # Process the audio file and extract features
        features = extract_features(file_path)
        os.remove(file_path)  # Remove the temp file after processing
        
        print(f"Extracted features: {features[:10]}")  # Log extracted features
        
        # Make prediction using the model
        prediction = model.predict([features])
        genre = prediction[0]
        
        return {'genre': genre}
    
    except Exception as e:
        print(f"Error during prediction: {e}")  # Log the error
        return jsonify({'error': 'An error occurred during processing.'}, {e}), 500


if __name__ == '__main__':
    # os.makedirs("temp", exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)