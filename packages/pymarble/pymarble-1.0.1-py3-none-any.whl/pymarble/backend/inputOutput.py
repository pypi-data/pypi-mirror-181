"""input and output to files; plot to screen"""
import os, struct, json, io
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .section import Section, arguments

def initContent(self):
  '''
  set binary file initially

  One could think of moving data into ram and use multiprocess to work in parallel
    - options are (disk,virt-disk, ram)
    - if running on one processor it does not make much sense / faster
    - if data too big for RAM, chunk it into pieces that fit into RAM
    - parallel actions on the self.content are difficult to coordinate
  '''
  self.fileLength = os.path.getsize(self.fileName)
  self.fileType   = 'disk'  #'disk': read directly from disk; 'ram' copy file in ram and work in virt. disk
                            #'data': #futureFeature copy file into data & work on different sections parallel
  if self.fileType=='disk':
    self.file       = open(self.fileName,'br')
    #runtime python test: 26.5sec # runtime shell test: 1m3.577s
  else:
    file            = open(self.fileName,'br')
    self.file       = io.BytesIO(file.read())
    file.close()
    #runtime python test: 22.8sec  # runtime shell test: 1m8.051s
  # set initial content
  self.content[np.int64(0)] = Section(length=self.fileLength, dType='b',prob=0)
  # output of initialization
  if self.verbose>1:
    print("Process file:",self.fileName,' of length',self.pretty(self.fileLength),'in mode',self.printMode)
  return


def saveTags(self):
  '''
  Output file content to .tags file
  '''
  if len(self.content)<2:
    print("**ERROR in SaveTags: NOT ENOUGH ENTRIES in content. I exit.")
    return
  tagsFile = self.fileName+'.tags'
  with open(tagsFile, 'w') as fOut:
    fOut.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    fOut.write('<wxHexEditor_XML_TAG>\n')
    fOut.write('  <filename path="'+self.fileName+'">\n')
    for idx, start in enumerate(self.content):
      section = self.content[start]
      end     = start + struct.calcsize(str(section.length)+section.dType)
      fOut.write('    <TAG id="'+str(idx)+'">\n')
      fOut.write('      <start_offset>'+str(start)+'</start_offset>\n')
      fOut.write('      <end_offset>'  +str(end)+'</end_offset>\n')
      fOut.write('      <tag_text>'    +str(section)+'</tag_text>\n')
      if section.dType=='d':
        fOut.write('      <font_colour>#000000</font_colour>\n')
        fOut.write('      <note_colour>#4EB371</note_colour>\n')
      elif section.dType=='f':
        fOut.write('      <font_colour>#000000</font_colour>\n')
        fOut.write('      <note_colour>#4E5FB3</note_colour>\n')
      elif section.dType=='c':
        fOut.write('      <font_colour>#000000</font_colour>\n')
        fOut.write('      <note_colour>#B38D4E</note_colour>\n')
      elif section.dType=='i':
        fOut.write('      <font_colour>#000000</font_colour>\n')
        fOut.write('      <note_colour>#FFF700</note_colour>\n')
      elif section.dType=='B':
        fOut.write('      <font_colour>#000000</font_colour>\n')
        fOut.write('      <note_colour>#FFFFFF</note_colour>\n')
      else:
        fOut.write('      <font_colour>#000000</font_colour>\n')
        fOut.write('      <note_colour>#FF0000</note_colour>\n')
      fOut.write('    </TAG>\n')
    fOut.write('  </filename>\n')
    fOut.write('  <meta>'+json.dumps(self.meta)+'</meta>\n')
    fOut.write('  <periodicity>'+json.dumps(self.periodicity)+'</periodicity>\n')
    fOut.write('</wxHexEditor_XML_TAG>\n')
  return


def loadTags(self):
  '''
  .tags file read into content
  '''
  tagsFile = self.fileName+'.tags'
  if not os.path.exists(tagsFile):
    print('**ERROR in loadTags: file does not exist',tagsFile,'. I exit.')
    return
  tree = ET.parse(tagsFile)
  root = tree.getroot()
  meta = root.find('meta')
  self.meta = json.loads(meta.text)
  periodicity = root.find('periodicity')
  self.periodicity = json.loads(periodicity.text)
  filename = root.find('filename')
  for tag in list(filename):
    start = int(tag.find('start_offset').text)
    self.content[start] = Section(data=tag.find('tag_text').text)
  return


def savePython(self):
  '''
  Output file content to .py file
  header has formalized description of file-structure
  '''
  pyFile = os.path.splitext(self.fileName)[0]+'.py'
  with open(pyFile, 'w') as fOut:
    # PYTHON PART
    # header
    fOut.write("#!/usr/bin/python3\n")
    fOut.write("# INFO: THIS PART IS IS FOR HUMANS BUT IT IS IGNORED BY MARBLE")
    fOut.write(self.pythonHeader())
    fOut.write(Section.pythonHeader())
    fOut.write('\n###MAIN FUNCTION\ntry:\n')
    # body: for loop items
    inForLoop = False
    if 'count' in self.periodicity:
      start = int(self.periodicity['count'])
      line = self.content[start].toPY(start, 'numberOfTests')
      fOut.write('  fIn.seek(0)\n')
      fOut.write('  '+line)
      self.content[start].dClass='meta'
    #body: things other than foor loop
    fOut.write('  fIn.seek(0)\n')
    lastOutput = 0
    if not bool(self.periodicity):  #if no periodicity
      fOut.write('  hdfBranch_ = fOut.create_group("test_1")\n')
      fOut.write('  hdfBranch_.attrs["NX_class"] = b"NXentry"\n')
      fOut.write('  hdfBranch = hdfBranch_.create_group("data")\n')
      fOut.write('  hdfBranch.attrs["NX_class"] = b"NXdata"\n')
    for start in self.content:
      if 'start' in self.periodicity and start==int(self.periodicity['start']):
        fOut.write('  for idxTest in range(numberOfTests):\n')
        fOut.write('    hdfBranch_ = fOut.create_group("test_"+str(idxTest+1))\n')
        fOut.write('    hdfBranch_.attrs["NX_class"] = b"NXentry"\n')
        fOut.write('    hdfBranch = hdfBranch_.create_group("data")\n')
        fOut.write('    hdfBranch.attrs["NX_class"] = b"NXdata"\n')
        inForLoop = True
      sect= self.content[start]
      if not sect.important:  #don't output unimportant items
        continue
      branchName = None
      if ( sect.dClass in ['meta','primary'] and inForLoop ) or not bool(self.periodicity):
        branchName = 'hdfBranch'
      line = self.content[start].toPY(start-lastOutput, self.content, branchName)
      if line:
        forLoopPrefix = '  ' if inForLoop else ''
        fOut.write('  '+forLoopPrefix+line)
        lastOutput = start+self.content[start].byteSize()
      if 'end' in self.periodicity and start==int(self.periodicity['end']):
        inForLoop = False
    # footer
    remainderContent = 0 if 'count' in self.periodicity else self.fileLength-lastOutput
    # create periodicity function
    # - if periodicity: remainder does not always have to be zero, no better logic
    #   one should evaluate by running through actual binary file
    fOut.write('  if os.path.getsize(fileNameIn)-fIn.tell()!='+str(remainderContent)+':\n')
    fOut.write('    print("Translation NOT successful")\n')
    fOut.write('  else:\n')
    fOut.write('    print("Translation successful")\n')
    fOut.write('\nexcept:\n  print("**ERROR** Exception in translation")\n')

    # FORMALIZED DESCRIPTION OF BINARY-FILE-STRUCTURE
    fOut.write("\n\n\n'''\n")
    fOut.write("# INFO: THIS PART IS LOADED BY MARBLE\n")
    fOut.write('# version= 1.0\n')
    fOut.write('# meta='+json.dumps(self.meta)+'\n')
    fOut.write('# periodicity='+json.dumps(self.periodicity)+'\n')
    fOut.write('# length='+str(len(self.content))+'\n')
    dataframe = pd.DataFrame()
    for start in self.content:
      lineData = dict( self.content[start].toCSV() )  #make a copy
      #first case: if len is represented by shape and its primary data: invalidate length
      if (lineData['shape']!=[] and np.prod(lineData['shape']) == lineData['length'] and \
        lineData['dClass']=='primary'):
        lineData['length']=-1
      lineData['value'] = lineData['value'].encode('unicode_escape')
      dataframe = pd.concat([dataframe, pd.Series(lineData).to_frame().T], ignore_index=True)
    dataframe = dataframe[arguments]         #sort colums by defined order
    del dataframe['shape']
    dataframe.to_csv(fOut, index=False)
    fOut.write("'''\n")
  return


def loadPython(self, pyFile=None):
  '''
  load python file and parse its header information
  '''
  compare = True
  if pyFile is None:
    pyFile = os.path.splitext(self.fileName)[0]+'.py'
    compare = False

  with open(pyFile, 'r') as fIn:
    for line in fIn:
      if line.strip() == '# INFO: THIS PART IS LOADED BY MARBLE':
        break
    line = fIn.readline().strip()
    if line.startswith('# meta='):
      self.meta = json.loads(line[7:])
    else:
      print("**ERROR: python does not match loadPython meta")
      return
    line = fIn.readline().strip()
    if line.startswith('# periodicity='):
      self.periodicity = json.loads(line[14:])
    else:
      print("**ERROR: python does not match loadPython periodicity")
      return
    line = fIn.readline().strip()
    if not line.startswith('# length='):
      print("**ERROR: python does not match loadPython length")
      return
    numLines = int(line[9:])
    readData = pd.read_csv(fIn, nrows=numLines).fillna('')
    readData = readData.to_dict(orient='records')
    start = 0
    #general version=>specific to this file
    for row in readData:
      row['shape'] = []
      if row['count'] =='[]':
        row['count']=[]
      else:
        anchorPoints = [int(i) for i in row['count'][1:-1].split(',')]
        row['count'] = []
        for jStart in anchorPoints:
          self.file.seek(jStart)
          data = self.file.read(self.content[jStart].byteSize())
          data = struct.unpack(self.content[jStart].size(), data)[0]
          row['shape'].append(data)
          row['count'].append(jStart)
      #for all sections
      section = Section(**row)
      section.value = section.value.encode('utf-8').decode('unicode_escape')
      if section.length<0:
        section.length = int(np.prod(section.shape))
      if compare and section.dType in ['b','c']:
        self.file.seek(start)
        newText = None
        if section.dType=='b':
          newText = self.byteToString(self.file.read(section.length),1)
        else:
          newText = bytearray(source=self.file.read(section.length)).decode('utf-8', errors='replace')
        diffText, diffFlag = self.diffStrings(section.value,newText)
        if diffFlag and section.prob<90:
          print('\nDifferent at',start,'|py: red, data: green')
          print(diffText)
      #save and move on
      self.content[start] = section
      start += section.byteSize()
  return


def plot(self, start, plotMode=1, show=True):
  '''
  Plot as graph values found at location i

  Args:
      start: starting location
      plotMode: plot as 1d time-series (1) or as 2d image (2)
  '''
  start = int(start)
  if not start in self.content:
    print("**ERROR: cannot print at start",start,'. I exit')
    return None
  section = self.content[start]
  #offsets on the x-axis
  #valuesX = np.linspace(start, start+section.byteSize(), section.length)
  #length on the x-axis
  valuesX = range(1, section.length+1)
  self.file.seek(start)
  data = self.file.read(section.byteSize())
  if len(data) !=struct.calcsize(section.size()):
    print('**ERROR: cannot plot size does not fit byte-length')
    return None
  valuesY = struct.unpack(section.size(), data) #get data
  if plotMode==1:
    ax1 = plt.subplot(111)
    ax1.plot(valuesX, valuesY, '-o')
    def toHex(num, _):
      return '0x%x' % int(num)
    if self.printMode=='hex':
      ax1.get_xaxis().set_major_formatter(ticker.FuncFormatter(toHex))
    yMin = np.percentile(valuesY,2)
    yMax = np.percentile(valuesY,98)
    yMin = 1.1*yMin-0.1*yMax
    yMax = 1.1*yMax-0.1*yMin
    # ax1.axhline(0, color='k', linestyle='dashed')
    # ax1.axvline(1, color='k', linestyle='dashed')
    ax1.set_ylim([yMin,yMax])
    ax1.set_xlabel('increment')
    ax1.set_ylabel('value')
  elif plotMode==2:
    sideLength = int(np.sqrt(len(valuesY)))
    valuesY = np.array(valuesY).reshape((sideLength,sideLength))
    ax1 = plt.subplot(111)
    image = ax1.imshow(valuesY)
    ax1.axis('off')
    plt.colorbar(image)
  if show:
    plt.show()
    return None
  return ax1


def pythonHeader(self):
  '''
  Header written at top of python file
  - includes only the python code and not the predefined functions
  - uses metadata to infuse python header and hdf5 metadata
  '''
  return """
'''
convert """+self.meta['vendor']+" "+self.meta['ext']+""" to .hdf5 file

in_file:
  label: """+self.meta['label']+"""
  vendor: """+self.meta['vendor']+"""
  software: """+self.meta['software']+"""
out_file:
  label: custom HDF5 with k-tests as well as metadata and converter groups

Help:
  start as: [file-name.py] [binary-file]
  -v: verbose = adds additional output
'''
import struct, sys, os, hashlib
import h5py                                    #CWL requirement
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

convURI = b'https://raw.githubusercontent.com/main/cwl/"""+self.meta['ext']+"""2hdf.cwl'
convVersion = b'1.5'

## COMMON PART FOR ALL CONVERTERS
fileNameIn = sys.argv[1]
fileNameOut= os.path.splitext(fileNameIn)[0]+'.hdf5'
fIn   = open(fileNameIn,'br')
fOut  = h5py.File(fileNameOut, 'w')
fOut.attrs['uri'] =     convURI
fOut.attrs['version'] = convVersion
fOut.attrs['original_file_name'] = fileNameIn
md5Hash = hashlib.md5()
md5Hash.update(fIn.read())
fOut.attrs['original_md5sum'] = md5Hash.hexdigest()
fOut.attrs['default'] = b'test_1'

"""
