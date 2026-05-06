# Live Streaming Transcription (Speech-to-Text)

Real-time transcription via WebSocket, receiving results as audio is spoken from BBC live services.

## What it does

Opens a WebSocket connection to Deepgram's streaming API and sends audio chunks in real time. As audio arrives, Deepgram returns transcribed results.

## Prerequisites

- Python 3.10+
- Set `DEEPGRAM_API_KEY` environment variable

# Run

```bash
python DG_BBC_streaming.py
```
