keywords = ["autumn", "mist", "white", "chill", "sun", "shadow", "shadows", "ride", "rode", "grass", "flower", "flowers", "bird", "birds", "tree", "trees", "herd", "herds", "deer", "browse", "browsing", "sit", "sitting", "noon", "shade"]
energy = [-1, -1, 1, -1, 1, -1, -1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, -1, -1, 1, -1]
stress = [-1, 0, 0, -1, -1, 1, 1, 0, 0, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, 0, 0]

def matchKeyword(word):
  energyval = 0.0
  stressval = 0.0

  if word in keywords:
    energyval = energy[keywords.index(word)]*0.1
    stressval = stress[keywords.index(word)]*0.1

  return energyval, stressval

def analyseText(text):
  energytotal = 0
  stresstotal = 0
  word = ""
  for char in text:
    if char == " ":
      energyval, stressval = matchKeyword(word)
      energytotal += energyval
      stresstotal += stressval
      word = ""
    else:
      word += char

  if energytotal>1: energytotal=1
  elif energytotal<-1: energytotal=-1
  if stresstotal>1: stresstotal=1
  elif stresstotal<-1: stresstotal=-1

  return energytotal, stresstotal
