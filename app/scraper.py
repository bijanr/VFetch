import requests
from bs4 import BeautifulSoup
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_youtube(query: str):
    """
    Scrapes YouTube for a given query and returns video results.

    Args:
        query (str): The search query.

    Returns:
        list: A list of dictionaries, where each dictionary represents a video
              and has the keys 'title', 'url', and 'id'.
              Returns an empty list if an error occurs.
    """
    try:
        search_query = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={search_query}"

        # Set a user-agent to mimic a real browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        logger.info(f"Searching YouTube for: {query}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, "html.parser")
        video_data = []

        # YouTube search results are often embedded in a script tag as a JSON object
        scripts = soup.find_all("script")
        found_data = False
        for script in scripts:
            script_str = str(script)
            if "var ytInitialData = " in script_str:
                try:
                    data_str = script_str.split("var ytInitialData = ")[1].split(";</script>")[0]
                    data = json.loads(data_str)
                    found_data = True
                except Exception as e:
                    logger.error(f"Failed to parse ytInitialData JSON: {e}")
                    break

                contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [{}])[0].get("itemSectionRenderer", {}).get("contents", [])

                for item in contents:
                    if "videoRenderer" in item:
                        video = item["videoRenderer"]
                        title = video.get("title", {}).get("runs", [{}])[0].get("text")
                        video_id = video.get("videoId")
                        if title and video_id:
                            video_url = f"/watch?v={video_id}"
                            video_data.append({
                                "title": title,
                                "url": video_url,
                                "id": video_id
                            })
                    if len(video_data) >= 15:
                        break
                break

        if not found_data:
            logger.error("Could not find ytInitialData in YouTube page. YouTube may have changed their page structure.")
            return []

        logger.info(f"Found {len(video_data)} videos for query: {query}")
        return video_data

    except requests.exceptions.Timeout:
        logger.error(f"Timeout while searching YouTube for: {query}")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during requests to YouTube: {e}")
        return []
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"Error parsing YouTube page structure: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

if __name__ == '__main__':
    # Example usage:
    search_results = scrape_youtube("Python tutorials for beginners")
    if search_results:
        for i, video in enumerate(search_results, 1):
            print(f"{i}. {video['title']} ({video['url']})")