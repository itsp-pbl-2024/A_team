class Participant:

    def __init__(self, user_id, user_name):
        self._user_id = user_id
        self._user_name = user_name

    def get_user_id(self):
        return self._user_id

    def get_user_name(self):
        return self._user_name
