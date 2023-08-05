"""Search file and find values"""
import struct, math, re, difflib
import numpy as np
from .section import Section, arguments

def findValue(self, value, dType='d', verbose=True, offset=0):
  '''
  find value in binary file by iterating all offsets

  Args:
    value: value to be found
    dType: ['d','i'] data-type: double or int
    verbose:  print to screen
    offset: offset to start from

  Returns:
    sorted by error
  '''
  if isinstance(value, str):
    value = float(value)
  if not verbose:
    allFound, allError = [], []
  byteSize = struct.calcsize(dType)
  for offsetI in range(byteSize):
    self.file.seek(offsetI+offset)
    data = self.file.read()
    numData = math.floor(len(data)/byteSize)
    data = data[:struct.calcsize(str(numData)+dType)] #crop binary data
    data = np.array(struct.unpack(str(numData)+dType, data), dtype=np.float128)    #get data
    mask = np.isfinite(data)
    data[mask] = np.abs((data[mask]-value)/value)     #relative difference
    data[~mask] = 1.
    found = np.where(data<self.optFind['maxError'])[0]       #threshold
    output = [self.pretty(i) for i in offsetI+offset+found*byteSize] #output
    if verbose:
      for idx, offsetJ in enumerate(output):
        print(offsetJ,'found '+str(value)+' with error '+str(data[found][idx]))
      if len(output)==0:
        print('... found nothing')
    else:
      allFound += output
      allError += list(data[found])
  if not verbose:
    return [x for _, x in sorted(zip(allError, allFound))]
  return None


def findBytes(self, value, dType='d', offset=0):
  '''
  find value in binary file by looking for the appropriate byte string

  https://stackoverflow.com/questions/3217334/searching-reading-binary-data-in-python

  Args:
    value: value to be found
    dType: ['d','f','i', 's'] data-type: double or int or string
    offset: offset to start from
  '''
  if dType=='s':
    searchString = bytes(value, 'utf-8').hex()
  else:
    if dType in ['i', 'H']:
      value = int(value)
      searchString = struct.pack(dType,value).hex()
    elif dType in ['f', 'd']:
      value = float(value)
      searchString = struct.pack(dType,value).hex()
      searchString = searchString[2:]  #chop of first byte (two chars) to allow for close values not precise
    else:
      print("*WARNING NOT TESTED*")
  self.file.seek(offset)
  data = self.file.read()
  found = data.hex().find(searchString)
  if found%2==1:                       #if odd: this is not a valid result, cause value not found
    found = -2
  found = int(found/2)                 #divide by 2 because byte has 2 chars
  if dType in ['f', 'd']:
    found -= 1                         #subtract because first byte was cutoff
  if self.verbose>0:
    if found<0:
      print('Number not found in file')
    else:
      print(self.pretty(found), 'found value '+str(value))
  return found


def label(self, start, data):
  '''
  Manually label / define key a section
  - Set probability to 100 and important to true since why would the user label it
  - if dType=f or d are labeled
    - search for that variable
    - link to that variable


  Args:
    start: start offset
    data: data of section
  '''
  start = int(start)
  #TODO_P3 z Temporary verification until version 1.1
  if start<0 or start>self.fileLength:
    print("**ERROR: start value does not make sense", start)
    return
  if start in self.content:  #edit
    self.content[start].setData(data=data)
  else:                           #create new
    self.content[start] = Section(data=data)
  self.content[start].prob = 100  #otherwise many backend scripts and backend cases do not work
  self.content[start].important = True
  if len(self.content[start].value)>40:
    self.content[start].value = ''
  runFill = not data.startswith('||')
  section = self.content[start]
  if section.dType in ['f','d','H']:
    #find count in file
    length = section.length
    if section.shape != [] and np.prod(section.shape)<length:
      # garbage at end of data-set
      length = np.prod(section.shape)
    anchor = None
    prevKvariables = 0
    #search existing anchors
    for startJ in self.content:
      sectionJ = self.content[startJ]
      if sectionJ.key.endswith(str(length)) and sectionJ.dType=='i':
        anchor = startJ
        break
      if re.search(r'^k\d+=', sectionJ.key) and sectionJ.dType=='i':
        prevKvariables += 1
    if anchor is None:    #only if not already found: create new
      anchor = self.findBytes(length,'i')
      if anchor>=0:
        self.content[anchor] = Section(length=1, dType='i', key='k'+str(prevKvariables+1)+'='+str(length),\
                                       prob=100, dClass='count', important=True)
        runFill = True
    #create link / enter property count
    if section.count == []:
      section.setData(count=[anchor])
    if len(section.count)>len(section.shape):
      shape = []
      for iCount in section.count:
        self.file.seek(iCount)
        iLength = self.file.read(self.content[iCount].byteSize())
        iLength = struct.unpack( self.content[iCount].size(), iLength)[0]
        shape.append(iLength)
      section.setData(shape=shape)
    section.setData(dClass='primary')
  elif 'count' not in data:
    section.setData(dClass='meta')
  if runFill:
    self.fill()
  return


def fill(self):
  '''
  Fill content by labeling undefined sections to be "undefined" binary data
  - cleaning / repair all cases of overlap
  - remove all 0-length items
  '''
  if len(self.content)<1:
    print("**ERROR in FILL: One entry required. I exit.")
    return
  rerun = True
  while rerun:  #loop until all changes made
    rerun = False
    toDelete = []
    starts = list(self.content)
    for idx,start in enumerate(starts):
      section = self.content[start]
      if section.length==0 and section.dType=='b':  #if byte of zero length
        toDelete.append(start)
      elif section.length<self.optAutomatic['minArray'] and section.dType in ['f','d']:
        #if data less that supposed
        toDelete.append(start)
      elif idx+1<len(starts) and section.dType=='c' and self.content[starts[idx+1]].dType=='B':
        #if text is followed by a zeros
        self.content[start].length += self.content[starts[idx+1]].length #   add zeros to text
        toDelete.append(starts[idx+1])                                   #   remove zeros
      elif section.entropy<0:  #repair missing entropies
        self.entropy(start)
    for start in toDelete:
      del self.content[start]
    toDelete = []
    starts = list(self.content)
    #create section before first entry
    if starts[0]>0:
      self.file.seek(0)
      text = self.byteToString(self.file.read(starts[0]),1)
      self.content[0] = Section(length=starts[0], dType='b', value=text)
      self.entropy(0)

    #create sections between sections
    for idx, start in enumerate(starts[:-1]):
      section = self.content[start]
      end = start + section.byteSize()
      if end<starts[idx+1]:
        #there is a hole, fill it with a section
        self.file.seek(end)
        text = self.byteToString(self.file.read(starts[idx+1]-end),1)
        self.content[end] = Section(length=starts[idx+1]-end, dType='b', value=text)
        self.entropy(end)
      elif end>starts[idx+1]:
        #there is an overlapp, shorten something
        if section.prob < self.content[ starts[idx+1] ].prob: #repair: shorten this section
          if struct.calcsize(section.dType)>1:
            # print("**WARNING: shorten this section with possibly important data, data-length>1B.")
            rerun = True
          section.length = int((starts[idx+1]-start)/struct.calcsize(section.dType))
          self.file.seek(start)
          section.value   = self.byteToString(self.file.read(section.length),1)
          self.content[start] = section
          self.entropy(start)   #set entropy
          if self.verbose>1:
            print('Shorten this entry',start,'=>end='+str(end)+\
              ', because next section starts at',starts[idx+1])
        else:  #repair: move next section to end of this section; shorten next section
          toDelete.append(starts[idx+1])
          secNext = Section(data=str(self.content[starts[idx+1]]))
          secNext.length = secNext.length-(end-start)
          if secNext.length > 0:   #only add if length is positive
            self.file.seek(end)
            secNext.value   = self.byteToString(self.file.read(secNext.length),1)
            self.content[end] = secNext
            self.entropy(end)
            if self.verbose>1:
              print('Shorten next entry',starts[idx+1])
          else:
            rerun = True
            if self.verbose>1:
              print('Shorten next entry',starts[idx+1],': do not since too short')
    for start in toDelete:
      del self.content[start]

    #create section after last section
    if starts[-1] in self.content:  #if last section still there
      section = self.content[starts[-1]]
      newStart = starts[-1]+struct.calcsize(str(max(section.length,0))+section.dType)#max: prevent neg. numbers
      if newStart<self.fileLength:
        self.file.seek(newStart)
        text = self.byteToString(self.file.read(self.fileLength-newStart),1)
        self.content[newStart] = Section(length=self.fileLength-newStart, dType='b', value=text)
        self.entropy(newStart)
  return


def verify(self):
  '''
  Verify some sanity tests
  '''
  for start in self.content:
    sect = self.content[start]
    if sect.dType not in ['b', 'B', 'f', 'd', 'i', 'c', 'H']:
      print('**ERROR: there is a non-defined dType',sect.dType,'| change to b')
      sect.dType='b'
    argumentsExist = sorted(list(self.content[start].__dict__))
    if argumentsExist != sorted(arguments):
      print('**ERROR: initialization error in Section')
      print('    do exist',argumentsExist)
      print('should exist',sorted(arguments))
  return



@staticmethod
def byteToString(aString, spaceEvery=1):
  '''
  convert bytestring to easy to read string

  Args:
      aString: byte-string
      spaceEvery: white-space for easy reading
  '''
  aString = aString.hex().upper()
  if spaceEvery>0:
    spaceEvery *= 2
    aString = ' '.join(aString[i:i+spaceEvery] for i in range(0, len(aString), spaceEvery))
  else:
    listI = [int(aString[i:i+2], base=16) for i in range(0,len(aString),2) ] #list of integer/char
    listI = np.split(listI, np.where(np.diff(listI) != 0)[0]+1)              #find consequtive entries
    aString = ''.join([''.join([hex(j)[2:].zfill(2) for j in i]) if len(i)<3 or i[0]>0 \
      else ' '+str(len(i))+'*00 ' for i in listI])
  return aString


@staticmethod
def diffStrings(old, new):
  '''
  determine difference between two strings and color those

  based on
  https://stackoverflow.com/questions/32500167/how-to-show-diff-of-two-string-sequences-in-colors

  Future questions:
  - try diff for byteString directly
  - does one need to output equal? If not, the start point does not make sense=>make sense
  - how can we improve (add '\n'); good for large differences
  - do automatically subdivide into sections: equal and differences
  - it would be best to have 00 00 00 reduced to 00

  Args:
    old (string): first string
    new (string): second string

  Returns:
    colored output
  '''
  red = lambda text: f"\033[38;2;255;0;0m{text}\033[0m"
  green = lambda text: f"\033[38;2;0;255;0m{text}\033[0m"

  result = ""
  codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
  differenceFlag = False
  for code in codes:
    #length = max(code[2]-code[1], code[4]-code[3])
    if code[0] == "equal":
      result += (old[code[1]:code[2]])
    elif code[0] == "delete" and len(bytes(filter(None,bytearray(old[code[1]:code[2]],'utf-8'))))>0:
      result += red(old[code[1]:code[2]])
      differenceFlag = True
    elif code[0] == "insert" and len(bytes(filter(None,bytearray(new[code[3]:code[4]],'utf-8'))))>0:
      result += green(new[code[3]:code[4]])
      differenceFlag = True
    elif code[0] == "replace" and (len(bytes(filter(None,bytearray(old[code[1]:code[2]],'utf-8'))))>0 \
                                or len(bytes(filter(None,bytearray(new[code[3]:code[4]],'utf-8'))))>0):
      result += (red(old[code[1]:code[2]]) + green(new[code[3]:code[4]]))
      differenceFlag = True
  return result, differenceFlag


def pretty(self, number):
  '''
  convert decimal or hexdecimal number in easy to read string

  Args:
      number: integer to convert to hex
  '''
  if isinstance(number, str):
    number = int(number.replace(':',''), 0)
  if self.printMode=='dec':
    formatString = "{:0"+str(len(str(self.fileLength)))+"d}"
    return formatString.format(number)
  aString = hex(number)[2:]
  sRef = hex(self.fileLength)[2:]
  aString = '0'*(len(sRef)-len(aString)) + aString
  aList = [aString[max(i-4,0):i] for i in list(np.arange(len(aString),0,-4))]
  aList.reverse()
  return '0x'+':'.join(aList)
