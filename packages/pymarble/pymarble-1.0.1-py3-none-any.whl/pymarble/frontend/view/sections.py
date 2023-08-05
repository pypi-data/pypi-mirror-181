'''
Module that defines different classes used to define view for MARBLE GUI
'''
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QPushButton,
                             QGridLayout, QComboBox, QLineEdit,
                             QRadioButton, QCheckBox,
                             QHBoxLayout, QWidget, QSpinBox,
                             )
from PyQt5.QtGui import QIcon
from .utils import createStyleSheet, COLOR_KEYS, PROBABILITY_MAP, IMAGE_DIR_PATH

class UISection:
  '''
  Class that handles data sections identified
  from the user loaded file, via the backend run
  '''
  def __init__(self, props):
    self.idx = props["id"]
    self.secKey = props["secKey"]

    # copy of data needed as part of copy-on-write that happens within sections
    self.key = props["data"].key
    self.unit = props["data"].unit
    self.prob = props["data"].prob
    self.link = props["data"].link
    self.count = props["data"].count
    self.shape = props["data"].shape
    self.dType = props["data"].dType
    self.value = props["data"].value
    self.imp = props["data"].important
    self.length = props["data"].length
    self.dClass = props["data"].dClass
    self.entropy = props["data"].entropy
    # other
    self.idx = props["id"]
    self.secKey = props["secKey"]
    self.updatedStart = self.secKey
    self.communicate = props["view"]


  def flagImportant(self):
    '''
    UI method that creates a checkbox for user to flag a section as important
    '''
    importantCheck = QCheckBox("important")
    importantCheck.setChecked(self.imp)
    importantCheck.stateChanged.connect(lambda: self.handleValueChange(importantCheck.isChecked(), "important"))
    return importantCheck

  def createKeyValueBox(self, keyWidget, valueWidget):
    '''
    UI method to create a key-value UI pair of widgets
    '''
    layout = QHBoxLayout()
    layout.addWidget(keyWidget)
    layout.addWidget(valueWidget)
    return layout

  def createEditButton(self, editForm):
    '''
    UI method that creates the edit button for each section
    '''
    editIcon = QIcon(os.path.join(IMAGE_DIR_PATH,"show_more_less.png"))
    editButton = QPushButton(editIcon, '')
    editButton.clicked.connect(lambda: handleEdit(editForm))

    def handleEdit(editForm):
      '''
      Handler function that allows section to expand/contract
      to allow editing of non-prominent section data
      '''
      editForm.setVisible(not editForm.isVisible())

    return editButton

  def createEditForm(self):
    '''
    UI method to create an extended form for user to update general section data
    '''
    def setNewStart(value):
      '''
      Function that captures user provided start value
      '''
      self.updatedStart = value

    def sectionSaveButton(layout):
      saveIcon = QIcon(os.path.join(IMAGE_DIR_PATH,"save_sec.jpg"))
      saveButton = QPushButton(saveIcon, "save")
      saveButton.clicked.connect(lambda: self.handleValueChange(self.updatedStart, "start"))
      layout.addWidget(saveButton, 1, (layout.columnCount() +1))

    def inputFor(data, key, title, layout, dtype=None, placeholder=None):
      '''
      UI Function to create custom textfield component
      '''
      # create UI components
      inputLabel = QLabel(f"&{title}:  ")
      if type(data) is int:
        inputField = QSpinBox()
        inputField.setMaximum(100000)
        inputField.setValue(data)
        if key == 'start':
          if dtype == 'f':
            inputField.setSingleStep(4)
          elif dtype == 'd':
            inputField.setSingleStep(8)
      else:
        inputField = QLineEdit()
        inputField.setPlaceholderText(placeholder)
        inputField.setText(data)

      # set appropriate handlers for change
      if key != "start":
        inputField.textChanged.connect(lambda: self.handleValueChange(inputField.text(), key))
      else:
        inputField.valueChanged[int].connect(lambda: setNewStart(inputField.value()))

      # arrange related components together
      inputLabel.setBuddy(inputField)
      layout.addLayout(self.createKeyValueBox(inputLabel, inputField), 1, (layout.columnCount() + 1))

    form = QWidget()
    formLayout = QGridLayout()
    formLayout.setHorizontalSpacing(80)

    inputFor(int(self.secKey), "start", "start", formLayout, dtype=self.dType)
    inputFor(int(self.length), "length", "length", formLayout, dtype=self.dType)
    inputFor(self.dType, "dType", "data type", formLayout, placeholder="enter data type")
    inputFor(self.link, "link", "link", formLayout, placeholder="enter link")
    inputFor(self.dClass, "dClass", "data class", formLayout, placeholder="enter length")
    sectionSaveButton(formLayout)

    form.setLayout(formLayout)
    return form

  def showCertainty(self):
    '''
    UI method that creates a component for user to indicate the certainity of thier input
    '''
    certaintyBox = QWidget()
    certaintyLayout = QHBoxLayout()

    certaintyLabel = QLabel("input certainty:")
    radioRed = QRadioButton()
    radioRed.setStyleSheet(createStyleSheet(element='radio', props={"color": COLOR_KEYS["RED"]}))
    if int(self.prob) <= PROBABILITY_MAP[COLOR_KEYS["RED"]]:
      radioRed.setChecked(True)
    radioRed.toggled.connect(lambda: self.handleValueChange(PROBABILITY_MAP[COLOR_KEYS["RED"]]))

    radioYellow = QRadioButton()
    radioYellow.setStyleSheet(createStyleSheet(element='radio', props={"color": COLOR_KEYS["YELLOW"]}))
    if int(self.prob) > PROBABILITY_MAP[COLOR_KEYS["RED"]] and int(self.prob) < PROBABILITY_MAP[COLOR_KEYS["GREEN"]]:
      radioYellow.setChecked(True)
    radioYellow.toggled.connect(lambda: self.handleValueChange(PROBABILITY_MAP[COLOR_KEYS["YELLOW"]]))

    radioGreen = QRadioButton()
    radioGreen.setStyleSheet(createStyleSheet(element='radio', props={"color": COLOR_KEYS["GREEN"]}))
    if int(self.prob) >= PROBABILITY_MAP[COLOR_KEYS["GREEN"]]:
      radioGreen.setChecked(True)
    radioGreen.toggled.connect(lambda: self.handleValueChange(PROBABILITY_MAP[COLOR_KEYS["GREEN"]]))

    certaintyLayout.addWidget(certaintyLabel)
    certaintyLayout.addWidget(radioRed)
    certaintyLayout.addWidget(radioYellow)
    certaintyLayout.addWidget(radioGreen)
    certaintyBox.setLayout(certaintyLayout)

    return certaintyBox

  def handleValueChange(self, newValue, key="prob"):
    '''
    Functional method to handle value change of input fields
    '''
    if key in ("length", "prob", "start"):
      if key == "start":
        # Needs extra care, separate signal despite being an int value change
        # because slot requires a different kind of handling for this update.
        self.communicate.updateSection.emit(self.secKey, newValue)
      else:
        self.communicate.updateIntValue.emit(self.secKey, key, int(newValue))
    elif isinstance(newValue, bool):
      self.communicate.updateBoolValue.emit(self.secKey, key, newValue)
    else:
      self.communicate.updateStrValue.emit(self.secKey, key, newValue)

class Unidentified(UISection):
  '''
  Sub-class of Section that handles sections of dType == 'b'
  i.e., information not identified by the backend.
  #1 | Unidentified | button->identify (different identify tools) | "edit"
  '''
  def __init__(self, props):
    super().__init__(props)
    self.algoDropdown = None

  def createWidget(self):
    '''
    UI Method to create a widget to handle unidentified sections of the processed file
    '''
    unidentifiedLayout = QGridLayout()

    algoLabel = QLabel("&algorithm:  ")
    self.algoDropdown = QComboBox()
    self.algoDropdown.addItems(["Algo option 01", "Algo option 02", "Algo option 03", "Algo option 04"])
    algoLabel.setBuddy(self.algoDropdown)
    unidentifiedLayout.addLayout(self.createKeyValueBox(algoLabel, self.algoDropdown), 1, 0, Qt.AlignmentFlag.AlignCenter)

    identifyIcon = QIcon(os.path.join(IMAGE_DIR_PATH,"identify.jpg"))
    identifyButton = QPushButton(identifyIcon, "identify")
    identifyButton.clicked.connect(lambda: self.handleIdentify())
    unidentifiedLayout.addWidget(identifyButton, 1, 1, Qt.AlignmentFlag.AlignCenter)

    unidentifiedLayout.setColumnStretch(2, 1)

    flag = self.flagImportant()
    # TODO enable button when functionality is clear, and handle data capture
    flag.setDisabled(True)
    editForm = self.createEditForm()
    editForm.setVisible(False)
    unidentifiedLayout.addWidget(flag, 1, 3, Qt.AlignmentFlag.AlignCenter)
    unidentifiedLayout.addWidget(self.createEditButton(editForm), 1, 4, Qt.AlignmentFlag.AlignCenter)
    unidentifiedLayout.addWidget(editForm, 2, 0, 1, 4, Qt. AlignmentFlag.AlignLeft)

    unidentifiedLayout.setHorizontalSpacing(80)
    return unidentifiedLayout

  def handleIdentify(self):
    '''
    Handler method to communicate users request to identify the section with a specified algo
    TODO implement this and write doc string
    '''
    print(f'Processing Identify. Method selected: {self.algoDropdown.currentText()}')

class TextMetaData(UISection):
  '''
  Sub-class of Section that handles sections of dType == 'c'
  i.e., Textual metadata in the loaded file that was identified by the backend.
  '''
  def __init__(self, props):
    super().__init__(props)
    self.editForm = None

  def createWidget(self):
    '''
    UI method to create a widget to handle textual metadata
    '''
    textMetadataLayout = QGridLayout()

    keyLabel = QLabel("&key:  ")
    keyInput = QLineEdit()
    keyInput.textChanged.connect(lambda: self.handleValueChange(keyInput.text(), "key"))
    keyInput.setPlaceholderText('enter key for value')
    keyInput.setText(self.key)
    keyLabel.setBuddy(keyInput)
    textMetadataLayout.addLayout(self.createKeyValueBox(keyLabel, keyInput), 1, 0, Qt.AlignmentFlag.AlignCenter)

    valueLabel = QLabel("&value:  ")
    sectionValue = QLabel(self.value)
    valueLabel.setBuddy(sectionValue)
    textMetadataLayout.addLayout(self.createKeyValueBox(valueLabel, sectionValue), 1, 1, Qt.AlignmentFlag.AlignCenter)


    textMetadataLayout.setColumnStretch(2, 1)

    certainty = self.showCertainty()
    textMetadataLayout.addWidget(certainty, 1, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

    flag = self.flagImportant()
    editForm = self.createEditForm()
    editForm.setVisible(False)
    textMetadataLayout.addWidget(flag, 1, 4, Qt.AlignmentFlag.AlignCenter)
    textMetadataLayout.addWidget(self.createEditButton(editForm), 1, 5, Qt.AlignmentFlag.AlignCenter)
    textMetadataLayout.addWidget(editForm, 2, 0, 1, 4, Qt. AlignmentFlag.AlignLeft)

    textMetadataLayout.setHorizontalSpacing(80)
    return textMetadataLayout

class PrimaryData(UISection):
  '''
  Sub-class of Section that handles sections of dType == 'd' || dType=='f'
  i.e., information not identified by the backend
  '''
  def __init__(self, props):
    super().__init__(props)
    self.editForm = None

  def createWidget(self):
    '''
    UI method to create a widget to handle primary/raw data
    '''
    primaryDataLayout = QGridLayout()

    keyLabel = QLabel("&key:  ")
    keyInput = QLineEdit()
    keyInput.textChanged.connect(lambda: self.handleValueChange(keyInput.text(), "key"))
    keyInput.setPlaceholderText('enter key for value')
    keyInput.setText(self.key)
    keyLabel.setBuddy(keyInput)
    primaryDataLayout.addLayout(self.createKeyValueBox(keyLabel, keyInput), 1, 0, Qt.AlignmentFlag.AlignCenter)

    unitLabel = QLabel("&unit:  ")
    unitInput = QLineEdit()
    unitInput.textChanged.connect(lambda: self.handleValueChange(unitInput.text(), "unit"))
    unitInput.setPlaceholderText('enter unit for key')
    unitInput.setText(self.unit)
    unitLabel.setBuddy(unitInput)
    primaryDataLayout.addLayout(self.createKeyValueBox(unitLabel, unitInput), 1, 1, Qt.AlignmentFlag.AlignCenter)


    valueLabel = QLabel("&value:  ")
    sectionValue = QLabel(self.value)
    valueLabel.setBuddy(sectionValue)
    primaryDataLayout.addLayout(self.createKeyValueBox(valueLabel, sectionValue), 1, 2, Qt.AlignmentFlag.AlignCenter)

    drawIcon = QIcon(os.path.join(IMAGE_DIR_PATH,"draw.jpeg"))
    drawButton = QPushButton(drawIcon, "plot")
    drawButton.clicked.connect(lambda: self.handleDraw())
    primaryDataLayout.addWidget(drawButton, 1, 3, Qt.AlignmentFlag.AlignCenter)

    primaryDataLayout.setColumnStretch(4, 1)

    if len(self.count) == 0:
      warningIcon = QIcon(os.path.join(IMAGE_DIR_PATH,"warning.jpg"))
      warningButton = QPushButton(warningIcon,'')
      warningButton.setFlat(True)
      warningButton.setToolTip("the corresponding length is not found in file")
      primaryDataLayout.addWidget(warningButton, 1, 5, Qt.AlignmentFlag.AlignRight)

    certainty = self.showCertainty()
    primaryDataLayout.addWidget(certainty, 1, 6, 1, 2, Qt.AlignmentFlag.AlignCenter)

    flag = self.flagImportant()
    editForm = self.createEditForm()
    editForm.setVisible(False)
    primaryDataLayout.addWidget(flag, 1, 8, 1, 1, Qt.AlignmentFlag.AlignVCenter)
    primaryDataLayout.addWidget(self.createEditButton(editForm), 1, 9, 1, 1, Qt.AlignmentFlag.AlignVCenter)
    primaryDataLayout.addWidget(editForm, 2, 0, 1, 8, Qt. AlignmentFlag.AlignLeft)

    primaryDataLayout.setHorizontalSpacing(80)
    return primaryDataLayout

  def handleDraw(self):
    '''
    Handler method that communicates users request to plot primary data of the section
    '''
    self.communicate.plotData[int].emit(self.secKey)
