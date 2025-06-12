import yt_dlp
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_download_url(video_url: str, quality: str = '720p'):
    """
    Returns a direct video URL for the requested quality.

    Args:
        video_url (str): The full URL of the YouTube video.
        quality (str): The desired video quality (e.g., '720p', '1080p').

    Returns:
        str: The direct download URL of the video, or None if an error occurs.
    """
    try:
        # Options for yt_dlp to extract information without downloading
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Extracting info for URL: {video_url}")
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            if not formats:
                logger.error("No formats found.")
                return None

            # Parse target quality
            match = re.search(r'(\d+)', quality)
            target_height = int(match.group(1)) if match else 720

            # Filter for mp4 video with audio, sorted by height descending
            candidates = [
                f for f in formats
                if f.get('vcodec', 'none') != 'none'
                and f.get('acodec', 'none') != 'none'
                and f.get('ext') == 'mp4'
                and f.get('height')
                and f.get('url')
            ]
            candidates.sort(key=lambda f: f['height'], reverse=True)

            # Find best match at or below target quality
            for f in candidates:
                if f['height'] <= target_height:
                    logger.info(f"Selected format: {f.get('format_id')} - {f['height']}p")
                    return f['url']

            # If none found, fallback to best available
            if candidates:
                logger.info(f"Falling back to lowest available: {candidates[-1].get('format_id')} - {candidates[-1]['height']}p")
                return candidates[-1]['url']

            # Fallback: try any format with a URL
            for f in formats:
                if f.get('url'):
                    logger.info("Fallback to any available format with URL.")
                    return f['url']

            logger.error("No suitable format found.")
            return None

    except Exception as e:
        logger.error(f"Error in get_download_url: {e}")
        return None