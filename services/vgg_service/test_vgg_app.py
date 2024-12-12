import pytest
import io
from io import BytesIO
import sys
import os
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vgg_app import app 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict_valid_file(client):
    # Path to the test audio file
    audio_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'disco.00004.wav')

    # Open the audio file and send it in the POST request
    with open(audio_file_path, 'rb') as audio_file:
        data = {
            'file': (BytesIO(audio_file.read()), 'disco.00004.wav')
        }

        response = client.post('/predict', data=data, content_type='multipart/form-data')

        # Check if the response is valid
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert b"predicted_genre" in response.data, "Response does not contain 'predicted_genre'"

def test_predict_no_file_provided(client):
    # Send a POST request without any file
    response = client.post('/predict', data={}, content_type='multipart/form-data')
    
    # Assert that the status code is 400
    assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
    
    # Assert that the response contains the expected error message
    assert b"No file part" in response.data, "Error message for missing file is incorrect or not present"
