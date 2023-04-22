from whatsapp_client.response import Response


class Device:
    def __init__(self, greenApi) -> None:
        self.greenApi = greenApi

    def _make_request(self, method, endpoint, payload=None, files=None):
        return self.greenApi.request(method, f"{{{{host}}}}/waInstance{{{{idInstance}}}}{endpoint}/{{{{apiTokenInstance}}}}", payload, files)

    def getDeviceInfo(self) -> Response:
        return self._make_request('GET', '/GetDeviceInfo')
