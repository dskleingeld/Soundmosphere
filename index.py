import os
import sqlite3
import util
import feature_extraction as fe
import codecs

#from meta_from_web_search import get_web_meta

db_path = "database.sqlite"

def add_music_dir(dirpath: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = "INSERT OR IGNORE INTO music_dirs (dir) VALUES ({})".format(quote_identifier(dirpath))
    c.execute(q)
    conn.commit()
    conn.close()

def add_unindexed(conn):
    #load music dirs from database
    c = conn.cursor()

    #for glob
    for dirpath in c.execute('SELECT dir FROM music_dirs'): #different file types still to be tested
        for filepath in util.iter_matching(dirpath[0], ".*\.(mp3|wav|ogg|aac|flac|opus|mp4)"):
            q = "SELECT EXISTS(SELECT 1 FROM features WHERE path = {});".format(quote_identifier(filepath))
            c.execute(q)
            res = c.fetchone()
            if res[0] == 0:
                q = "INSERT OR IGNORE INTO to_index (path) VALUES ({})".format(quote_identifier(filepath))
                c.execute(q)
    conn.commit()

#must be ran before ANY threat touches the database
def init_db():
    if not os.path.isfile(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        #create the needed tables
        c.execute('''CREATE TABLE music_dirs (dir text UNIQUE PRIMARY KEY)''')
        c.execute('''CREATE TABLE to_index (path text UNIQUE PRIMARY KEY)''')
        c.execute('''CREATE TABLE features (path text UNIQUE PRIMARY KEY, 
            tempo real, beats real, rms real, cent real,
            rolloff real, zcr real, low real, entropy real,

            stress real, energy real
        )''')
        conn.commit()
        conn.close()

def keep_updated(new_path_rx, shutdown_rx):
    conn = sqlite3.connect(db_path)

    while True:
        add_unindexed(conn)
        index_unindexed(conn, shutdown_rx)
        finalise_index(conn) #TODO opt: dont do this every time

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
    numb_unindexed = len(unindexed)

    for path in unindexed:
        if shutdown_rx.poll():
            return #stop if we need to quit

        res = index_file(path) #if index succeeded, remove from db
        q = "DELETE FROM to_index WHERE path = {};".format(quote_identifier(path))
        c.execute(q)
        
        q = ("INSERT OR IGNORE INTO features "
        + "(path, tempo, beats, rms, cent, rolloff, zcr, low, entropy) "
        + "VALUES ({},{});".format(quote_identifier(path),res))
        c.execute(q)
        conn.commit()

        numb_unindexed -= 1
        print("indexing files in background, {} left".format(numb_unindexed))
        #TODO opt: reindex every 15 new numbers or so
        #TODO opt: do indexing in parallel?


def index_file(path: str):
    #get_web_meta(path) #can not be used
    features = fe.extract_features(path)
    #features = None
    
    return features

#iterate through database and set "energy" and "stress" level
def finalise_index(conn):
    c = conn.cursor()
    min_eng = 1e6
    min_stress = 1e6
    max_eng = -1e6
    max_stress = -1e6
    
    to_update = []
    for row in c.execute("SELECT path, tempo, beats, rms, cent, rolloff, zcr, low, entropy FROM features"):
        path = row[0]
        features = fe.Features(str_list=row)
        (energy, stress) = features.classify()
        
        if energy > max_eng:
            max_eng = energy
        if energy < min_eng:
            min_eng = energy
        if stress > max_stress:
            max_stress = stress
        if stress < min_stress:
            min_stress = stress

        to_update.append((stress, energy, path))
        
    for (stress, energy, path) in to_update:
        energy = norm(energy, min_eng, max_eng)
        stress = norm(stress, min_stress, max_stress, )
        q = "UPDATE features SET stress= {0:f}, energy={1:f} WHERE path={2}".format(stress, energy, quote_identifier(path))
        c.execute(q)
    conn.commit()


def quote_identifier(s, errors="strict"):
    encodable = s.encode("utf-8", errors).decode("utf-8")

    nul_index = encodable.find("\x00")

    if nul_index >= 0:
        error = UnicodeEncodeError("NUL-terminated utf-8", encodable,
                                   nul_index, nul_index + 1, "NUL not allowed")
        error_handler = codecs.lookup_error(errors)
        replacement, _ = error_handler(error)
        encodable = encodable.replace("\x00", replacement)

    return "\"" + encodable.replace("\"", "\"\"") + "\""

def finish_previous_indexing():
    conn = sqlite3.connect(db_path)
    finalise_index(conn)

def print_database():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    print("printing_database")
    for row in c.execute("SELECT * FROM features"):
        print(row)

def print_column(column: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    print("printing column: {}".format(column))
    for row in c.execute("SELECT {} FROM features".format(column)):
        print(row)

def norm(var, varmin, varmax):
    return (var-varmin)/(varmax-varmin)