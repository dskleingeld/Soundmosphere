from keywords import keywords, energy, stress

def matchKeyword(word):
  energyval = 0.0
  stressval = 0.0

  if word in keywords:
    energyval = energy[keywords.index(word)]*0.05
    stressval = stress[keywords.index(word)]*0.05

  return energyval, stressval

def analyseText(text):
  energytotal = 0
  stresstotal = 0
  word = ""
  for word in text:
    energyval, stressval = matchKeyword(word)  
    energytotal += energyval
    stresstotal += stressval

  if energytotal>1: energytotal=1
  elif energytotal<-1: energytotal=-1
  if stresstotal>1: stresstotal=1
  elif stresstotal<-1: stresstotal=-1

  return energytotal, stresstotal
