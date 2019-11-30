import glob
import sqlite3

def find_unindexed():
    #load music dirs from database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE music_dirs (dir text)''')

    #for glob


def keep_updated(new_file_rx, shutdown_rx):
    
    #find new music files to index
    #add to still to be indexed list

    while not shutdown_rx.poll():
        if not new_file_rx.poll(timeout=0.1):
            continue

        new_path = new_file_rx.recv()
        print(new_path)