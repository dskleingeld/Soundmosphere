import os
import sqlite3
import util

db_path = "database.sqlite"

def add_music_dir(path: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO music_dirs (dir) VALUES ('"+path+"')")
    conn.commit()
    conn.close()

def add_unindexed(conn):
    #load music dirs from database
    c = conn.cursor()

    #for glob
    for dirpath in c.execute('SELECT * FROM music_dirs'):
        for filepath in util.iter_matching(dirpath[0], ".*\.(mp3|wav)"):
            print(filepath)
            c.execute("INSERT OR IGNORE INTO unindexed (path) VALUES ('"+filepath+"')")

#must be ran before ANY threat touches the database
def init_db():
    if not os.path.isfile(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        #create the needed tables
        c.execute('CREATE TABLE music_dirs (dir text)')
        c.execute('CREATE TABLE unindexed (path text)')
        conn.commit()
        conn.close()

def keep_updated(new_file_rx, shutdown_rx):
    #find new music files to index
    conn = sqlite3.connect(db_path)
    add_unindexed(conn)

    c = conn.cursor()
    for row in c.execute("SELECT * FROM unindexed"):
        if shutdown_rx.poll():
            return #stop if we need to quit
        
        res = index(row) #if index succeeded, remove from db
        if res == "":
            c.execute("DELETE * FROM unindexed WHERE path = '"+row+"'")

    while not shutdown_rx.poll():
        if not new_file_rx.poll(timeout=0.1):
            continue

        new_path = new_file_rx.recv()
        print(new_path)

def index(path: str):
    print("add code here to categorises/analyses a file at given path")
    return "" #return empty string indecates failure