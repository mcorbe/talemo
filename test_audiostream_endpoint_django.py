from django.test import Client
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

# Create a test client
client = Client()

# Data to send in the request
data = {
    'prompt': 'This is a test prompt for audio streaming.'
}

# Make the POST request
response = client.post('/audiostream/start/', data=data, content_type='application/json')

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    response_data = response.json()
    
    # Check if the response contains a playlist URL
    if 'playlist' in response_data:
        print(f"Success! Received playlist URL: {response_data['playlist']}")
        
        # Verify the URL format
        expected_format = "/media/hls/"
        if expected_format in response_data['playlist'] and response_data['playlist'].endswith('/audio.m3u8'):
            print(f"URL format is correct: {response_data['playlist']}")
        else:
            print(f"URL format is incorrect. Expected format containing '{expected_format}' and ending with '/audio.m3u8'")
    else:
        print(f"Error: Response does not contain a playlist URL. Response: {response_data}")
else:
    print(f"Error: Request failed with status code {response.status_code}")
    print(f"Response: {response.content.decode()}")