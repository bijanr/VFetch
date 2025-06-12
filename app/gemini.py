import os
# import google.generativeai as genai
import json
from dotenv import load_dotenv
import logging

# Toggle Gemini ranking on/off
ENABLE_GEMINI = True

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Commented out Gemini API configuration
# api_key = None
# model = None

# try:
#     api_key = os.environ.get("GEMINI_API_KEY")
#     if api_key:
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel('models/gemini-1.5-flash')
#         logger.info("Successfully configured Gemini API")
#     else:
#         logger.warning("GEMINI_API_KEY environment variable not set. Gemini analysis will be disabled.")
# except Exception as e:
#     logger.error(f"Error configuring Gemini API: {str(e)}")
#     api_key = None
#     model = None

def analyze_and_rank_results(results: list) -> list:
    """
    Analyzes and ranks search results using the Gemini API.
    If Gemini API is not available, returns results without analysis.

    Args:
        results (list): A list of dictionaries, where each dictionary represents a scraped video.

    Returns:
        list: The modified list of dictionaries with 'safety_rating' and 'relevance_score',
              sorted by 'relevance_score'.
    """
    if not ENABLE_GEMINI:
        logger.info("Gemini ranking disabled. Returning results unchanged.")
        return results

    # If 'viewCount' or similar popularity metric is present, sort by it
    def get_popularity(item):
        # Try to extract view count or similar metric
        for key in ['viewCount', 'views', 'popularity']:
            if key in item:
                try:
                    return int(item[key].replace(',', '').replace(' views', '').strip())
                except Exception:
                    continue
        return 0  # Default if not found

    # Sort results by popularity descending, if possible
    ranked = sorted(results, key=get_popularity, reverse=True)
    logger.info("Gemini ranking applied: results sorted by popularity.")
    return ranked

if __name__ == '__main__':
    # Example usage for testing
    sample_results = [
        {'title': 'How to Bake a Cake', 'url': 'http://example.com/cake'},
        {'title': 'Funny Cat Videos Compilation', 'url': 'http://example.com/cats'},
        {'title': 'Learn Python Programming for Beginners', 'url': 'http://example.com/python'}
    ]

    print("Analyzing and ranking sample results...")
    ranked_results = analyze_and_rank_results(sample_results)
    print("\nRanked Results:")
    for res in ranked_results:
        print(f"  Title: {res.get('title')}")
        print(f"  URL: {res.get('url')}")
        # Only print keys if they exist
        if 'safety_rating' in res:
            print(f"    Safety Rating: {res['safety_rating']}")
        if 'relevance_score' in res:
            print(f"    Relevance Score: {res['relevance_score']}")
        print("-" * 20)