from room import Room
from participants import Participants


class RoomList:

    def __init__(self):
        self._rooms = []

    def get_rooms(self):
        return self._rooms

    def create_room(self, num):
        id = len(self._rooms) + 1
        participants = Participants(num)
        room = Room(participants, id)
        self._rooms.append(room)
    
    def get_room(self, id):
        for i in self._rooms:
            if i.get_id == id:
                return i
