import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle as pkl
import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

videos = pd.read_pickle('../../data/videos_raw_metadata')
transcripts = pd.read_pickle('../../transcripts.pkl')

def get_transcript(uid):
    transcript = YouTubeTranscriptApi.get_transcript(uid)
    formatter = TextFormatter()
    string_formatted = formatter.format_transcript(transcript)
    transcript = string_formatted.split('\n')
    return transcript
i = 0

for uid in tqdm(videos):
    if uid in transcripts:
        continue
    try:
        transcript = get_transcript(uid)
    except Exception as e:
        print(e)
        transcript = []
    transcripts[uid] = transcript
    i += 1
    if i % 1000 == 0:
        pkl.dump(transcripts, open('transcripts-temp', 'wb'))

pkl.dump(transcripts, open('transcripts', 'wb'))