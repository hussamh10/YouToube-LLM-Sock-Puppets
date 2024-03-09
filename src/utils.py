from tqdm.notebook import tqdm

def get_id(url):
    if len(url.split('v=')) <= 1:
        return None
    url = url.split('v=')[1]
    url = url.split('&')[0]
    return url

def decode_upnext(urls):
    urls = eval(urls.decode('utf-8'))
    ids = []
    for u in urls:
        ids.append(get_id(u))
    return ids


def clean(metadata, titles=None):
    videos = dict()
    for i in metadata:
        video = metadata[i]
        vs = video['snippet']
        id = video['id']

        videos[id] = dict()
        videos[id]['id'] = video['id']
        videos[id]['title'] = vs['title']
        videos[id]['description'] = vs['description']
        videos[id]['tags'] = vs.get('tags', [])
        videos[id]['category'] = vs['categoryId']
        videos[id]['channel_title'] = vs['channelTitle']
        videos[id]['embeddings'] = dict()

        if titles is not None:
            videos[id]['embeddings']['title'] = titles[videos[id]['title']]
    return videos



