from array import array
import requests
import json
import httpx
from rich.console import Console

from whatsapp_client.response import Response

from whatsapp_client.tools.account import Account
from whatsapp_client.tools.device import Device
from whatsapp_client.tools.groups import Groups
from whatsapp_client.tools.journals import Journals
from whatsapp_client.tools.marking import Marking
from whatsapp_client.tools.queues import Queues
from whatsapp_client.tools.receiving import Receiving
from whatsapp_client.tools.sending import Sending
from whatsapp_client.tools.serviceMethods import ServiceMethods
from whatsapp_client.tools.webhooks import Webhooks


class GreenApi:
    'REST API class'

    host: str
    idInstance: str
    apiTokenInstance: str

    def __init__(self, 
                    idInstance: str, 
                    apiTokenInstance: str,
                    host: str = 'https://api.green-api.com') -> None:
        self.host = host
        self.idInstance = idInstance
        self.apiTokenInstance = apiTokenInstance

        self.account = Account(self)
        self.device = Device(self)
        self.groups = Groups(self)
        self.journals = Journals(self)
        self.marking = Marking(self)
        self.queues = Queues(self)
        self.receiving = Receiving(self)
        self.sending = Sending(self)
        self.serviceMethods = ServiceMethods(self)
        self.webhooks = Webhooks(self)

    def request(self, method: str, url: str, 
                payload: any = None, files: array = None):
        url = url.replace('{{host}}', self.host)
        url = url.replace('{{idInstance}}', self.idInstance)
        url = url.replace('{{apiTokenInstance}}', self.apiTokenInstance)
        status_code = 0
        text = ''
        try:
            headers = {}
            payloadData = None
            if payload != None:
                if files == None:
                    headers = {
                        'Content-Type': 'application/json'
                    }
                    payloadData = json.dumps(payload)
                else:
                    payloadData = payload   
            result = requests.request(method, url, headers = headers, 
                                        data = payloadData, 
                                        files = files)
            status_code = result.status_code
            text = result.text
            result.raise_for_status()
        except requests.HTTPError:
            return Response(status_code, text)
        except Exception as err:
            status_code = 0
            text = f'Other error occurred: {err}'
        return Response(status_code, text)

    def request(self, method: str, url: str, payload: any = None, files: array = None):
        url = url.replace('{{host}}', self.host)
        url = url.replace('{{idInstance}}', self.idInstance)
        url = url.replace('{{apiTokenInstance}}', self.apiTokenInstance)

        console = Console()

        try:
            with httpx.Client() as client:
                headers = {}
                payload_data = None
                if payload is not None:
                    if files is None:
                        headers = {'Content-Type': 'application/json'}
                        payload_data = json.dumps(payload)
                    else:
                        payload_data = payload

                response = self.make_request(method, url, client, headers, payload_data, files)

                status_code = response.status_code
                text = response.text
                response.raise_for_status()
        except httpx.HTTPError:
            console.print(f"[bold red]HTTP error occurred: {status_code}[/bold red]")
            return Response(status_code, text)
        except Exception as err:
            status_code = 0
            text = f'Other error occurred: {err}'
            console.print(f"[bold red]{text}[/bold red]")
            return Response(status_code, text)

        return Response(status_code, text)

    def make_request(self, method, url, client, headers, payload_data, files):
        if method == "GET":
            return client.get(url, headers=headers)
        elif method == "POST":
            return client.post(url, headers=headers, data=payload_data, files=files)
        elif method == "PUT":
            return client.put(url, headers=headers, data=payload_data)
        elif method == "DELETE":
            return client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")