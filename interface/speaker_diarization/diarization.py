from collections import defaultdict
from diart import SpeakerDiarization, SpeakerDiarizationConfig
from diart.sources import MicrophoneAudioSource
from diart.inference import StreamingInference
from diart.sinks import RTTMWriter
import os
import requests
import json


class MySpeakerDiarization:
    def __init__(self, id_name=defaultdict(str), speaker_num=5):
        self.id_name = id_name
        self.speaker_num = speaker_num
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
        inference.attach_observers(RTTMWriter(mic.uri, "testtesttest"))

    def start(self):
        self.clear_file()

    def associate_id2name(self, speaker_id, name):
        self.id_name[speaker_id] = name

    def register_id(self, name):
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
        print(self.id_name)
        self.associate_id2name(max_id, name)
        print(self.id_name)

    def clear_file(self):
        file_path = "file.rttm"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

    def save_to_server(self):
        url = "http://localhost:5000/register"
        headers = {"Content-Type": "application/json"}
        data = {"n": len(self.speaker_num)}
        res = requests.post(url, data=json.dumps(data), headers=headers)

        url = "http://localhost:5000/send"
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

        for i in range(len(self.speaker_num)):
            data = {
                "id": str(i),
                "durations": str(id_and_durations[str(i)]),
            }
            res = requests.post(url, data=json.dumps(data), headers=headers)
            print(res.text)

    def fetch_from_server(self):
        url = "http://localhost:5000/get_speaking_time"
        headers = {"Content-Type": "application/json"}
        data = defaultdict(float)
        for i in range(len(self.speaker_num)):
            res = requests.get(url, headers=headers, json={"id": i})
            data[i] = float(res.text)  # TODO
        return data
