import logging
import requests
import json
from datetime import date

class EstadoPingAPI:
    def __init__(self, env, catalog):
        self._state = 'INITIAL'
        self._status = 200
        self._text = ''
        self._env = env
        if (env == 'pro'):
            self._gw = 'apicp-gateway-vf.internal.vodafone.com'
        else:
            self._gw = 'apict-gateway-vf.internal.vodafone.com'
        self._catalog = catalog

    def ping(self):
        resul = ''
        try:
            response = requests.get("https://" + self._gw + "/vodafone-spain/"
                + self._catalog + "/ping/ping", verify=False)
            if (response.status_code != self._status):
                resul = '[' + self._env + '][' + self._catalog + '][' + self._state + '] Status changed from ' + str(self._status) + ' to ' + str(response.status_code)
                self._status = response.status_code
                self._text = ''
            else:
                self._status = response.status_code
                if (response.status_code == 200):
                    txt = json.dumps(response.json())
                    state = self._state
                    self.evalFecha(response.json()["fecha"])
                    if (state != self._state or self._text != txt):
                        self._text = txt
                        resul = '[' + self._env + '][' + self._catalog + '][' + self._state + '] ' + txt
        except:
            logging.exception('Exception calling API')
            resul: 'Error de conexión'
        finally:
            return resul
    
    def evalFecha(self, fecha):
        if (len(fecha) and fecha[6:8] == date.today().strftime('%d')):
            self._state = 'OK'
        else:
            self._state = 'KO'
