from collections import defaultdict


class Room:

    def __init__(self, participants):
        self._members = participants
        self._messages = []
        self._latests = defaultdict(int)

    # send message and update latestmessage
    def add_message(self, id, msg, time):
        self._messages.append((id, msg))
        self._latests[id] = time

    def get_messages(self):
        return self._messages

    def get_participant(self, id):
        for i in self._members:
            if i.get_id() == id:
                return i

    def get_participants(self):
        return self._members

    def get_latests(self):
        return self._latests
