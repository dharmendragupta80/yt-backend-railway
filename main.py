from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/getvideo', methods=['GET'])
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    ydl_opts = {
        'quiet': True,
        'format': 'best[ext=mp4]/best',
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify(info.get('url'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
