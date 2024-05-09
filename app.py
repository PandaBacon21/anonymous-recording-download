import json
import requests
import os
from dotenv import load_dotenv

from utils.get_token import token

load_dotenv()

# retrieve the access token
ACCESS_TOKEN = token()

TARGET_EMAIL = os.environ.get('TARGET_EMAIL')
TARGET_AUTO_RECEPTIONIST = os.environ.get('TARGET_AUTO_RECEPTIONIST')
VOICEMAIL_DOWNLOAD_LOCATION = os.environ.get('VOICEMAIL_DOWNLOAD_LOCATION')
BASE_URL = 'https://api.zoom.us/v2'
HEADERS = {
        'content-type': 'application/json',
        'authorization': f'Bearer {ACCESS_TOKEN}'
    }

def get_user():
    endpoint = '/users'
    full_url = BASE_URL+endpoint
    response = requests.get(url=full_url, headers=HEADERS)

    print(f'endpoint: {endpoint}, status code: {response.status_code}')

    r_content = json.loads(response.content)
    target = next((item for item in r_content['users'] if item['email'] == TARGET_EMAIL), None)
    # print(f"userId: {target['id']}")
    return(target['id'])

def get_user_voicemail(userId):
    endpoint = f'/phone/users/{userId}/voice_mails'
    full_url = BASE_URL+endpoint
    response = requests.get(url=full_url, headers=HEADERS)

    print(f'endpoint: {endpoint}, status code: {response.status_code}')

    r_content = json.loads(response.content)
    return r_content['voice_mails']

def get_anonymous_auto_receptionist_voicemail(voicemail_array):
    anonymous_auto_receptionist_voicemails = []
    for item in voicemail_array: 
        if item['callee_name'] == TARGET_AUTO_RECEPTIONIST: 
            anonymous_auto_receptionist_voicemails.append({'date_time':item['date_time'], 'download_url':item['download_url']})
    # print(f'download urls: {anonymous_auto_receptionist_voicemails}')
    return anonymous_auto_receptionist_voicemails

def download_voicemails(recording_url_array):
    download_dir = VOICEMAIL_DOWNLOAD_LOCATION
    os.makedirs(download_dir, exist_ok=True)
    for url in recording_url_array:
        file_name = f"{url['date_time']}.mp3"
        full_filename = f'{download_dir}/{file_name}'
        response = requests.get(url['download_url'], headers=HEADERS)
        with open(full_filename, 'wb') as f: 
            f.write(response.content)
            print(f'Recording {file_name}: download complete')

def main(): 
    userId = get_user()
    recording_array = get_anonymous_auto_receptionist_voicemail(get_user_voicemail(userId))
    download_voicemails(recording_array)

if __name__ == '__main__': 
    main()