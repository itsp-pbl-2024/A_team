class RoomList:

    def __init__(self):
        self._rooms = []
    
    def get_rooms(self):
        return self._rooms
    
    def add_room(self, room):
        self._rooms.append(room)