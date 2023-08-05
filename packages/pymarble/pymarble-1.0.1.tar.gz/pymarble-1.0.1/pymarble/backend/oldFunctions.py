"""Find differences between binary files, not helpful"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from skimage.morphology import closing


def compare(self, otherFileName):
  '''
  not needed anymore since this compare assumes a static binary file
  -> REPLACE WITH DIFF OF STRUCTURE INFORMATION of csv-part in python file

  perform diff on this and other file: compare both files and print difference

  offset not clear from here

  Args:
      otherFileName: name of file to compare to
  '''
  lenClose = 16

  self.file.seek(0)
  data1 = self.file.read()
  data2 = open(otherFileName,'rb').read()

  diffStart = None
  bin1s, bin2s  = [], []
  xPlot,yPlot1, yPlot2  = [], [], []
  for i in range( max(len(data1),len(data1)) ):
    bin1 = data1[i] if i<len(data1) else None
    bin2 = data2[i] if i<len(data2) else None
    if bin1!=bin2:
      if diffStart is None:
        diffStart = i
      bin1s.append(bin1)
      bin2s.append(bin2)
      xPlot.append(i)
      yPlot1.append(bin1)
      yPlot2.append(bin2)
    if bin1==bin2 and diffStart is not None:
      if len(bin1s)<5:
        bin1s = ','.join([hex(j)[2:].upper() for j in bin1s])
        bin2s = ','.join([hex(j)[2:].upper() for j in bin2s])
        print(self.pretty(diffStart),'-',self.pretty(i-1),'| A:',bin1s,'  B:',bin2s)
      else:
        print(self.pretty(diffStart),'-',self.pretty(i-1),'|',len(bin1s),'bytes')
      diffStart = None
      bin1s, bin2s  = [], []
  #plot
  ax1 = plt.subplot(111)
  ax2 = ax1.twinx()
  mask = np.zeros(self.fileLength, dtype=np.bool)
  mask[xPlot] = 1
  mask = closing(mask, np.array([0]+[1]*lenClose+[0]))
  ax1.plot(mask,c='k')
  ax2.plot(xPlot,yPlot1,'.')
  ax2.plot(xPlot,yPlot2,'.')
  def toHex(num, _):
    return ('0x%x' % int(num)).upper()
  ax1.get_xaxis().set_major_formatter(ticker.FuncFormatter(toHex))
  ax2.get_yaxis().set_major_formatter(ticker.FuncFormatter(toHex))
  ax1.set_xlim(left=0)
  ax2.set_ylim(bottom=0)
  ax1.set_ylim([-0.02,1.02])
  ax1.set_xlabel('position')
  ax1.set_ylabel('different')
  ax2.set_ylabel('value')
  plt.show()
  return
