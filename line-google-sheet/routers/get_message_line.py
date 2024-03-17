from fastapi import APIRouter, Request
import json, requests, datetime

from core.settings import CUS_PREFIX
from core.LINE import LineBot
from linebot.models import MessageEvent, TextMessage
from core.dependencies import test_google

_PATH = f"/receive_message/{CUS_PREFIX}"

router = APIRouter(tags=["Check"])

CHANNEL_ACCESS_TOKEN = 'aRK4D6ECg7cryUb9B8AIJzvIijaj4LPARRNbTzEZ0bfitG4omYi64PdmSBy/XIFqVinKEhqIVgugHiHtHJHvgHcm7ZmhRwg06QfJ8wf/o/HKhFGXK2/spo89NP8bWFtuiIvsUp9g8Gm+ArhwqTvwfgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '3b4f7e8b0672b2052fc5066bc824c15c'

line_bot = LineBot(CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET)

@router.post(_PATH, status_code=201)
async def message_line(request: Request):
    res = await line_bot.handle_webhook(request)
    val = {
        "datetime":"",
        "no":"",
        "ship":"",
        "ship_name":"",
        "ship_phone":"",
        "ship_cod":"",
        "receive_name":"",
        "receive_address":"",
        "receive_phone":"",
        "product":"",
        "cod":"",
    }
    text = ""
    if res:
        body = await request.body()
        body = body.decode()
        body = json.loads(body)
        events = body["events"]
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]
    timestamp = events[0]["timestamp"]
    dt_object = datetime.datetime.fromtimestamp(timestamp / 1000)
    formatted_datetime = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    val["datetime"] = formatted_datetime
    for txt in text.split("\n"):
        if txt.find(":") != -1:
            tx = txt.split(":", maxsplit=1)
            if tx[0] == "ลำดับ":
                val["no"] = tx[1]
            elif tx[0] == "ผู้ส่ง":
                val["ship"] = tx[1]
            elif tx[0] == "ชื่อผู้ส่ง":
                val["ship_name"] = tx[1]
            elif tx[0] == "เบอร์โทรผู้ส่ง":
                val["ship_phone"] = tx[1]
            elif tx[0] == "rCOD":
                val["ship_cod"] = tx[1]
            elif tx[0] == "ผู้รับ":
                val["receive_name"] = tx[1]
            elif tx[0] == "ที่อยู่":
                val["receive_address"] = tx[1]
            elif tx[0] == "เบอร์โทรผู้รับ":
                val["receive_phone"] = tx[1]
            elif tx[0] == "สินค้า":
                val["product"] = tx[1]
            elif tx[0] == "pCOD":
                val["cod"] = tx[1]
    rows = []
    rows.append(val["datetime"])
    rows.append(val["no"])
    rows.append(val["ship"])
    rows.append(val["ship_name"])
    rows.append(val["ship_phone"])
    rows.append(val["ship_cod"])
    rows.append(val["receive_name"])
    rows.append(val["receive_address"])
    rows.append(val["receive_phone"])
    rows.append(val["product"])
    rows.append(val["cod"])
    test_google("sheet1","https://docs.google.com/spreadsheets/d/1_tStTrf_53QOXFxE6rSU3Can8e4zVJGuAfWSI_SkZ2I/edit?usp=sharing",[rows])

    # Process each event
    responses = []
    str_reply_message = "Update Done."
    line_bot.handle_text_message(events[0]["replyToken"],str_reply_message)

    # Return the response(s) as JSON
    return "OK"

@router.get(_PATH, status_code=200)
async def message_line(request: Request):
    return "OK"