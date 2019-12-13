from keywords import keywords

def matchKeyword(word):
  energyval = 0
  stressval = 0
  if word in keywords.keys():
    energyval = keywords[word].energy *0.05
    stressval = keywords[word].stress *0.05

  return energyval, stressval

def analyseText(text):
  energytotal = 0.5
  stresstotal = 0.5
  for word in text.split():
    energyval, stressval = matchKeyword(word)  
    energytotal += energyval
    stresstotal += stressval

  if energytotal>1: energytotal=1
  elif energytotal<0: energytotal=0
  if stresstotal>1: stresstotal=1
  elif stresstotal<0: stresstotal=0

  return energytotal, stresstotal
