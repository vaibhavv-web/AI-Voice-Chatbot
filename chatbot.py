import os
import requests
from dotenv import load_dotenv
from gtts import gTTS
from datetime import datetime
from prompt import SYSTEM_PROMPT
from tools import web_search

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_llm_response(message, history):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost:7860",
        "X-Title": "AI Voice Chatbot",
        "Content-Type": "application/json"
    }

    # Detect if web search is needed
    if any(word in message.lower() for word in ["news", "latest", "search", "current", "today"]):
        search_results = web_search(message)

        message = f"""
User question: {message}

Here are some web search results:

{search_results}

Use these results to answer the question.
"""

    # Build conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        for msg in history:
            messages.append(msg)

    messages.append({"role": "user", "content": message})

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": messages
    }

    try:
        response = requests.post(URL, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"


def respond(message, chat_history):

    if chat_history is None:
        chat_history = []

    # Handle date query locally
    if "date" in message.lower():
        text = f"Today's date is {datetime.now().strftime('%d %B %Y')}"
    else:
        text = generate_llm_response(message, chat_history)

    # Convert text to speech
    tts = gTTS(text)
    audio_file = "response.mp3"
    tts.save(audio_file)

    # Update chat history
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": text})

    return chat_history, audio_file