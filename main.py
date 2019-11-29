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

    (new_file_rx, new_file_tx) = Pipe(duplex=False)
    (shutdown1_rx, shutdown1_tx) = Pipe(duplex=False)
    index_proc = Process(target=index.keep_updated, args(new_file_rx, shutdown1_rx)

    (transcribe_rx, transcribe_tx) = Pipe(duplex=False)
    (shutdown2_rx, shutdown2_tx) = Pipe(duplex=False)
    speech_proc = Process(target=transcripe, args=(transcribe_tx,shutdown_rx))
    speech_proc.start()

    playlist_changes = tQueue()
    analysis_thread = Thread(target=analyse, args=(transcribe_rx,playlist_changes,))
    analysis_thread.start()

    audio_thread = Thread(target=play, args=(playlist_changes,))
    audio_thread.start()

    #start user interface
    user_interface.wait_for_enter()
    print("shutting down now")

    #send shutdown signal do all threads and processes
    shutdown1_tx.send(True)
    shutdown2_tx.send(True)
    analysis_thread.keep_running = False
    audio_thread.keep_running = False

    speech_proc.join()
    analysis_thread.join()
    audio_thread.join()
