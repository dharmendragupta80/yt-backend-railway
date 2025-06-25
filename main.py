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
        'skip_download': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            result_formats = []

            for f in formats:
                format_id = f.get('format_id')
                resolution = f.get('format_note') or f.get('height') or 'audio'
                ext = f.get('ext')
                url = f.get('url')
                if not url:
                    continue

                filesize = f.get('filesize') or f.get('filesize_approx')
                size_mb = f"{round(filesize / (1024 * 1024), 2)} MB" if filesize else "Unknown size"
                label = f"{resolution} · {ext.upper()} · {size_mb}"

                result_formats.append({
                    'format_id': format_id,
                    'label': label,
                    'url': url
                })

            return jsonify(result_formats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/getformats', methods=['GET'])
def get_formats():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    ydl_opts = {
        'quiet': True,
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            formats = info.get('formats', [])
            return jsonify(formats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



