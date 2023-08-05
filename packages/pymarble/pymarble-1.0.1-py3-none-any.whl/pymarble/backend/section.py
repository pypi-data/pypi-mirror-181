"""Section of data"""
import struct
import numpy as np

arguments =    ['length','dType','key','unit','link','dClass','count','shape','prob','entropy',\
                'important'     ,'value']
arguments0=    [0       ,''     ,''   ,''    ,''    ,''      ,[]     ,[]     ,0     ,-1.0     ,\
                False           ,''     ]
argumentsType =[int     ,str    ,str  ,str   ,str   ,str     ,list   ,list   ,int   ,float    ,\
                bool            ,str]
'''
  length: length of section, responsible for size, byteSize of section
    - generally length = shape[0]*shape[1]
    - in case garbage (malloc) is in section: length is larger than product of shape
  dClass: meta, primary, count/parameter, ''=unknown
  count: offset/location of the count
    - relates to the shape
    - cannot be the variable name because formalized description should not have variable name
  shape: shape of array for primary data
    - linear vector is turned into shape
    - each primary data should have one.
    - however, not really needed since count says it all
      benefit is only the ability for user to supply shape

  prob = probability: 0, 25, 50,75, 100 = 1-5 stars!
    - 0 unidentified
    - 10 sequences of 00 or FF
    - 40-60 ascii strings: the longer the higher with cutoff at 10-long;
            ascii stings include the following 00
    - 40-60 sequences: tho longer the higher: cutoff at 100-long
    - 100   if manually set key,unit,link
  entropy -> see automaticIdentify:entropy
'''

class Section:
  """
  class that represents each identified section of data
  """
  def __init__(self, **kwargs):
    for idx, name in enumerate(arguments):
      setattr(self, name, argumentsType[idx](kwargs.get(name, arguments0[idx])) )
    if 'data' in kwargs:
      self.setData(data = kwargs['data'])
    if self.shape==[] and self.length>0:
      if self.dType=='c' and self.value!='':
        self.shape=[len(self.value)]
      else:
        self.shape=[self.length]
    return


  def setData(self, **kwargs):
    '''
    Change values

    Args:
       data: string of | separated list with possible spaces
    '''
    for idx, name in enumerate(arguments):
      setattr(self, name, argumentsType[idx](kwargs.get(name, getattr(self,name))) )
    if 'data' in kwargs:
      data = [i.strip() for i in kwargs['data'].split('|')]
      for idx, name in enumerate(arguments):
        if idx<len(data) and len(data[idx])>0:
          if argumentsType[idx]==list:
            setattr(self, name, [int(i) for i in data[idx].split(',')] )
          else:
            if argumentsType[idx]==bool and isinstance(data[idx],str):
              setattr(self, name, data[idx]=='True' )
            else:
              setattr(self, name, argumentsType[idx](data[idx]) )
      #add shape if not given
      if (arguments.index('shape')>=len(data) or self.shape==[]) and self.length>0:
        self.shape=[self.length]
    return


  def __repr__(self, shorten=False):
    '''
    Used for print(Section) or str(Section)
    - use |-system for easy to reading
    - complete data
    - is the text label in the .tags file
    '''
    return '|'.join( self.toList(shorten=shorten) )


  def toCSV(self):
    '''
    Return dictionary for csv format for header of .py file
    - used for save/load of structure information
    '''
    return self.__dict__


  def toList(self, shorten=False):
    '''
    Return list of all arguments
    - used for printing of table
    - clean output before printing / saving in .tags file
    - no shortening of strings since .tags need all

    Args:
      shorten: simplify columns
    '''
    localCopy = self.__dict__.copy()
    localCopy['entropy'] = '{:6.4f}'.format(localCopy['entropy'])     #Prevent issues with diff in tags file
    if shorten and localCopy['dType'] in ['b','B']:
      localCopy['value'] = 'binary string'
    localCopy['count'] = str(localCopy['count'])[1:-1]
    localCopy['shape'] = str(localCopy['shape'])[1:-1]
    data =  sorted(localCopy.items(), key=lambda pair: arguments.index(pair[0]))
    return [str(i) for _,i in data]



  def toPY(self,relPos, content=None, hdf5Branch=None):
    '''
    Return one-line string in python format for body of .py file
    - not used for save/load of structure information

    Args:
      relPos: relative offset for reading compared to last
      content: list of content from calling entity
      hdf5Branch: hdf5Branch to save into
    '''
    if hdf5Branch is None:
      hdf5Branch = 'fOut'
    if self.dType in ['b','B']:
      return None
    if self.dType=='c' or self.dClass=='meta':
      length = str(self.length)  #default: char
      if self.dType!='c':
        length= '"'+self.size()+'"'
      key = self.key.replace(':','_')
      return 'addAttrs('+str(relPos)+', '+length+', '+hdf5Branch+', "'+key+'")\n'
    if self.dType=='i':
      variable = self.key.split('=')[0]
      if content is not None and isinstance(content, str):
        variable = content
      return variable+' = readData('+str(relPos)+', "'+self.size()+'")[0]\n'
    #if data with dTypes: d,f,H
    if len(self.shape) in [0,1] and len(self.count)==1  and np.prod(self.shape)==self.length:
      #default case: shape (un)identified and one count
      variable = content[self.count[0]].key.split('=')[0]
      return 'addData('+str(relPos)+', str('+variable+')+"'+self.dType+'", '+hdf5Branch+', "'\
          +self.key+'", "'+self.unit+'")\n'
    if len(self.shape) == len(self.count) and np.prod(self.shape)==self.length:
      #case: image with x,y count and shape
      variables = [content[i].key.split('=')[0] for i in self.count]
      prodVariables = '*'.join(variables)
      return 'addData('+str(relPos)+', str('+prodVariables+')+"'+self.dType+'", '+hdf5Branch+', "'\
          +self.key+'", "'+self.unit+'", shape=['+','.join(variables)+'])\n'
    if len(self.shape)>0 and len(self.shape)==len(self.count) and self.length>np.prod(self.shape):
      #garbage case: lots of garbage behind real data specified by shape
      variables = [content[i].key.split('=')[0] for i in self.count]
      return 'addData('+str(relPos)+', str('+str(self.length)+')+"'+self.dType+'", '+hdf5Branch+', "'\
          +self.key+'", "'+self.unit+'", shape=['+','.join(variables)+'])\n'
    print("**ERROR in section.py: UNDEFINED shape, count, length:", self.shape, self.count, self.length)
    return 'print("**ERROR occurred during deciphering")\n'


  def byteSize(self):
    '''
    return the byte size of this item
    '''
    return struct.calcsize(str(self.length)+self.dType)


  def size(self):
    '''
    return the size string: e.g. 600d
    '''
    return str(self.length)+self.dType


  @staticmethod
  def pythonHeader():
    '''
    Python header including all python function since
    - they depend on which properties in the section exist (e.g. links)
    - these functions are called by the output of toPY()
    '''
    return """

def addAttrs(relPos, format, hdfBranch, key):
  '''
  helper function: add attribute to branch

  Args:
    relPos: relative file offset
    format: data to read, int=numb. of chars, otherwise 4i
    hdfBrach: branch to add
    key: name of the key

  Returns:
    none
  '''
  fIn.seek(relPos, 1)
  if '-v' in sys.argv:
    print('add Attrs', fIn.tell(), end=' ')
  key = key.lower().replace(' ','_')
  if type(format)==int:
    value = bytearray(source=fIn.read(format)).decode('latin-1')
    if hdfBranch:
      hdfBranch.attrs[key] = value.replace('\\x00','')
  else:
    value = struct.unpack(format, fIn.read(struct.calcsize(format)))
    if hdfBranch:
      if len(value)==0:
        hdfBranch.attrs[key] = value[0]
      else:
        hdfBranch.attrs[key] = value
  if '-v' in sys.argv:
    print(value)
  return


def addData(relPos, format, hdfBranch, key, unit, shape=None):
  '''
  helper function: add data to branch

  Args:
    relPos: relative file offset
    format: data to read, int=numb. of chars, otherwise 4i
    hdfBrach: branch to add
    key: name of the key
    unit: scientific unit
    shape: shape of the array

  Returns:
    success
  '''
  fIn.seek(relPos, 1)
  if '-v' in sys.argv:
    print('add data', fIn.tell())
  data = fIn.read(struct.calcsize(format))
  if len(data) < struct.calcsize(format):
    return False
  data = struct.unpack(format, data)
  if shape is not None:
    data = np.array(data)[:np.prod(shape)].reshape(shape)
  if '-v' in sys.argv:
    if shape is not None and len(shape)==2:
      plt.imshow(data)
    else:
      plt.plot(data,'.')
    plt.show()
  dset = hdfBranch.create_dataset(key, data=data)
  dset.attrs['unit'] = unit
  hdfBranch.attrs['signal'] = key
  return True


def readData(relPos, format):
  '''
  helper function: read few values and return

  Args:
    relPos: relative file offset
    format: data to read, int=numb. of chars, otherwise 4i

  Returns:
    value as list
  '''
  fIn.seek(relPos, 1)
  if '-v' in sys.argv:
    print('read data', fIn.tell(), end=' ')
  data = fIn.read(struct.calcsize(format))
  if len(data) < struct.calcsize(format):
    return False
  if '-v' in sys.argv:
    print(struct.unpack(format, data))
  return struct.unpack(format, data)

"""
