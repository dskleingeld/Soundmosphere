from queue import Queue as tQueue
import threading

MAX_RECENT_WORDS = 90

def analyse(rx, playlist_changes):
    t = threading.currentThread()
    recent_words = []
    

    while getattr(t, "keep_running", True):
        if not rx.poll(timeout=0.1):
            continue
        
        new_text = rx.recv()
        recent_words = recent_words+new_text.split(" ")
        recent_words = recent_words[-MAX_RECENT_WORDS:]
        recent_text = " ".join(recent_words)

    print("stopped analysis")