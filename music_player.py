import queue
import threading
from pydub import AudioSegment
from pydub.playback import play as dubplay
from pydub.playback import _play_with_simpleaudio
from subprocess import call
import time

from enum import Enum

class OrderType(Enum):
    VOLUME_CHANGE = 1
    SONG_CHANGE = 2
    #might add new shit

class SongChangeType(Enum):
    FAST = 1
    SLOW = 2

class VolumeChangeType(Enum):
    FAST = 1
    SLOW = 2
    #might add new shit too

class Order():
    orderType = OrderType.SONG_CHANGE#can be OrderType
    volumeChangeType = VolumeChangeType.FAST
    songChangeType = SongChangeType.FAST
    path = ""
    volume = 0

def play(playlist_changes):
    t = threading.currentThread()
    player = None
    crossfade = False

    while getattr(t, "keep_running", True):
        try:
            changes = playlist_changes.get(False)
        except queue.Empty:
            continue

        #do something with the changes
        if (changes.orderType == OrderType.SONG_CHANGE):
          if (changes.songChangeType == SongChangeType.FAST):
            audio = AudioSegment.from_file(changes.path)
            if player: #already another song playing
              crossfade = True
              for i in range(10): #turn down volume
                call(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
                time.sleep(0.05)                
              player.stop() #stop playing old song
            player = _play_with_simpleaudio(audio) #start new song
            if crossfade:
              for i in range(10): #turn up volume
                call(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
                time.sleep(0.05)
          else:
            time.sleep(3)
            audio = AudioSegment.from_file(changes.path)
            if player:            
              player.stop()
            player = _play_with_simpleaudio(audio)

        if (changes.orderType == OrderType.VOLUME_CHANGE):
          if (changes.volume == 1):
            call(["amixer", "-D", "pulse", "sset", "Master", "5%+"])
          else:
            call(["amixer", "-D", "pulse", "sset", "Master", "5%-"])
          

    print("stopped music playback")
