from participant import Participant


class Participants:

    def __init__(self, user_num):
        self._participants = []
        for _ in range(user_num):
            user_id = len(self._participants) + 1
            self.add_participant(user_id)

    def get_participants(self):
        return self._participants

    def add_participant(self, user_id):
        participant = Participant(user_id, user_id)
        self._participants.append(participant)
