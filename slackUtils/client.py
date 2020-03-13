import logging
import os
import json
from slackclient import SlackClient

class Client:
    def __init__(self):
        SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
        self._client = SlackClient(SLACK_BOT_TOKEN)
        logging.debug("[Slack] Authorized slack client")

    def sendMessage(self, msg):
        updateMsg = self._client.api_call("chat.postMessage",
            channel='#pruebas', text=msg).decode('utf-8')
        obj = json.loads(updateMsg)
        if obj['ok'] is not True:
            logging.error(updateMsg)
        else:
            logging.debug(updateMsg)