# Live agent with Speech-to-Text and Text-to-Speech

Real-time simple conversational agent using Deepgram and Groq APIs.

## What it does

Waits for the user to record a message using the spacebar and sends the audio to Deepgram for STT conversion. The request is then sent to Groq and the text answer converted back to audio using Deepgram TTS.

## Prerequisites

- Python 3.10+
- Set `DEEPGRAM_API_KEY` environment variable
- Set `GROQ_API_KEY` environment variable

# Run

```bash
python DG_Groq_agent.py
```
