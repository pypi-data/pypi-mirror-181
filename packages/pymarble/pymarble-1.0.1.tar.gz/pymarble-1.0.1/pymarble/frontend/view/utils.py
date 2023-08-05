'''
Module contains helper variables and functions for the MARBLE GUI application
'''
import os
import time
from multiprocessing import Process
# The modules above are imported to create a setTimeout() [JS] like function in python
# to be used to imitate the proces of a backend call

# Define path to directory containing all images
base_file_path = os.sep.join((__file__.split(os.sep)[:-2]))
IMAGE_DIR_PATH = os.path.join(base_file_path, 'static', 'images')

# Defining a dictionary of variable name suffixes
VARIABLE_OPTIONS = {
  'BUTTON_ACTION': '_button_action',
  'MENU': '_menu',
}

# Defining Menu bar options and corresponding action options
MENU_TREE = {
  'File': ['New File', 'Open File', 'Save File', 'Revert File', 'Close File'],
  'Edit': ['Undo', 'Redo', 'Copy', 'Cut', 'Paste', 'Find', 'Replace'],
  'View': ['Open View', 'Appearance', 'Explorer', 'Problems', 'Testing', 'Word Wrap'],
  'Help': ['Get Started', 'Documentation', 'About']
}

# Color identifiers
COLOR_KEYS = {
  "RED": "_r",
  "YELLOW": "_y",
  "GREEN": "_g"
}

# Color profiles for UI
STYLESHEET_CONSTS = {
  "colors": {
    COLOR_KEYS["RED"]: "#df3c3c",
    COLOR_KEYS["YELLOW"]: "#f7f257",
    COLOR_KEYS["GREEN"]: "#83df50"
  },
  "size": {
    "radio": 20,
  },
  "border": {
    "radio" : 2
  }
}

# Section Type
DTYPE_TO_COLOR = {
  "b": ["#e5e5e5","#cccccc"],
  "c": ["#e5fdff","#65aeb5"],
  "d": ["#eaeafe","#877bd1"],
  "f": ["#eaeafe","#877bd1"],
  "i": ["#9a031e","#9a031e"],
  "B": ["#9a031e","#9a031e"]
}

# Color-probability map
PROBABILITY_MAP = {
  COLOR_KEYS["RED"]: 25,
  COLOR_KEYS["YELLOW"]: 50,
  COLOR_KEYS["GREEN"]: 75
}

# Creating an appropriate variable name
def createVariableNames(inputString, ext):
  '''
  Function to help create variables for different types of menu options/option buttons
  '''
  # converting string to lowercase
  lowerString = inputString.lower()
  # replacing all whitespaces with _, if input string contains more than one word
  prefix = lowerString.replace(' ', '_')
  return prefix+VARIABLE_OPTIONS[ext]

def createStyleSheet(element, props):
  '''
  Creates stylesheet for requested elements based on props given
  '''
  style = None
  if element == 'radio':
    colorCode = props["color"]
    radioSize = STYLESHEET_CONSTS["size"]["radio"]
    radioBorder = STYLESHEET_CONSTS["border"]["radio"]
    radioColor = STYLESHEET_CONSTS["colors"][colorCode]

    style = '''
    QRadioButton::indicator {{
      border: {border}px solid black;
      height: {height}px;
      width: {size}px;
      margin-right: -4px;
    }}
    QRadioButton::indicator:checked {{
      background: {color};
    }}
    '''.format(size=radioSize - radioBorder * 2,
               border=radioBorder,
               height=(radioSize - radioBorder * 2)*2,
               color=radioColor)
  elif element == 'groupbox':
    style = '''
    QGroupBox {{
    background-color: {background_color};
    border: 1px solid {border_color};
    border-left: {flag_width}px solid {flag_color};
    }}
    '''.format(flag_width=20,
              background_color=DTYPE_TO_COLOR.get(props)[0],
              flag_color=DTYPE_TO_COLOR.get(props)[1],
              border_color=DTYPE_TO_COLOR.get(props)[1])
  return style

# Imitating the time break of backend call
# SOURCE - https://dreamix.eu/blog/webothers/timeout-function-in-python-3
def secondsPassed():
  '''
  Helper function that should timeout after 5 seconds.
  It simply prints a number and waits 1 second
  '''
  i = 0
  while True:
    i += 1
    print(i)
    time.sleep(1)


def setTimeOut():
  '''
  Each Process has its own memory space.
  Allows us to kill it without worrying that some resources are left open
  '''
  # Create a Process
  actionProcess = Process(target=secondsPassed)

  # Start the process and block it for 5 seconds.
  actionProcess.start()
  actionProcess.join(timeout=10)

  # Terminate the process
  actionProcess.terminate()
