from fastapi import FastAPI
import json
import random
import urllib.request
from pydantic import BaseModel
from base_xmlrpc import xmlrpc_odoo

### SET Default
odoo_token_api = "c6099dc770c53936edaafa65f720ebfd000fa2b6"
HOST = 'odoo16.majin.xyz'
PORT = 20001
DB = 'odoo16_test'
USER = 'saharat.iamjaeng@gmail.com'
PASS = odoo_token_api if odoo_token_api else 'majinsblabla'
url_com = "https://%s/xmlrpc/2/common" % (HOST)
url_obj = "https://%s/xmlrpc/2/object" % (HOST)
test = True

### TEST Function
def case_test():
    global DB,USER,PASS,url_com,url_obj
    conn_api = xmlrpc_odoo(DB,USER,PASS,url_com,url_obj)
    conn_uid = conn_api.login()
    test1 = conn_api.call_method("res.partner", "check_access_rights", ['read'], {'raise_exception': False})
    print("Test : call_methed :",test1) ### Test call function
    test2 = conn_api.call_list("res.partner", [[['is_company', '=', True]]], limit=3) ### Test read all
    print("Test : call_count :",test2) ### Test read all
    test3 = conn_api.call_search_read("res.partner", [[['is_company', '=', True]]], {'fields': ['name', 'country_id', 'comment'], 'limit': 5})
    print("Test : call_search_read :",test3)
    args = [{
            'color': 8,
            'memo': 'This is another note TEST111',
            'create_uid': conn_uid,
        }]
    test4 = conn_api.call_create("note.note", args) ### Create
    print("Test : call_create :",test4,args)
    test5 = conn_api.call_read("note.note",[[test4]],fields=["color","memo"])
    print("Test : call_raed :", test5)
    test6 = conn_api.call_write("note.note",test4,[[test4], {"color":4, "memo": "Test call_write"}])
    print("Test : call_write :", test6)
    test7 = conn_api.call_delete("note.note",test4)
    print("Test : call_delete :",test7)

class Note(BaseModel):
    color: int
    memo: str

class Login(BaseModel):
    user: str
    password: str

class Transfer(BaseModel):
    partner_id: int
    picking_type_id: int
    origin: str

if test:
    case_test()

app = FastAPI()

@app.post("/api/notes")
async def create_note(note: Note, login: Login):
    global DB,USER,PASS,url_com,url_obj
    conn_api = xmlrpc_odoo(DB,USER,PASS,url_com,url_obj)
    conn_uid = conn_api.login()
    # create a new note
    args = {
        'color': note.color,
        'memo': note.memo,
        'create_uid': conn_uid,
    }
    note_id = conn_api.call_create("note.note", args)
    return {"id": note_id}

@app.post("/api/transfers")
async def create_note(transfer: Transfer, login: Login):
    global DB,USER,PASS,url_com,url_obj
    conn_api = xmlrpc_odoo(DB,USER,PASS,url_com,url_obj)
    conn_uid = conn_api.login()
    # create a new note
    args = {
        'partner_id': transfer.partner_id,
        'picking_type_id': transfer.picking_type_id,
        #'move_type': transfer.move_type,
        #'location_id': transfer.location_id,
        #'location_dest_id': transfer.location_dest_id,
        'origin': transfer.origin,
        'create_uid': conn_uid,
    }
    transfer_id = conn_api.call_create("note.note", args)
    return {"id": transfer_id}

