import ast


class Message:

    def __init__(self, data):
        self._data = data
        self._length = self.caluculate_voice_amount()

    # estimate length of speaking
    def caluculate_voice_amount(self):
        v_length = 0
        for i in ast.literal_eval(self._data["durations"]):
            v_length += float(i)
        return v_length

    def get_length(self):
        return self._length

    def get_user_id(self):
        return self._data["id"]
