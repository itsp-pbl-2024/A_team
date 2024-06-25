from collections import defaultdict
import os


def extract_duration(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    durations = defaultdict(float)
    for line in lines:
        if line.startswith("SPEAKER"):
            data = line.split(" ")
            speaker_id = data[7]
            durations[speaker_id] = float(data[4]) + durations[speaker_id]

    durations = list(durations.items())
    return durations


def remove_file(file_path):

    os.remove(file_path)


print(remove_file("file.rttm"))
