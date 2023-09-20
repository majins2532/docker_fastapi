from fastapi import FastAPI, Header, HTTPException, BackgroundTasks, Depends
from fastapi.logger import logger
from base_xmlrpc import xmlrpc_odoo
from logger import logger,func_log
import os
from dotenv import load_dotenv

### Load env
load_dotenv('.config.env')

### SET Default
token = os.getenv('x-token')
os.getenv('odoo_token_api')
odoo_token_api = os.getenv('odoo_token_api')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB = os.getenv('DB')
USER = os.getenv('USER')
PASS = os.getenv('PASS')
http_type = os.getenv('http_type')

print(DB, USER, PASS, HOST, None, http_type)
odoo = xmlrpc_odoo(DB, USER, PASS, HOST, None, http_type)
odoo.connect()

def write_log(message: str):
    func_log.info(message)

app = FastAPI()

@app.get("/api/v1/check_connect")
def check_connect(x_token: str | None = Header(default=None)):
    if x_token != token:
        write_log(f"GET: /api/v1/check_connect | Code : 498")
        raise HTTPException(status_code=498, detail="Invalid x_token")
    write_log(f"GET: /api/v1/check_connect")
    res = None
    res = odoo.version_odoo()
    return res