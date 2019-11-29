from queue import Queue as tQueue
import threading

def analyse(rx, playlist_changes):
    t = threading.currentThread()
    while getattr(t, "keep_running", True):
        if not rx.poll(timeout=0.1):
            continue
        
        new_text = rx.recv()
        print(new_text) #do usefull stuff with text instead


    print("stopped analysis")