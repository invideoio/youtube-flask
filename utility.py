import json
import urllib.parse as urlparse
from urllib.parse import parse_qs
import logging
import requests
log = logging.getLogger('yt_caller')

def get_youtube_id(url):
    parsed = urlparse.urlparse(url)
    parsed_query = parse_qs(parsed.query)
    return parsed_query['v'][0]
    
def decode_yt_data(encoded_data):
    decoded_data = parse_qs(encoded_data)
    player_response = json.loads(decoded_data["player_response"][0])
    return player_response

def get_data_from_youtube(id):
    yt_response = requests.get("https://www.youtube.com/get_video_info?video_id={}".format(id))
    # TODO: implement fail safe with el parameter.
    # Request video metadata (e.g. https://www.youtube.com/get_video_info?video_id=e_S9VvJM1PI). Try with el=detailpage if it fails.
    # Full blog: https://tyrrrz.me/blog/reverse-engineering-youtube
    status_code = yt_response.status_code
    if status_code == 200:
        return (yt_response.text, status_code)
    else:
        log.error("Youtube fetching failed, status_code={}".format(status_code))
        return (None, status_code)
    return yt_response.text if yt_response.status_code == 200 else None