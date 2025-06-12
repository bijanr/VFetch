import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gemini_config():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("❌ GEMINI_API_KEY not found in environment variables")
        logger.info("Please create a .env file with GEMINI_API_KEY=your_api_key")
        return False
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        logger.info("✅ Successfully configured Gemini API")
        
        # List available models
        logger.info("Checking available models...")
        for m in genai.list_models():
            logger.info(f"Found model: {m.name}")
        
        # Try to get the model
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content("Say 'Hello, World!'")
        
        logger.info("✅ Successfully connected to Gemini API")
        logger.info(f"Test response: {response.text}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing Gemini API: {str(e)}")
        return False

if __name__ == "__main__":
    print("\nTesting Gemini API Configuration...")
    print("-" * 40)
    success = test_gemini_config()
    print("-" * 40)
    if success:
        print("✅ Gemini API is configured correctly!")
    else:
        print("❌ Gemini API configuration failed. Please check the errors above.") 