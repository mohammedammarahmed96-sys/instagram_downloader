from flask import Flask, request, render_template, send_file, jsonify
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_videos():
    data = request.json
    links = data.get('links', [])

    if not links:
        return jsonify({"error": "No links provided"}), 400

    if len(links) > 1:
        return jsonify({"error": "Direct download supports 1 link at a time"}), 400

    link = links[0]
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        video_tag = soup.find('meta', property='og:video')

        if video_tag:
            video_url = video_tag['content']
            video_response = requests.get(video_url, headers=headers, stream=True)
            video_file = BytesIO(video_response.content)
            return send_file(
                video_file,
                as_attachment=True,
                download_name="instagram_video.mp4",
                mimetype="video/mp4"
            )
        else:
            return jsonify({"error": "Could not fetch video"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns the port dynamically
    app.run(host="0.0.0.0", port=port, debug=True)
