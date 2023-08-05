"""module that describes binary file that is to be deciphered"""
import os
from sortedcontainers import SortedDict

class BinaryFile:
  """
  class that describes binary file that is to be deciphered
  """
  #pylint: disable=import-outside-toplevel
  from .inputOutput import saveTags, loadTags, savePython, loadPython, plot, pythonHeader, initContent
  from .commandLine import printNext, printAscii, printList
  from .automaticIdentify import primaryTimeData, findStreak, useExportedFile, entropy, automatic, \
    findZeroSections, findAsciiSections, findXMLSection
  from .util import findValue, findBytes, fill, verify, byteToString, pretty, label, diffStrings
  #pylint: enable=import-outside-toplevel

  def __init__(self, fileName, verbose=1):
    '''
    initialize

    Args:
      filename: name of file
      verbose: verbose output. 0=no output; 1=minmal; 2=more

    '''
    #All options should be here. GUI can change these defaults
    self.optGeneral   = {'maxSize':-1}
    self.optFind      = {'maxError':1e-4}
    self.optAutomatic = {'minChars':10,   'minArray': 50, 'maxExp':11, 'minZeros':16, 'minEntropy':3}
    self.optEntropy   = {'blockSize':256, 'skipEvery':5}

    self.fileName   = fileName
    self.content    = SortedDict()
    self.periodicity= {}
    self.file       = None
    self.printMode  = 'dec' #      printMode: dec-decimal, hex-hexadecimal
    self.verbose    = verbose
    self.meta       = {'vendor':'', 'label':'', 'software':'', 'ext':os.path.splitext(fileName)[1][1:]}

    self.initContent()
    return
