from collections import defaultdict


class Room:

    def __init__(self, participants, id):
        self._members = participants
        self._messages = []
        self._latests = defaultdict(int)
        self._id = id

    # send message and update latestmessage
    def add_message(self, message):
        self._messages.append(message)
        self._latests[message.get_id()] += message.get_length()

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

    def get_id(self):
        return self._id

    # TODO find alone boy during room
    def search_alone(self):
        participant = self.get_participant(0)
        return participant
