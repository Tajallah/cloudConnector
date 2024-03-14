import requests
from os import environ
import base64
import rsa

keypath = environ.get('KEY_PATH')
private_key = open(keypath, 'rb').read()
private_key = rsa.PrivateKey.load_pkcs1(private_key)

testing_url = "http://localhost:8101/chat"
test_content = "test"

import base64

def encrypt_test_content():
    return rsa.encrypt(test_content.encode(), private_key)

def sign_test_content():
    signature = rsa.sign(test_content.encode(), private_key, 'SHA-1')
    return base64.b64encode(signature).decode()

payload = {
    "role": "user",
    "content": base64.b64encode(encrypt_test_content()).decode(),
    "mode": "test",
    "character": "test",
    "signature": sign_test_content()
}

def test_get():
    print(payload)
    response = requests.post(testing_url, json=payload)
    print(response.text)
    assert response.status_code == 200

test_get()