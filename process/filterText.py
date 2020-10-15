import configparser
import sys

try:
    config = configparser.ConfigParser()
    config.read_file(open(r'config.txt'))
except OSError as error:
    print(error.strerror)
    sys.exit()

category = list(config.get('Category Container', 'category'))

def filterText(textArr):
  text = []
  meaning = []
  confidence = []
  containerNumberArr = []
  confidenceArr = []
  
  for word, conf in textArr:
    for char in word:
      if word[-1] in category:
        bool = "owner"
        
    if len(word) != 4 or word == 'TARE':
      bool = "unknown"
    if len(word) == 6 or len(word) == 7:
      for char in word:
        bool = "serial"
        if char.isnumeric() == False:
          bool = "unknown"
    meaning.append(bool)
    text.append(word)
    confidence.append(conf)

  try:
    filter = text[meaning.index("owner")]
    confFilter = confidence[meaning.index("owner")]

    containerNumberArr.append(filter)
    confidenceArr.append(confFilter)
  except ValueError:
    None

  try:
    filter = text[meaning.index("serial")]
    confFilter = confidence[meaning.index("serial")]

    containerNumberArr.append(filter)
    confidenceArr.append(confFilter)
  except ValueError:
    None

  # Calculate Confidence
  avgConf = round((sum(confidenceArr)/len(confidenceArr)), 2)
  containerNumber = ''.join(str(e) for e in containerNumberArr)
  return containerNumber, avgConf