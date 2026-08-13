
import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI
GROQ_API_KEY = os.getenv("GROQ_API_KEY"
                         "")

groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

response = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful Python tutor. Keep replies under 3 sentences."},
        {"role": "user", "content": "What is an API key in one line?"},
    ],
)

print("🦙 Reply:", response.choices[0].message.content)