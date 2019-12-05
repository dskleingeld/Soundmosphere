import os
import sqlite3
import util
import feature_extraction as fe

#from meta_from_web_search import get_web_meta

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
    for dirpath in c.execute('SELECT dir FROM music_dirs'):
        for filepath in util.iter_matching(dirpath[0], ".*\.(mp3|wav)"):
            c.execute("INSERT OR IGNORE INTO to_index (path) VALUES ('"+filepath+"')")
    conn.commit()

#must be ran before ANY threat touches the database
def init_db():
    if not os.path.isfile(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        #create the needed tables
        c.execute('''CREATE TABLE music_dirs (dir text)''')
        c.execute('''CREATE TABLE to_index (path text)''')
        c.execute('''CREATE TABLE features (path text, 
            tempo real, beats real, rms real, cent real,
            rolloff real, zcr real, low real, entropy real,

            stress real, energy real
        )''')
        conn.commit()
        conn.close()

def keep_updated(new_path_rx, shutdown_rx):
    #find new music files to index
    conn = sqlite3.connect(db_path)
    #must normalize as we might have been
    #stopped mid normalization

    while True:
        add_unindexed(conn)
        index_unindexed(conn, shutdown_rx)
        finalise_index(conn) #TODO opt: dont do this every time
        print("hoho")

        while True: 
            if shutdown_rx.poll():
                return
            if not new_path_rx.poll(timeout=0.1):
                continue

            new_path = new_path_rx.recv()
            add_music_dir(new_path)

def index_unindexed(conn, shutdown_rx):
    c = conn.cursor()
    unindexed = []
    for path in c.execute("SELECT * FROM to_index"):
        unindexed += path

    for path in unindexed:
        if shutdown_rx.poll():
            return #stop if we need to quit

        res = index_file(path) #if index succeeded, remove from db
        if res != None:
            c.execute("DELETE FROM to_index WHERE path='"+path+"';")
            q = ("INSERT INTO features "
            + "(path, tempo, beats, rms, cent, rolloff, zcr, low, entropy) "
            + "VALUES ('"+path+"',"+str(res)+")")
            c.execute(q)
    conn.commit()


def index_file(path: str):
    #get_web_meta(path) #can not be used
    features = fe.extract_features(path)
    #features = None
    
    return features

#iterate through database and set "energy" and "stress" level
def finalise_index(conn):
    c = conn.cursor()
    mini = fe.Features(str_list=[1e6,1e6,1e6,1e6,1e6,1e6,1e6,1e6,1e6])
    maxi = fe.Features(str_list=[-1e6,-1e6,-1e6,-1e6,-1e6,-1e6,-1e6,-1e6,-1e6])
    
    #find minimum and maximum values for each feature
    for row in c.execute("SELECT path, tempo, beats, rms, cent, rolloff, zcr, low, entropy FROM features"):
        path = row[0]
        features = fe.Features(str_list=row)
        fe.update_bounds(features, mini, maxi)

    for row in c.execute("SELECT path, tempo, beats, rms, cent, rolloff, zcr, low, entropy FROM features"):
        path = row[0]
        features = fe.Features(str_list=row)
        (energy, stress) = features.classify()
        
        c.execute("UPDATE features SET stress= {0:f}, energy={1:f} WHERE path='{2}'".format(stress, energy, path))
    conn.commit()

def finish_previous_indexing():
    conn = sqlite3.connect(db_path)
    finalise_index(conn)

def print_database():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    print("printing_database")
    for row in c.execute("SELECT * FROM features"):
        print(row)