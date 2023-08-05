"""Functions that output to commandline in commandline usage"""
import re, struct
from prettytable import PrettyTable
from .section import arguments

def printNext(self, count, dType='i'):
  '''
  print next variables in file

  Args:
      count: number of items printed
      dType: ['d','i','f'] data-type: double, int, float
  '''
  currPosition = self.file.tell()
  count = int(count)
  byteSize = struct.calcsize(dType)
  data = self.file.read(count*byteSize)
  data = struct.unpack(str(count)+dType, data) #get data
  print(currPosition,str(data))
  return


def printAscii(self, numRows=None):
  '''
  print the file as ascii and return to zero position

  Args:
      numRows: number of rows to print; default=None: print all
  '''
  bytesPerRow = 64
  offset = 0
  while True:
    data = self.file.read(bytesPerRow)
    if len(data)==0:
      break
    data = bytearray(source=data).decode('utf-8', errors='replace')
    data = ''.join(re.findall(r'[ -~]',data))
    if len(data)>1:
      print(self.pretty(offset)+':',data)
    offset += bytesPerRow
    if numRows and offset/bytesPerRow > int(numRows)-1:
      break
  self.file.seek(0)
  return


def printList(self, printBinary=False):
  '''
  print list of all items
  - shorten long texts to 30 chars

  Args:
    printBinary: print also binary entries
  '''
  table = PrettyTable()
  table.field_names = ['position']+arguments
  for start in self.content:
    if self.content[start].dType not in ['b','B'] or printBinary:
      row = [start]+self.content[start].toList()
      if self.printMode=='hex':
        row[0] = self.pretty(row[0])
        row[1] = self.pretty(row[1])
      row = [str(i)[:30] for i in row]
      table.add_row(row)
  table.align = "l"
  # table.border = False
  table.padding_width = 0
  print(table)
  return
