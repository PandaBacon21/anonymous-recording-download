import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

DB_LOCATION = os.environ.get('DB_LOCATION')

def connect_db():
    con = sqlite3.connect(f'{DB_LOCATION}')
    cur = con.cursor()
    # create the tokens table
    cur.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name = 'tokens' '''
    )
    if cur.fetchone()[0] == 1:
        print('Token Table Exists')
    else: 
        print('Tokens Table Does NOT Exist. Creating Table')
        cur.execute('CREATE TABLE tokens(uuid INTEGER UNIQUE, token TEXT, expire TEXT)')
