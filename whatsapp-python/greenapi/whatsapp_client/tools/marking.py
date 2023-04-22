from whatsapp_client.response import Response

class Marking:
    def __init__(self, greenApi) -> None:
        self.greenApi = greenApi

    def _make_request(self, method, endpoint, payload=None, files=None):
        return self.greenApi.request(method, f"{{{{host}}}}/waInstance{{{{idInstance}}}}{endpoint}/{{{{apiTokenInstance}}}}", payload, files)

    def readChat(self, chatId: str, idMessage: str) -> Response:
        requestBody = {'chatId': chatId, 'idMessage': idMessage}
        return self._make_request('POST', '/ReadChat', requestBody)
