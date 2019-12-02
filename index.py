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
            c.execute("INSERT OR IGNORE INTO to_index (path) VALUES ('"+filepath+"')")

#must be ran before ANY threat touches the database
def init_db():
    if not os.path.isfile(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        #create the needed tables
        c.execute('CREATE TABLE music_dirs (dir text)')
        c.execute('CREATE TABLE to_index (path text)')
        c.execute('''CREATE TABLE indexed 
        (path text, some_numb real, another_numb real)''')
        conn.commit()
        conn.close()

def keep_updated(new_path_rx, shutdown_rx):
    #find new music files to index
    conn = sqlite3.connect(db_path)
    while True:
        add_unindexed(conn)
        index_unindexed(conn, shutdown_rx)

        while True: 
            if shutdown_rx.poll():
                return
            if not new_path_rx.poll(timeout=0.1):
                continue

            new_path = new_path_rx.recv()
            add_music_dir(new_path)

def index_unindexed(conn, shutdown_rx):
    c = conn.cursor()
    for row in c.execute("SELECT * FROM to_index"):
        if shutdown_rx.poll():
            return #stop if we need to quit
        
        path = row[0]
        res = index_file(path) #if index succeeded, remove from db
        if res != None:
            c.execute("DELETE FROM to_index WHERE path='"+path+"'")
            q = "INSERT INTO indexed VALUES ('"+path+"',"+str(res[0])+","+"NULL"+")"
            c.execute(q)

def index_file(path: str):
    print("add code here to categorises/analyses a file at given path")
    #return None
    return (0.1, 0)