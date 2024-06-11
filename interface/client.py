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

sperker_num = 3

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
prediction = inference()


url = "http://localhost:5000/send"
headers = {"Content-Type": "application/json"}
for i in range(sperker_num):
    data = {
        "id": str(i),
        "durations": str(prediction.label_timeline("speaker" + str(i))),
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    print(res.text)
