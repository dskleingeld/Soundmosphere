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
        print(new_text)
        recent_words = recent_words+new_text.split(" ")
        recent_words = recent_words[-MAX_RECENT_WORDS:]
        recent_text = " ".join(recent_words)

        energy, stress = analyseText(recent_text)

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        for row in c.execute("SELECT energy FROM features ORDER BY energy ASC"):
          for i in range(len(row)):
            while row[i] < energy: i += 1
            print (row[i-1], row[i], row[i+1]) 

    print("stopped analysis")
