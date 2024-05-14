from participant import Participant


class Participants:

    def __init__(self, num):
        self._participants = []
        for _ in range(num):
            id = len(self._participants) + 1
            self.add_participant(id)

    def get_participants(self):
        return self._participants

    def add_participant(self, id):
        participant = Participant(id, id)
        self._participants.append(participant)
