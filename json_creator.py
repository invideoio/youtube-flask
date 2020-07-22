def get_video_list(youtube_data):
    video_list = []
    streaming_data = youtube_data['streamingData']
    formats = streaming_data['formats'] if streaming_data is not None else []
    for format in formats:
        video_object = {}
        video_object['url'] = format['url']
        video_object['extension'] = format['mimeType'].split(';')[0].split('video/')[-1]
        video_object['video_format'] = format['width']
        video_object['format_display_string'] = str(format['width']) + 'p'
        video_object['has_audio'] = True
        video_object['size_in_bytes'] = int(format['contentLength']) if 'contentLength' in format else 0
        video_object['size_display_string'] = str(round(video_object['size_in_bytes'] / 1048576, 1)) + 'MB'
        video_object['width'] = format['width']
        video_object['height'] = format['height']
        video_list.append(video_object)
    return video_list


def get_audio_list(youtube_data):
    streaming_data = youtube_data['streamingData']
    adaptive_formats = streaming_data['adaptiveFormats'] if streaming_data is not None else []
    audio_formats = [format for format in adaptive_formats if 'audio/' in format['mimeType']]
    audio_list = []
    for format in audio_formats:
        audio_object = {}
        audio_object['url'] = format['url']
        audio_object['bitrate'] = int(format['averageBitrate'] / 1000)
        audio_object['bitrate_display_string'] = "@{}kbps".format(audio_object['bitrate'])
        audio_object['size_in_bytes'] = int(format['contentLength'])
        audio_object['size_display_string'] = str(round(audio_object['size_in_bytes'] / 1048576, 1)) + 'MB'
        audio_object['extension'] = format['mimeType'].split(';')[0].split('audio/')[-1]
        audio_list.append(audio_object)
    return audio_list


def create_response_from_youtube_data(youtube_data):
    response_data = {}
    video_details = youtube_data['videoDetails']
    response_data['title'] = video_details['title']
    thumbnail_list = video_details['thumbnail']['thumbnails']
    biggest_thumbnail_url = thumbnail_list[-1]['url']
    response_data['thumbnail_url'] = biggest_thumbnail_url
    response_data['duration_seconds'] = int(video_details['lengthSeconds'])
    response_data['video_list'] = get_video_list(youtube_data)
    response_data['audio_list'] = get_audio_list(youtube_data)
    return response_data
