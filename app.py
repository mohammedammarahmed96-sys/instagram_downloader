from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_videos():
    data = request.json
    links = data.get('links', [])
    video_urls = []

    for link in links:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            video_tag = soup.find('meta', property='og:video')
            if video_tag:
                video_urls.append(video_tag['content'])
            else:
                video_urls.append(f"Could not fetch video: {link}")
        except Exception as e:
            video_urls.append(f"Error fetching: {link}")
    return jsonify({'urls': video_urls})

if __name__ == "__main__":
    app.run(debug=True)
