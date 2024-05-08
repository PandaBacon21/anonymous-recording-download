import os
import base64
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sqlite3

from .connect_db  import connect_db

load_dotenv()

ACCOUNT_ID = os.environ.get('ACCOUNT_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
DB_LOCATION = os.environ.get('DB_LOCATION')

BASE_URL = 'https://api.zoom.us/v2/'
AUTH_URL = 'https://zoom.us/oauth/token'

message = f'{CLIENT_ID}:{CLIENT_SECRET}'
encoded = base64.b64encode(message.encode()).decode()

def get_new_token():
    con = sqlite3.connect(f'{DB_LOCATION}')
    cur = con.cursor()

    headers = {
        'content-type': 'application/json',
        'authorization': f'Basic {encoded}'
    }
    FINAL_URL = f'{AUTH_URL}?grant_type=account_credentials&account_id={ACCOUNT_ID}'
    response = requests.post(url=FINAL_URL, headers=headers)
    r_content = json.loads(response.content)

    access_token = r_content['access_token']
    token_exp = datetime.now() + timedelta(seconds=r_content['expires_in'])

    cur.execute(
        'INSERT OR REPLACE INTO tokens(uuid, token, expire) VALUES (?,?,?)', (1, access_token, token_exp.strftime('%Y-%m-%d %H:%M:%S')) 
    )
    con.commit()
    cur.close()
    return access_token, token_exp.strftime('%Y-%m-%d %H:%M:%S')

def check_token_valid(token_exp):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if (token_exp < current_datetime):
        print('Token Is Expired. Retrieving New Token')
        return False
    else:
        print('Access Token Is Valid')
        return True
            
def token():
    connect_db()
    con = sqlite3.connect(f'{DB_LOCATION}')
    cur = con.cursor()
    try: 
        data = cur.execute('SELECT token, expire FROM tokens WHERE uuid = 1').fetchone()
        access_token = data[0]
        token_expire = data[1]
    except Exception as ex:
        print('Token Not In DB, fetching new token')
        access_token, token_expire = get_new_token()
    if check_token_valid(token_expire) == False:
        access_token,_ = get_new_token()
        return access_token
    else: 
        return access_token
