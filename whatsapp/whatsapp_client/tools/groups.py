from array import ArrayType, array
import os.path
from whatsapp_client.response import Response


class Groups:
    def __init__(self, greenApi) -> None:
        self.greenApi = greenApi

    def _make_request(self, method, endpoint, payload=None, files=None):
        return self.greenApi.request(method, f"{{{{host}}}}/waInstance{{{{idInstance}}}}{endpoint}/{{{{apiTokenInstance}}}}", payload, files)

    def addGroupParticipant(self, groupId: str, participantChatId: str) -> Response:
        requestBody = {'groupId': groupId, 'participantChatId': participantChatId}
        return self._make_request('POST', '/AddGroupParticipant', requestBody)

    def createGroup(self, groupName: str, chatIds: array) -> Response:
        requestBody = {'groupName': groupName, 'chatIds': chatIds}
        return self._make_request('POST', '/CreateGroup', requestBody)

    def getGroupData(self, groupId: str) -> Response:
        requestBody = {'groupId': groupId}
        return self._make_request('POST', '/GetGroupData', requestBody)

    def leaveGroup(self, groupId: str) -> Response:
        requestBody = {'groupId': groupId}
        return self._make_request('POST', '/LeaveGroup', requestBody)

    def removeAdmin(self, groupId: str, participantChatId: str) -> Response:
        requestBody = {'groupId': groupId, 'participantChatId': participantChatId}
        return self._make_request('POST', '/RemoveAdmin', requestBody)

    def removeGroupParticipant(self, groupId: str, participantChatId: str) -> Response:
        requestBody = {'groupId': groupId, 'participantChatId': participantChatId}
        return self._make_request('POST', '/RemoveGroupParticipant', requestBody)

    def setGroupAdmin(self, groupId: str, participantChatId: str) -> Response:
        requestBody = {'groupId': groupId, 'participantChatId': participantChatId}
        return self._make_request('POST', '/SetGroupAdmin', requestBody)

    def setGroupPicture(self, groupId: str, path: str) -> Response:
        requestBody = {'groupId': groupId}
        path_parts = os.path.split(path)
        file = path_parts[1]
        files = [('file', (file, open(path, 'rb'), 'image/jpeg'))]
        return self._make_request('POST', '/SetGroupPicture', requestBody, files)

    def updateGroupName(self, groupId: str, groupName: str) -> Response:
        requestBody = {'groupId': groupId, 'groupName': groupName}
        return self._make_request('POST', '/UpdateGroupName', requestBody)
