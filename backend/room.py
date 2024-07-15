from collections import defaultdict
from typing import Optional, List
from participants import Participants
from message import Message


class Room:

    def __init__(self, participants: Participants, room_id: int):
        self._participants = participants
        self._messages = []
        self._latests = defaultdict(int)
        self._room_id = room_id

        self.reset_latests()

    def reset_latests(self):
        for participant in self._participants.get_participants():
            self._latests[participant] = 0

    # send message and update latestmessage
    def add_message(self, message: Message):
        self._messages.append(message)
        self._latests[message.get_user_id()] += message.get_length()

    def get_messages(self) -> List[Message]:
        return self._messages

    def get_participant(self, user_id: int) -> Optional[int]:
        for i in self._participants.get_participants():
            if i == user_id:
                return i

    def get_participants(self) -> Participants:
        return self._participants

    def get_latests(self):
        return self._latests

    def get_room_id(self):
        return self._room_id

    # find alone boy with the least amount of speaking
    def search_alone(self) -> Optional[int]:
        if not self._latests:
            return None

        botti_id = min(self._latests, key=self._latests.get)
        return botti_id
