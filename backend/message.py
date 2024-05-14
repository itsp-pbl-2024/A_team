class Message:

    def __init__(self, data):
        self._data = data
        self._length = self.caluculate_voice_amount()

    # estimate length of speaking
    def caluculate_voice_amount(self):
        return len(self._data["message"])

    def get_length(self):
        return self._length

    def get_user_id(self):
        return self._data["id"]
