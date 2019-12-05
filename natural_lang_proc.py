import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

# Process whole documents
#text = ("Fire leaped from the dragon's jaws. He circled for a while high in the air above them lighting all the lake; the trees by the shores shone like copper and like blood with leaping shadows of dense black at their feet. Then down he swooped straight through the arrow-storm, reckless in his rage, taking no heed to turn his scaly sides towards his foes, seeking only to set their town ablaze.")
#text = "There was an autumn-like mist white upon the ground and the air was chill, but soon the sun rose red in the East and the mists vanished, and while the shadows were still long they were offgain. So they rode now for two more days, and all the while they saw nothing save grass and flowers and birds and scattered trees, and occasionally small herds of red deer browsing or sitting at noon in the shade. "
#text = "They spent a cold and lonely night and their spirits fell. The next day they set out again. Balin and Bilbo rode behind, each leading another pony heavily laden beside him; the others were some way ahead picking out a slow road, for there were no paths. They made north-west, slanting away from te River Running, and drawing ever nearer and nearer to a great spur of the Mountain that was flung out southwards towards them."
text = "he found himself standing in a landscape that looked exactly like a chine chessboard on every black square there was a monster there were two dogs snakes and finds with three roses teeth and forehead at dogs and five head a demon kings and so on he was so to speak looking out through the eyes of the young hero of the story it was like being in the passenger seat of an outer mobile all he had to do was watch while the hero is patched one months do after another and at fancourt towards the white stone tower at the end"

doc = nlp(text)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)