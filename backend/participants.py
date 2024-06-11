class Participants:

    def __init__(self, user_num):
        self._participants = []
        cur = 0
        for _ in range(user_num):
            self._participants.append(cur)
            cur += 1

    def get_participants(self):
        return self._participants
