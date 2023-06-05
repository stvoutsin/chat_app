import os

BASE_URL = "http://localhost:8000"

# Get the path to the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Set the relative path to the database file
SQLALCHEMY_DATABASE_URL = "sqlite:////" + os.path.join(base_dir, "chat_app.db")
AI_ENABLED = True
OPENAI_API_KEY = ""
OPENAI_CONFIG = {
    "temperature": 0.5,
    "max_tokens": 50,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}
tone = "nice"