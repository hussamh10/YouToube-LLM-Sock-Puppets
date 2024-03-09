from tqdm import tqdm
import pandas as pd
import pickle as pkl
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from multiprocessing import Pool

# Function to get the transcript
def get_transcript(uid):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(uid)
        formatter = TextFormatter()
        string_formatted = formatter.format_transcript(transcript)
        return uid, string_formatted.split('\n')
    except Exception as e:
        print(e)
        return uid, []

# Function to process a slice of video IDs
def process_slice(video_slice):
    local_transcripts = {}
    i = 0
    for uid in tqdm(video_slice):
        local_transcripts[uid] = get_transcript(uid)[1]
        i += 1
        if (i + 1) % 500 == 0:
            pkl.dump(local_transcripts, open(f'transcripts_temp_{uid}.pkl', 'wb'))
    return local_transcripts

if __name__ == '__main__':
    # Load data
    videos = pd.read_pickle('../../data/videos_raw_metadata')
    transcripts = pd.read_pickle('../../transcripts.pkl')

    filtered_videos = [uid for uid in videos if uid not in transcripts]

    total_videos = len(filtered_videos)
    slice_size = total_videos // 20
    slices = [filtered_videos[i:i + slice_size] for i in range(0, total_videos, slice_size)]

    with Pool(20) as pool:
        results = pool.map(process_slice, slices)

    for local_transcripts in results:
        transcripts.update(local_transcripts)

    pkl.dump(transcripts, open('transcripts.pkl', 'wb'))
