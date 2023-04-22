import os.path
import time
from whatsapp_client.response import Response
from rich.console import Console

class Webhooks:
    def __init__(self, greenApi) -> None:
        self.greenApi = greenApi
        self.started = False
        self.console = Console()

    def _make_request(self, method, endpoint, payload=None, files=None):
        time.sleep(3)  # Add a tiny sleep
        return self.greenApi.request(method,'{{host}}/waInstance{{idInstance}}/receiveNotification/{{apiTokenInstance}}', payload, files)

    def startReceivingNotifications(self, onEvent) -> bool:
        self.started = True
        print('Starting receiving notifications')
        self.job(onEvent)

    def stopReceivingNotifications(self) -> bool:
        self.started = False

    def job(self, onEvent) -> None:
        print('Incoming notifications are being received. '\
            'To interrupt, press Ctrl+C')
        try:
            while self.started == True:
                resultReceive = self._make_request('GET', '/receiveNotification')
                if resultReceive.code == 200:
                    if resultReceive.data is None:
                        # There are no incoming notifications,
                        # we send the request again
                        time.sleep(1)  # Add a tiny sleep
                        continue
                    body = resultReceive.data['body']
                    typeWebhook = body['typeWebhook']
                    onEvent(typeWebhook, body)
                    # self._make_request('DELETE', '/deleteNotification/{0}'.format(resultReceive.data['receiptId']))
            print('End receiving')
        except KeyboardInterrupt:
            print('End receiving')
