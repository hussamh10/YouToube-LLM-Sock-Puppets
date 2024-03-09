import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
​
​
PATH = 'data_youtube/'
​
final_dict = {}
for file_ in os.listdir(PATH):
    print(file_, flush=True)
    tid = 'tree-'+file_.split('-')[0][2:]
    pid = 'path-'+file_.split('.')[0].split('-')[1][1:]
    final_dict.setdefault(tid, {})
    final_dict[tid].setdefault(pid, {})
​
    with open(PATH+file_, "r") as infile:
        data = json.load(infile)
        for depth, key in enumerate(data.keys()):
            
            vids = data[key][1]
            final_dict[tid][pid].setdefault('depth-'+str(depth), {})
            for vid in vids:
                # We are assuming there are no "yt-shorts" in the list of videos
                vid_id = vid.split('v=')[1]                
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(vid_id)
                    formatter = TextFormatter()
                    # .format_transcript(transcript) turns the transcript into a String.
                    string_formatted = formatter.format_transcript(transcript)
                    final_dict[tid][pid]['depth-'+str(depth)].update({'vid-id: '+vid_id: string_formatted})
                
                except:
                    final_dict[tid][pid]['depth-'+str(depth)].update({'vid-id: '+vid_id: 'transcript_disabled'})
​
​
json_object = json.dumps(final_dict, indent=2)
with open('transcript_data.json', 'w') as outfile:
    outfile.write(json_object)