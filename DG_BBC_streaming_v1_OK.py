import httpx
import logging
import threading
import os

from dotenv import load_dotenv
from deepgram import DeepgramClient
from deepgram.core.events import EventType

load_dotenv()

URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"

def main():
    try:
        # use default config
        deepgram: DeepgramClient = DeepgramClient(
            api_key=os.environ.get("DEEPGRAM_API_KEY"),
        )

        # Create a websocket connection to Deepgram
        with deepgram.listen.v1.connect(
            model="nova-3",
        ) as connection:
            def on_message(message) -> None:
                msg_type = getattr(message, "type", "Unknown")
                if hasattr(message, 'channel') and hasattr(message.channel, 'alternatives'):
                    sentence = message.channel.alternatives[0].transcript
                    if len(sentence) == 0:
                        return
                    print(message.channel.alternatives[0].transcript)

            connection.on(EventType.OPEN, lambda _: print("Connection opened"))
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
            connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

            lock_exit = threading.Lock()
            exit = False

            # Define a thread for start_listening with error handling
            def listening_thread():
                try:
                    connection.start_listening()
                except Exception as e:
                    print(f"Error in listening thread: {e}")

            # Start listening in a separate thread
            listen_thread = threading.Thread(target=listening_thread)
            listen_thread.start()

            # define a worker thread for HTTP streaming with error handling
            def myThread():
                try:
                    with httpx.stream("GET", URL) as r:
                        for data in r.iter_bytes():
                            lock_exit.acquire()
                            if exit:
                                break
                            lock_exit.release()

                            connection.send_media(data)
                except Exception as e:
                    print(f"Error in HTTP streaming thread: {e}")

            # start the HTTP streaming thread
            myHttp = threading.Thread(target=myThread)
            myHttp.start()

            # signal finished
            input("")
            lock_exit.acquire()
            exit = True
            lock_exit.release()

            # Wait for both threads to close and join with timeout
            myHttp.join(timeout=5.0)
            listen_thread.join(timeout=5.0)

            print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

if __name__ == "__main__":
    main()