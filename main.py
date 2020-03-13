import schedule
import time
import logging
from apiConnect import EstadoPingAPI as ping
from slackUtils import client as slack

def checkPing(pings, slack):
    for ping in pings:
        resul = ping.ping()
        logging.error('[checkPing]' + resul)
        if (resul != ''):
            slack.sendMessage('Changed message: ' + resul)

pings = []
pings.append(ping.EstadoPingAPI('pre', 'sandbox'))
pings.append(ping.EstadoPingAPI('pre', 'desarrollo'))
pings.append(ping.EstadoPingAPI('pre', 'sit-1'))
pings.append(ping.EstadoPingAPI('pre', 'sit-2'))
pings.append(ping.EstadoPingAPI('pre', 'pprd'))
pings.append(ping.EstadoPingAPI('pro', 'sandbox'))
slack = slack.Client()
checkPing(pings, slack)
schedule.every(60).seconds.do(lambda: checkPing(pings, slack))
while True:
  schedule.run_pending()
  time.sleep(5) # sleep for 5 seconds between checks on the scheduler
