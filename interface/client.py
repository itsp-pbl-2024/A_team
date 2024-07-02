from diart import SpeakerDiarization, SpeakerDiarizationConfig
from diart.sources import MicrophoneAudioSource
from diart.inference import StreamingInference
from diart.sinks import RTTMWriter
import requests
import json

"""
diartの使い方
prediction.chart()  
    各スピーカーの合計会話時間

prediction.label_timeline("speakerId")
    スピーカー0が話した時間帯の詳細。各要素について、.start, .end, .duration, .dataがある
"""

sperker_num = 2

config = SpeakerDiarizationConfig(
    max_speakers=sperker_num,
    step=0.5,
    latency=0.5,
    tau_active=0.555,
    rho_update=0.422,
    delta_new=1.517,
)
pipeline = SpeakerDiarization()
mic = MicrophoneAudioSource()
inference = StreamingInference(pipeline, mic)
inference.attach_observers(RTTMWriter(mic.uri, "file.rttm"))
prediction = inference()


url = "http://localhost:5000/register"
headers = {"Content-Type": "application/json"}
data = {"n": sperker_num}
res = requests.post(url, data=json.dumps(data), headers=headers)

url = "http://localhost:5000/send"

for i in range(sperker_num):
    durations = []
    for statement in prediction.label_timeline("speaker" + str(i)):
        durations.append(str(statement.end - statement.start))
    data = {
        "id": str(i),
        "durations": str(durations),
    }
    res = requests.post(url, data=data, headers=headers)
