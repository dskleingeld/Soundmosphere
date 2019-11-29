import queue
import threading

def play(playlist_changes):
    t = threading.currentThread()
    while getattr(t, "keep_running", True):
        try:
            changes = playlist_changes.get_nowait()
        except queue.Empty:
            continue

        print(changes)
    print("stopped music playback")

