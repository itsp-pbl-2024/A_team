from room import Room
from participants import Participants


class Rooms:

    def __init__(self):
        self._rooms = []

    def get_rooms(self):
        return self._rooms

    def create_room(self, user_num):
        room_id = len(self._rooms) + 1
        participants = Participants(user_num)
        room = Room(participants, room_id)
        self._rooms.append(room)
        return room_id

    def get_room(self, room_id):
        for i in self._rooms:
            if i.get_room_id() == room_id:
                return i
