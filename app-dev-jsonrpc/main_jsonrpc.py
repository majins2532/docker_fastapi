from fastapi import FastAPI
import json
import random
import urllib.request
from pydantic import BaseModel

odoo_token_api = "c6099dc770c53936edaafa65f720ebfd000fa2b6"
HOST = 'odoo16.majin.xyz'
PORT = 20001
DB = 'odoo16_test'
USER = 'saharat.iamjaeng@gmail.com'
PASS = 'majinsblabla'
#HOST="mp.almacom.co.th"
#PORT="" ## not use
#DB="demo"
#USER="admin"
#PASS="admin"
url = "https://%s/jsonrpc/" % (HOST)

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

class Note(BaseModel):
    color: int
    memo: str

class Login(BaseModel):
    user: str
    password: str

class Transfer(BaseModel):
    partner_id: int
    picking_type_id: int
    #move_type: str
    #location_id: int
    #location_dest_id: int
    origin: str

app = FastAPI()

@app.post("/api/notes")
async def create_note(note: Note, login: Login):
    global DB
    uid = call(url, "common", "login", DB, login.user, login.password)
    # create a new note
    args = {
        'color': note.color,
        'memo': note.memo,
        'create_uid': uid,
    }
    note_id = call(url, "object", "execute", DB, uid, login.password, 'note.note', 'create', args)
    return {"id": note_id}

@app.post("/api/transfers")
async def create_note(transfer: Transfer, login: Login):
    global DB
    uid = call(url, "common", "login", DB, login.user, login.password)
    # create a new note
    args = {
        'partner_id': transfer.partner_id,
        'picking_type_id': transfer.picking_type_id,
        #'move_type': transfer.move_type,
        #'location_id': transfer.location_id,
        #'location_dest_id': transfer.location_dest_id,
        'origin': transfer.origin,
        'create_uid': uid,
    }
    note_id = call(url, "object", "execute", DB, uid, login.password, 'stock.picking', 'create', args)
    return {"id": note_id}

