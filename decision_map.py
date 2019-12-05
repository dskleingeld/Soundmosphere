from queue import Queue as tQueue
import threading
from text_analysis import analyseText
import sqlite3

MAX_RECENT_WORDS = 90

def analyse(rx, playlist_changes):
    t = threading.currentThread()
    recent_words = []
    
    db_path = "database.sqlite"

    while getattr(t, "keep_running", True):
        if not rx.poll(timeout=0.1):
            continue
        
        new_text = rx.recv()
        recent_words = recent_words+new_text.split(" ")
        recent_words = recent_words[-MAX_RECENT_WORDS:]
        recent_text = " ".join(recent_words)

        energy, stress = analyseText(recent_text)

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        for row in c.execute("SELECT path FROM features"):
          print(row)
        #for row in c.execute("SELECT path FROM features WHERE energy < "+str(energy+x)+" AND energy > "+str(energy-x)+" AND stress < "+str(stress+x)+" AND stress > "+str(stress-x))):
        #for row in c.execute("SELECT path FROM features ORDER BY ABS(energy-"+str(energy)+") ASC LIMIT 5"):
         # print(path)
        for row in c.execute("SELECT path FROM features WHERE energy < 0.5 AND stress < 0.5"):
          print(row)

    print("stopped analysis")
