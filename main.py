from multiprocessing import Process
from threading import Thread

from multiprocessing import Pipe
from queue import Queue as tQueue

from deepspeech_stream import transcripe
from decision_map import analyse
from music_player import play

import index
import user_interface

if __name__ == '__main__':

    index.init_db() #setup the db
    index.finish_previous_indexing()

    #temporary test code
    index.add_music_dir("/home/kleingeld/Music")
    #end test

    (new_path_rx, new_file_tx) = Pipe(duplex=False)
    (shutdown1_rx, shutdown1_tx) = Pipe(duplex=False)
    index_proc = Process(target=index.keep_updated, args=(new_path_rx, shutdown1_rx))
    index_proc.start()
    
    (transcribe_rx, transcribe_tx) = Pipe(duplex=False)
    #(shutdown2_rx, shutdown2_tx) = Pipe(duplex=False)
    #speech_proc = Process(target=transcripe, args=(transcribe_tx,shutdown2_rx))
    #speech_proc.start()

    playlist_changes = tQueue()
    analysis_thread = Thread(target=analyse, args=(transcribe_rx,playlist_changes,))
    analysis_thread.start()

    # audio_thread = Thread(target=play, args=(playlist_changes,))
    # audio_thread.start()

    #send test speech
    import time
    time.sleep(2)
    #index.print_database()


    transcribe_tx.send("There was an autumn-like mist white upon the ground and")
    transcribe_tx.send("the air was chill")
    transcribe_tx.send("but soon the sun rose red in the East and the mists vanished, and while the shadows were still long they were offgain. So they rode now for two more days, and all the while they saw nothing save grass and flowers and birds and scattered")
    transcribe_tx.send("trees, and occasionally small herds of red deer browsing or")
    transcribe_tx.send("sitting at noon in the shade.")
    transcribe_tx.send("Fire leaped from the dragon's jaws. He circled for a while high in the air above them lighting all the lake; the trees by the shores shone like copper and like blood with leaping shadows of dense black at their")
    

    #start user interface
    user_interface.wait_for_enter()
    print("shutting down, please wait")

    #send shutdown signal do all threads and processes
    shutdown1_tx.send(True)
    #shutdown2_tx.send(True)
    analysis_thread.keep_running = False
    #audio_thread.keep_running = False

    index_proc.join()
    #speech_proc.join()
    analysis_thread.join()
    #audio_thread.join()

    print("done")
