import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from utils import send_text_message
from fsm import TocMachine
load_dotenv()


app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET",
                           None)
channel_access_token = os.getenv(
    "LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


# FSM
machine = TocMachine(
    states=["user", "jail", "backdoor", "hall", "kitchen", "explore_kitchen", "sword_room", "armor_room",
            "bedroom", "explore_bedroom", "secret_room", "wrong_answer", "correct_answer", "outside", "lawn", "gate", "warehouse", "dead", "win"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "jail",
            "conditions": "is_going_to_jail",
        },
        {
            "trigger": "advance",
            "source": "jail",
            "dest": "backdoor",
            "conditions": "is_going_to_backdoor",
        },

        {
            "trigger": "advance",
            "source": "jail",
            "dest": "kitchen",
            "conditions": "is_going_to_kitchen",
        },
        {
            "trigger": "advance",
            "source": "kitchen",
            "dest": "jail",
            "conditions": "is_going_to_jail",
        },
        {
            "trigger": "advance",
            "source": "kitchen",
            "dest": "explore_kitchen",
            "conditions": "is_going_to_explore_kitchen",
        },
        {
            "trigger": "advance",
            "source": "jail",
            "dest": "hall",
            "conditions": "is_going_to_hall",
        },
        {
            "trigger": "advance",
            "source": "hall",
            "dest": "sword_room",
            "conditions": "is_going_to_sword_room",
        },
        {
            "trigger": "advance",
            "source": "sword_room",
            "dest": "outside",
            "conditions": "is_going_to_outside",
        },
        {
            "trigger": "advance",
            "source": "sword_room",
            "dest": "secret_room",
            "conditions": "is_going_to_secret_room",
        },
        {
            "trigger": "advance",
            "source": "hall",
            "dest": "armor_room",
            "conditions": "is_going_to_armor_room",
        },
        {
            "trigger": "advance",
            "source": "hall",
            "dest": "bedroom",
            "conditions": "is_going_to_bedroom",
        },
        {
            "trigger": "advance",
            "source": "bedroom",
            "dest": "explore_bedroom",
            "conditions": "is_going_to_explore_bedroom",
        },
        {
            "trigger": "advance",
            "source": "bedroom",
            "dest": "hall",
            "conditions": "is_going_to_hall",
        },
        {
            "trigger": "advance",
            "source": "armor_room",
            "dest": "outside",
            "conditions": "is_going_to_outside",
        },
        {
            "trigger": "advance",
            "source": "armor_room",
            "dest": "secret_room",
            "conditions": "is_going_to_secret_room",
        },
        {
            "trigger": "advance",
            "source": "secret_room",
            "dest": "wrong_answer",
            "conditions": "is_going_to_wrong_answer",
        },
        {
            "trigger": "advance",
            "source": "secret_room",
            "dest": "correct_answer",
            "conditions": "is_going_to_correct_answer",
        },
        {
            "trigger": "advance",
            "source": "correct_answer",
            "dest": "outside",
            "conditions": "is_going_to_outside",
        },
        {
            "trigger": "advance",
            "source": "outdoors",
            "dest": "lawn",
            "conditions": "is_going_to_lawn",
        },
        {
            "trigger": "advance",
            "source": "outdoors",
            "dest": "gate",
            "conditions": "is_going_to_gate",
        },
        {
            "trigger": "advance",
            "source": "outdoors",
            "dest": "warehouse",
            "conditions": "is_going_to_warehouse",
        },
        {
            "trigger": "advance",
            "source": ["gate", "lawn", "wrong_answer"],
            "dest": "dead",
            "conditions": "is_going_to_dead",
        },
        {
            "trigger": "advance",
            "source": ["gate", "lawn", "warehouse"],
            "dest": "win",
            "conditions": "is_going_to_win",
        },
        {
            "trigger": "advance",
            "source": ["win", "dead"],
            "dest": "user",
            "conditions": "is_going_to_user",
        },

        {
            "trigger": "back",
            "source": "backdoor",
            "dest": "jail",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        # line_bot_api.reply_message(
        #     event.reply_token, TextSendMessage(text=event.message.text)
        # )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        # Advance the FSM for each MessageEvent
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw(
        "fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ['PORT']
    app.run(host="0.0.0.0", port=port, debug=True)
