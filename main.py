from fastapi import FastAPI
from pydantic import BaseModel
import requests
import base64
from os import environ
import rsa

keypath = environ.get('KEY_PATH')
print(keypath)
private_key = open(keypath, 'rb').read()
public_key = open(keypath + ".pub", 'rb').read()
private_key = rsa.PrivateKey.load_pkcs1(private_key)
public_key = rsa.PublicKey.load_pkcs1(public_key)

llmServerLocation = environ.get('LLM_SERVER_LOCATION')

if llmServerLocation is None or keypath is None:
    print("Please set the environment variables LLM_SERVER_LOCATION and KEY_PATH")
    exit(1)

def decryptChatMsg(msg: bytes):
    return rsa.decrypt(base64.b64decode(msg), private_key)

def verifyChatMsg(msg: bytes, signature: bytes):
    return rsa.verify(decryptChatMsg(msg), base64.b64decode(signature), public_key)

#manual page that describes the proper use of the API
manPage = """LLM CLOUD CONNECTOR API
\n
\n
Used to connect to the LLM server and send and receive chat messages\n
--------------------------------------------------------------------
\n
\n
Routes:\n
"""

#dataModel
class ChatMsg(BaseModel):
    role: str
    content: str
    mode: str
    character: str
    signature: str

app = FastAPI()

@app.get("/")
def readRoot():
    return {"message" : "You don't belong here. Ask your admin for the right path"}

@app.get("/man")
def readManPage(cht: ChatMsg):
    if verifyChatMsg(cht.content, cht.signature):
        return {
            "role": cht.role,
            "content": decryptChatMsg(cht.content).decode('utf-8'),
            "mode": cht.mode,
            "character": cht.character,
            "signature": cht.signature
        }

@app.get("/status")
def readStatus():
    llmCheck = requests.get(llmServerLocation)
    if llmCheck.status_code == 200:
        return {"status": "ok"}
    else:
        return {
            "status": "error",
            "message": "LLM Server is not reachable",
            "status_code": llmCheck.status_code,
            "info": llmCheck.text
        }

@app.post("/chat")
def extractChatMsg(cht: ChatMsg):
    if verifyChatMsg(cht.content, cht.signature):
        return {
            "role": cht.role,
            "content": decryptChatMsg(cht.content).decode('utf-8'),
            "mode": cht.mode,
            "character": cht.character,
            "signature": cht.signature
        }
    else:
        return {
            "role": cht.role,
            "content": "Invalid Signature",
            "mode": cht.mode,
            "character": cht.character,
            "signature": cht.signature
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8101)

#def parseChatMsg()

