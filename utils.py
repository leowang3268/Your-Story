import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage


channel_access_token = os.getenv(
    "LINE_CHANNEL_ACCESS_TOKEN", "Qz7htfBX3N2xPvqqlFCjD/k5sANOj33rgXp/4tNVVFTPUry1BFvQfrvw8dEEzsPp4yTSFtgNkP84seW6BUb8m7kvy1qDVjslDa2pfamLvc6TtS1YuTWYC2rhbyivUNqap8WijQZ5NoMhKJGeV6Tf5AdB04t89/1O/w1cDnyilFU=")


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
