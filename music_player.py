import queue
import threading

from enum import Enum

class OrderType(Enum):
    VOLUME_CHANGE = 1
    SONG_CHANGE = 2
    #might add new shit

class Change(Enum):
    FAST = 1
    SLOW = 2
    #might add new shit too

class Order(Enum):
    orderType = OrderType.SONG_CHANGE#can be OrderType
    path = ""
    volume = 0

def play(playlist_changes):
    t = threading.currentThread()

    while getattr(t, "keep_running", True):
        try:
            changes = playlist_changes.get_nowait()
        except queue.Empty:
            continue

        #do something with the changes

    print("stopped music playback")
