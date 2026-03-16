import os
import gradio as gr
from dotenv import load_dotenv
from chatbot import respond
import whisper

# Load environment variables
load_dotenv()

# Load Whisper model
whisper_model = whisper.load_model("base")


def transcribe_audio(audio_path):
    """
    Convert speech to text using Whisper
    """
    result = whisper_model.transcribe(audio_path)
    text = result["text"].strip()
    return text


def handle_text(message, chat_history):

    if not message.strip():
        return chat_history, None, ""

    new_history, audio_file = respond(message, chat_history)

    return new_history, audio_file, ""


def handle_voice(audio_path, chat_history):

    if audio_path is None:
        return chat_history, None

    # Transcribe audio using Whisper
    result = whisper_model.transcribe(audio_path)

    transcribed_text = result["text"].strip()

    print("User said:", transcribed_text)

    new_history, audio_file = respond(transcribed_text, chat_history)

    return new_history, audio_file

with gr.Blocks() as demo:

    gr.Markdown("# 🎙️ AI Voice Chatbot")

    chatbot = gr.Chatbot()

    audio = gr.Audio(
        label="AI Voice Response",
        autoplay=True
    )

    with gr.Row():

        msg = gr.Textbox(
            placeholder="Type your message here...",
            show_label=False,
            scale=4,
        )

        mic = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Or speak",
            scale=1,
        )

    send_btn = gr.Button("Send", variant="primary")

    msg.submit(handle_text, [msg, chatbot], [chatbot, audio, msg])
    send_btn.click(handle_text, [msg, chatbot], [chatbot, audio, msg])

    mic.stop_recording(handle_voice, [mic, chatbot], [chatbot, audio])

demo.launch()