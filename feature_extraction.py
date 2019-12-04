import numpy as np
import librosa

class Features:
    tempo = 0 #tempo
    beats = 0 #average beats per frame
    rms = 0 #rms
    cent = 0 #centroid
    rolloff = 0 #rolloff
    zcr = 0 #zcr
    low = 0 #lowenergy
    entropy = 0 #entropy

    def normalize(self, min, max):
        self.tempo = (self.tempo-min.tempo)/(max.tempo-min.tempo)
        self.beats = (self.beats-min.beats)/(max.tempo-min.beats)
        self.rms = (self.rms-min.rms)/(max.rms-min.rms)
        self.cent = (self.cent-min.cent)/(max.cent-min.cent)
        self.rolloff = (self.rolloff-min.rolloff)/(max.rolloff-min.rolloff)
        self.zcr = (self.zcr-min.zcr)/(max.zcr-min.zcr)
        self.low = (self.low-min.low)/(max.low-min.low)
        self.entropy = (self.entropy-min.entropy)/(max.entropy-min.entropy)

    def classify(self):        
        energy = 0.8*self.rmse + (1-self.low)*0.2
        timbre = 0.2*self.zcr + 0.4*self.cent+ 0.3*self.rolloff + 0.1*self.entropy
        rhythm = 0.4*self.beats + 0.6*self.tempo

        if energy < 0.5: #low energy
            if (0.7*timbre + 0.3*rhythm < 0.5): 
                emotionClass = 'contentment' #2 (+/-)
            else:
                emotionClass = 'depression' #3  (-/-)
            stress = 0.7*timbre + 0.3*rhythm
        else:
            if (0.3*timbre + 0.7*rhythm < 0.5): 
                emotionClass = 'exuberance' #1 (+/+)
            else:
                emotionClass = 'frantic' #4 (-/+)
            stress = 0.3*timbre + 0.7*rhythm
        
        return (energy, stress)

def norm(var, varmin, varmax):
    return (var-varmin)/(varmax-varmin)

def extract_features(songname):
    features = Features()
   
    y, sr = librosa.load(songname, duration=60)
    #TODO check if song already in database

    # Extracting Features
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    
    mean = np.mean(rmse[0])
    count = 0
    for rms in rmse[0]:
        if (rms < mean):
            count += 1
    lowenergy = float(count)/float(len(rmse[0]))

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    entropy = librosa.feature.spectral_flatness(y=y)
    zcr = librosa.feature.zero_crossing_rate(y)  
    pitch = librosa.core.piptrack(y=y, sr=sr)
    
    # Add Features to class
    features.tempo = tempo  # tempo (beats per minute), middle = 120 bpm
    features.beats = np.average(beats)
    features.rms = np.mean(rmse)
    features.cent = np.mean(cent)
    features.rolloff = np.mean(rolloff)
    features.zcr = np.var(rolloff)
    features.low = lowenergy
    features.entropy = np.mean(entropy)

    return features