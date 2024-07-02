from collections import defaultdict
from diart import SpeakerDiarization, SpeakerDiarizationConfig
from diart.sources import MicrophoneAudioSource
from diart.inference import StreamingInference
from diart.sinks import RTTMWriter
import os
import requests
import json
import sys


class MySpeakerDiarization:
    id_name = defaultdict(str)
    speaker_num = 5

    def __init__(self, id_name=defaultdict(str), speaker_num=5):
        self.id_name = id_name
        config = SpeakerDiarizationConfig(
            max_speakers=speaker_num,
            step=0.5,
            latency=0.5,
            tau_active=0.555,
            rho_update=0.422,
            delta_new=1.517,
        )
        pipeline = SpeakerDiarization(config)
        mic = MicrophoneAudioSource()
        inference = StreamingInference(pipeline, mic)
        inference.attach_observers(RTTMWriter(mic.uri, "file.rttm"))
        self.prediction = inference()

    def start(self):
        self.clear_file()

    @classmethod
    def associate_id2name(cls, speaker_id, name):
        cls.id_name[name] = speaker_id

    @classmethod
    def register_id(cls, name):
        file_path = "file.rttm"
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        durations = defaultdict(float)
        for line in lines:
            if line.startswith("SPEAKER"):
                data = line.split(" ")
                speaker_id = data[7]
                durations[speaker_id] = float(data[4]) + durations[speaker_id]

        durations = list(durations.items())
        max_id = max(durations, key=lambda x: x[1])[0]
        cls.associate_id2name(max_id, name)

    @staticmethod
    def clear_file():
        file_path = "file.rttm"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

    @classmethod
    def save_to_server(cls):
        url = "http://127.0.0.1:5000/send"
        headers = {"Content-Type": "application/json"}
        file_path = "file.rttm"
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        id_and_durations = defaultdict(list)
        for line in lines:
            if line.startswith("SPEAKER"):
                data = line.split(" ")
                # data[7]はspeaker0, speaker1, ...のような形式。ここから数字を取り出す
                speaker_id = data[7].split("r")[1]
                id_and_durations[speaker_id].append(float(data[4]))

        for i in range(cls.speaker_num):
            data = {
                "id": i,
                "durations": str(id_and_durations[str(i)]),
            }
            res = requests.post(url, json=data, headers=headers)
        cls.clear_file()

    def fetch_from_server(self):
        url = "http://127.0.0.1:5000/get_speaking_time"
        headers = {"Content-Type": "application/json"}
        data = defaultdict(float)
        for i in range(self.speaker_num):
            res = requests.get(url, headers=headers, json={"id": i})
            data[i] = float(res.text)  # TODO
        return data

    @classmethod
    def set_speaker_num(cls, speaker_num):
        cls.speaker_num = speaker_num

    @classmethod
    def get_id_from_name(cls, name):
        return cls.id_name[name]

    @staticmethod
    def register_speaker_num(speaker_num):
        url = "http://127.0.0.1:5000/register"
        headers = {"Content-Type": "application/json"}
        data = {"n": speaker_num}
        res = requests.post(url, json=data)


def run_diarization(speaker_num):
    MySpeakerDiarization.set_speaker_num(speaker_num)
    diarization_pipeline = MySpeakerDiarization(speaker_num=speaker_num)


if __name__ == "__main__":
    num_speakers = int(sys.argv[1])
    run_diarization(num_speakers)
