import logging
import requests
from requests.sessions import Request

import settings
logger = logging.getLogger('root')

class AppRegister:
    HOST = 'http://localhost:8001/'
    _data = None

    def set_data(self):
        if not settings.APP_ID:
            logger.critical('Set APP_ID to data')

        self._data = {
            'app': settings.APP_ID,
            'name': settings.NAME,
            'na_me': settings.NA_ME,
            'method': settings.CONFIG_WEBHOOK_METHOD,
            'callback_url': settings.CONFIG_WEBHOOK_URL
        }

    def send_register_request(self):
        self.set_data()
        response = None

        try:
            req = Request(
                method='POST',
                url=f'{self.HOST}auth/app_register',
                json=self._data
            )
            session = requests.sessions.session()
            response = session.send(req.prepare())

        except requests.exceptions.RequestException as e:
            pass
        finally:
            if response:
                assert response.status_code == 200, \
                    'App not register in identity'


    def send_unregister_request(self):
        self.set_data()
        response = None

        try:
            req = Request(
                method='POST',
                url=f'{self.HOST}auth/app_unregister',
                json=self._data
            )
            session = requests.sessions.session()
            response = session.send(req.prepare())
        except requests.exceptions.RequestException as e:
            pass
        finally:
            if response:
                assert response.status_code == 200, \
                    'App not register in identity'




