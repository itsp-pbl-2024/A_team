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

    # find alone boy during room
    def search_alone(self):
        total_length = defaultdict(int)
        for message in self._messages:
            total_length[message.get_id()] += message.get_length()
        botti_id = 0
        min_length = 1 << 60
        for user_id in total_length:
            if total_length[user_id] < min_length:
                botti_id = user_id
                min_length = total_length[user_id]

        participant = self.get_participant(botti_id)
        return participant
