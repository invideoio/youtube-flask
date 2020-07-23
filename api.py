from flask import Flask
from flask_restplus import reqparse, abort, Api, Resource, fields

from json_creator import create_response_from_youtube_data
from utility import get_youtube_id,decode_yt_data,get_data_from_youtube
app = Flask(__name__)
api = Api(app)

videoModel = api.model('video', {
    'url': fields.String,
    'extension': fields.String,
    'video_format': fields.Integer,
    'format_display_string': fields.String,
    'size_display_string': fields.String,
    'size_in_bytes': fields.Integer,
    'has_audio': fields.Boolean,
    'width': fields.Integer,
    'height': fields.Integer
})

audioModel = api.model('audio', {
    'bitrate': fields.Integer,
    'bitrate_display_string': fields.String,
    'size_in_bytes': fields.Integer,
    'size_display_string': fields.String,
    'extension': fields.String,
    'url': fields.String,
})

responseModel = api.model('response', {
    'title': fields.String,
    'thumbnail_url': fields.String,
    'duration_seconds': fields.Integer,
    'video_list': fields.List(fields.Nested(videoModel)),
    'audio_list': fields.List(fields.Nested(audioModel)),
})


@api.route('/youtube_details', endpoint="youtube_details")
@api.doc(params={'yt_url': 'A Youtube Url'})
class YoutubeDataFetcher(Resource):
    @api.marshal_with(responseModel)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('yt_url', type=str)
        args = parser.parse_args()
        url = args['yt_url'] if 'yt_url' in args else None
        if url is None:
            abort(400)
        # 4 Steps
        #1. Fetch the Id from the youtube url
        #2. Call the youtube open endpoint
        #3. decode the response as querystring
        #4. convert to our required data type
        #1
        id = get_youtube_id(url)
        #2
        (encoded_data, status_code) = get_data_from_youtube(id)
        if encoded_data is None:
            abort(status_code)
        #3
        decoded_player_response = decode_yt_data(encoded_data)
        #4
        response_data = create_response_from_youtube_data(decoded_player_response)
        return response_data

if __name__ == '__main__':
    app.run(debug=True)