from whatsapp_client.response import Response

class Journals:
    def __init__(self, greenApi) -> None:
        self.greenApi = greenApi

    def _make_request(self, method, endpoint, payload=None, files=None):
        return self.greenApi.request(method, f"{{{{host}}}}/waInstance{{{{idInstance}}}}{endpoint}/{{{{apiTokenInstance}}}}", payload, files)

    def getChatHistory(self, chatId: str, count: str) -> Response:
        requestBody = {'chatId': chatId, 'count': count}
        return self._make_request('POST', '/GetChatHistory', requestBody)

    def lastIncomingMessages(self) -> Response:
        return self._make_request('GET', '/LastIncomingMessages')

    def lastOutgoingMessages(self) -> Response:
        return self._make_request('GET', '/LastOutgoingMessages')
