'''
Module contains communication channels for MARBLE GUI
'''
from PyQt5.QtCore import pyqtSignal, QObject

'''
Class that defines custom signals,
used to communicate events across various
classes of the application
'''
class Communicate(QObject):
	'''
  Class that defines custom signals,
  used to communicate events across various
  classes of the application
  '''
	# signals to update UI
	# Signal to draw and repaint the view of the application
	drawSignal = pyqtSignal()
	plotData = pyqtSignal(int)

	# signals to communicate user input/updates
	certainSignal = pyqtSignal(int)
	updateStrValue = pyqtSignal(int, str, str)
	updateIntValue = pyqtSignal(int, str, int)
	updateBoolValue = pyqtSignal(int, str, bool)
	updateSection = pyqtSignal(int, int)
  