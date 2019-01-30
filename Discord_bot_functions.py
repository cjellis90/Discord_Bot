def isFloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def percentage(percent, whole):
  return ((percent * whole) /100.0)

def computeEntry(value):
  
  if(isFloat(value)):
    value = float(value)
    i = 1
    for x in range(1,21):
      finalVal = (percentage(i,value) + value)
      finalVal = str(finalVal)
      stringI = str(i)
      print(stringI,"% is: ",finalVal)
      i += 1
  else:
    print("The correct command is !entry <number>")
