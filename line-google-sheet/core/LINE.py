from fastapi import Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

class LineBot:
    def __init__(self, channel_access_token, channel_secret):
        self.line_bot_api = LineBotApi(channel_access_token)
        self.handler = WebhookHandler(channel_secret)

    def handle_text_message(self, reply_token, message_text):
        self.reply(reply_token, message_text)

    def reply(self, reply_token, text):
        self.line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    async def handle_webhook(self, request: Request):
        signature = request.headers['X-Line-Signature']
        body = await request.body()
        try:
            self.handler.handle(body.decode(), signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        return True