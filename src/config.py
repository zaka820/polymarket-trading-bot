from dotenv import load_dotenv
import os

load_dotenv()

def load_config():
    return {
        "api_key": os.getenv("API_KEY"),
        "api_secret": os.getenv("API_SECRET"),
        "api_endpoint": os.getenv("API_ENDPOINT"),
    }