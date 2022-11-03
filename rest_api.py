'''API server that handles multiple endpoints for user audio projects.'''
import base64
import audio_metadata
from flask import Flask, jsonify, request


app = Flask(__name__)

audio_raw_data = {}
audio_meta_data = {}


# NOTE: Requires file name as url parameter.
@app.route('/post', methods=['POST'])
def post_audio():
    '''Saves raw audio data & metadata in memory'''
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({'result': 'FAILURE. Missing file name!'})

    data = request.get_data()

    try:
        metadata = audio_metadata.loads(data)
        audio_raw_data[file_name] = data
        audio_meta_data[file_name] = metadata
    except (audio_metadata.FormatError, audio_metadata.UnsupportedFormat,
            ValueError) as error:

        return jsonify({
            'result': 'FAILURE',
            'error': str(error)
            })

    context = {'result': 'SUCCESS'}
    return jsonify(context)


# NOTE: Requires file name as parameter
@app.route("/download", methods=["GET"])
def get_file_data():
    '''Returns the raw audio data encoded in base64 and returned as utf-8 string.'''
    file_name = request.args.get('name')
    if not file_name:
        return jsonify({'result': 'FAILURE. Missing file name!'})

    if file_name not in audio_raw_data:
        return jsonify({'result': 'FAILURE. File not found!'})

    # Decodes base64 encoded bytes object to utf-8 serializable string
    encoded_file = base64.encodebytes(audio_raw_data[file_name]).decode('utf-8')

    context = {file_name: encoded_file}
    return jsonify(context)


@app.route("/list", methods=["GET"])
def get_files():
    '''Returns a list of all uploaded audio files. Option to specify a max_duration in seconds'''
    max_duration = request.args.get('maxduration')
    context = {}

    if max_duration is None:
        for file_name, metadata in audio_meta_data.items():
            context[file_name] = metadata['streaminfo']['duration']
    else:
        for file_name, metadata in audio_meta_data.items():
            if metadata['streaminfo']['duration'] <= float(max_duration):
                context[file_name] = metadata['streaminfo']['duration']

    return jsonify(context)


# NOTE: Requires file name as parameter.
@app.route("/info", methods=["GET"])
def get_info():
    '''Returns metadata about requested audio file such as duration, bitrate, etc.'''
    file_name = request.args.get('name')
    if not file_name:
        return jsonify({'result': 'FAILURE. Missing file name!'})

    if file_name not in audio_raw_data:
        return jsonify({'result': 'FAILURE. File not found!'})

    metadata = audio_meta_data[file_name]

    context = {
        'filesize': metadata['filesize'],
    }

    # Adds streaminfo dictionary key/val pairs to existing context dictionary
    context.update(metadata['streaminfo'])

    return jsonify(context)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
