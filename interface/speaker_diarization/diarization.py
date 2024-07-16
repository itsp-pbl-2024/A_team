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
            max_speakers=MySpeakerDiarization.get_enrolled_speakers_num(speaker_num),  # speaker_num,
            step=0.5,
            latency=0.5,
            tau_active=0.8,
            rho_update=0.3,
            delta_new=0.4,
        )
        pipeline = SpeakerDiarization(config)
        mic = MicrophoneAudioSource()
        inference = StreamingInference(pipeline, mic)
        self.streaming_flag = False

        # フックを追加して、ストリーミングの進行状況を標準出力に書き込む
        def on_next(value):
            if not self.streaming_flag:
                self.streaming_flag = True
                print("Streaming now", flush=True)

        # カスタムオブザーバーを追加
        inference.attach_hooks(on_next)
        inference.attach_observers(RTTMWriter(mic.uri, "file.rttm"))
        self.prediction = inference()

    def start(self):
        self.clear_file()

    @classmethod
    def associate_id2name(cls, speaker_id, name):
        cls.id_name[name] = speaker_id

    @classmethod
    def register_id(cls, name) -> bool:
        file_path = "file.rttm"
        if name == "":
            return False
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not lines:
                return False

            durations = defaultdict(float)
            for line in lines:
                if line.startswith("SPEAKER"):
                    data = line.split(" ")
                    if len(data) < 8:  # Ensure there are enough elements
                        print("error in rttm file.")
                        return False
                    try:
                        speaker_id = data[7]
                        duration = float(data[4])
                        durations[speaker_id] += duration
                    except (ValueError, IndexError):
                        return False

            if not durations:
                return False

            max_id = max(durations.items(), key=lambda x: x[1])[0]
            cls.associate_id2name(max_id, name)
            return True

        except FileNotFoundError:
            return False

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
                "durations": id_and_durations[str(i)],
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
    def get_enrolled_speakers_num(speaker_num):
        return speaker_num + 1

    @staticmethod
    def register_speaker_num(speaker_num):
        url = "http://127.0.0.1:5000/register"
        headers = {"Content-Type": "application/json"}
        data = {"n": MySpeakerDiarization.get_enrolled_speakers_num(speaker_num)}
        res = requests.post(url, json=data)


def run_diarization(speaker_num):
    MySpeakerDiarization.set_speaker_num(speaker_num)
    diarization_pipeline = MySpeakerDiarization(speaker_num=speaker_num)


if __name__ == "__main__":
    num_speakers = int(sys.argv[1])
    run_diarization(num_speakers)
