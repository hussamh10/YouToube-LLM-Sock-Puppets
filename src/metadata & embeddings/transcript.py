import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import pickle as pkl

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
transcripts = pd.read_pickle('../../transcripts.pkl')
videos = pd.read_pickle('../../data/videos_raw_metadata')

def get_embeddeding(sentences):
    embeddings = [model.encode(s) for s in sentences]
    embedding = np.mean(embeddings, axis=0)
    if len(sentences) == 0:
        return np.zeros(768)

    return embedding

embs = dict()
for video in tqdm(transcripts):
    transcript = transcripts[video]
    embs[video] = get_embeddeding(transcript)

pkl.dump(embs, open('embeddings-temp', 'wb'))