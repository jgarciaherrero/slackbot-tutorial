import os
import schedule
import time
import logging
import json
import requests
from slackclient import SlackClient

logging.basicConfig(level=logging.DEBUG)

def sendMessage(slack_client, msg):
  # make the POST request through the python slack client
  try:
    response = requests.get("https://apict-gateway-vf.internal.vodafone.com/vodafone-spain/desarrollo/ping/ping", verify=False)
    print(response.status_code)
    if (response.status_code != 200):
      updateMsg = slack_client.api_call(
        "chat.postMessage",
        channel='#pruebas',
        text="Error al invocar el ping en Desarrollo"
      ).decode('utf-8')
      obj = json.loads(updateMsg)
      # check if the request was a success
      if obj['ok'] is not True:
        logging.error(updateMsg)
      else:
        logging.debug(updateMsg)
  except:
    logging.error("Ha ocurrido una excepción")
    updateMsg = slack_client.api_call(
      "chat.postMessage",
      channel='#pruebas',
      text="Error al invocar el ping en Desarrollo"
    ).decode('utf-8')

if __name__ == "__main__":
  SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
  slack_client = SlackClient(SLACK_BOT_TOKEN)
  logging.debug("authorized slack client")

  # # For testing
  msg = "¡Buenos dias!"
  schedule.every(10).seconds.do(lambda: sendMessage(slack_client, msg))

  # schedule.every().monday.at("13:15").do(lambda: sendMessage(slack_client, msg))
  logging.info("Entrando en el bucle")

  while True:
    schedule.run_pending()
    time.sleep(5) # sleep for 5 seconds between checks on the scheduler
