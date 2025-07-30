import requests
from flask import Flask, request, jsonify, render_template, Response, stream_with_context, redirect
from app.scraper import scrape_youtube
from app.gemini import analyze_and_rank_results
from app.downloader import get_download_url
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/') # api root directory to fetch html
def index():
    return render_template('index.html')

@app.route('/api/search') #/api/search?q=hey+jude
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'A search query is required.'}), 400
    
    logger.info(f"Received search query: {query}")
    results = scrape_youtube(query)
    logger.info(f"Scraper returned {len(results)} results")
    # Always call analyze_and_rank_results, Gemini can be toggled in gemini.py
    analyzed_results = analyze_and_rank_results(results)
    logger.info(f"Returning {len(analyzed_results)} analyzed results")
    return jsonify(analyzed_results)

@app.route('/api/download') #api/download?url="Hey+jude+Remastered"&quality="360p"
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '720p')

    if not video_url:
        return jsonify({'error': 'The video URL is required.'}), 400

    logger.info(f"Download request received for URL: {video_url} with quality: {quality}")
    direct_url = get_download_url(video_url, quality)
    if not direct_url:
        logger.error(f"Failed to get download URL for video: {video_url}")
        return Response("Could not retrieve download link.", status=500)
    # Redirect the user to the direct video URL
    return redirect(direct_url)

if __name__ == "__main__":
    app.run()