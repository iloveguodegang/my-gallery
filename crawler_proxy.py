from flask import Flask, request, Response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/fetch_image')
def fetch_image():
    url = request.args.get('url')
    if not url:
        return 'No url', 400
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return Response(resp.content, content_type=resp.headers.get('Content-Type', 'image/jpeg'))
        else:
            return f'Failed to fetch: {resp.status_code}', 500
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(port=5000) 