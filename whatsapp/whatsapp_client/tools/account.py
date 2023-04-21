import os.path
from whatsapp_client.response import Response
from rich.console import Console


class Account:
    def __init__(self, greenApi) -> None:
        self.greenApi = greenApi
        self.console = Console()

    def _make_request(self, method, endpoint, payload=None, files=None):
        return self.greenApi.request(method, f"{{{{host}}}}/waInstance{{{{idInstance}}}}{endpoint}/{{{{apiTokenInstance}}}}", payload, files)

    def getSettings(self) -> Response:
        return self._make_request('GET', '/getSettings')

    def getStateInstance(self) -> Response:
        return self._make_request('GET', '/getStateInstance')

    def getStatusInstance(self) -> Response:
        return self._make_request('GET', '/getStatusInstance')

    def logout(self) -> Response:
        return self._make_request('GET', '/Logout')

    def qr(self) -> Response:
        return self._make_request('GET', '/QR')

    def reboot(self) -> Response:
        return self._make_request('GET', '/Reboot')

    def setProfilePicture(self, path) -> Response:
        path_parts = os.path.split(path)
        file = path_parts[1]
        files = [('file', (file, open(path, 'rb'), 'image/jpeg'))]

        return self._make_request('POST', '/SetProfilePicture', files=files)

    def setSettings(self, requestBody) -> Response:
        return self._make_request('POST', '/SetSettings', requestBody)
