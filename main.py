from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Direct Link API Running!'

@app.route('/getvideo', methods=['GET'])
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    ydl_opts = {
        'quiet': True,
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'http_chunk_size': 1048576,  # 1MB
        'socket_timeout': 10,
        'retries': 2
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            print("Video URL:", info.get('url'))  # Railway logs
            return jsonify({'url': info.get('url')})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/getformats', methods=['GET'])
def get_formats():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    ydl_opts = {
        'quiet': True,
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'http_chunk_size': 1048576,
        'socket_timeout': 10,
        'retries': 2
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            formats = info.get('formats', [])
            print("Formats:", len(formats))
            return jsonify(formats)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
