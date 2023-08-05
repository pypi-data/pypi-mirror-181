#!/usr/bin/env python3
'''
Entry module for MARBLE GUI application
'''

import os
import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QAction, QToolBar,
                             QBoxLayout, QWidget, QMainWindow,
                             QScrollArea, QGridLayout, QGroupBox,
                             QFileDialog, QSizePolicy)
from ..backend import BinaryFile
from ..backend.inputOutput import plot
from ..backend.util import label
from .view.sections import PrimaryData, TextMetaData, Unidentified
from .view.utils import MENU_TREE, IMAGE_DIR_PATH, createVariableNames, createStyleSheet
from .view.comms import  Communicate

class MainWindow(QMainWindow):
  '''
  Main Window class for MARBLE GUI
  '''
  def __init__(self, *args, **kwargs):
    # use to initialize super class' attributes and methods appropriately
    super(MainWindow, self).__init__(*args, **kwargs)

    # Define dtype to UI handler class map
    self._DTYPE_TO_UICLASS = {
      "b": Unidentified,
      "c": TextMetaData,
      "d": PrimaryData,
      "f": PrimaryData
    }

    # Define backend
    self.backend = None

    # Defining window/view parameters
    self.setWindowTitle("MARBLE")

    # QPalette contains color groups for widget states (active, inactive, disabled)
    self.originalPalette = QApplication.palette()
    QApplication.setPalette(self.originalPalette)

    # Menu
    menu = self.menuBar()
    for option in MENU_TREE:
      self.createMenuOption(menu, option)

    # Toolbar
    toolbar = QToolBar("toolbar")

    # NOTE spacer widgets.
    # you can't add the same widget to both left and right.
    # you need two different widgets.
    leftSpacer = QWidget()
    leftSpacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    rightSpacer = QWidget()
    rightSpacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    loadIcon = QIcon(os.path.join(IMAGE_DIR_PATH, "load_file.png"))
    self.loadAction = QAction(loadIcon, "load file", self)
    self.loadAction.triggered.connect(self.handleLoad)
    toolbar.addAction(self.loadAction)

    self.loadedFileIndicator = QAction()
    self.loadedFileIndicator.setVisible(False)
    toolbar.addAction(self.loadedFileIndicator)

    toolbar.addWidget(leftSpacer)

    filterIcon = QIcon(os.path.join(IMAGE_DIR_PATH,"filter.png"))
    self.filterAction = QAction(filterIcon, "filter data", self)
    self.filterAction.triggered.connect(self.drawView)
    self.filterAction.setCheckable(True)
    self.filterAction.setVisible(False)
    toolbar.addAction(self.filterAction)

    saveIcon = QIcon(os.path.join(IMAGE_DIR_PATH, "save.jpeg"))
    self.saveAction = QAction(saveIcon, "save form", self)
    self.saveAction.triggered.connect(self.handleSave)
    self.saveAction.setEnabled(False)
    toolbar.addAction(self.saveAction)

    self.addToolBar(toolbar)

    # App widget and base Layout
    self.window = QWidget(self)

    self.baseLayout = QBoxLayout(QBoxLayout.Direction.TopToBottom, self.window)
    self.setCentralWidget(self.window)

    # Creating a container view to be embedded in the baselayout
    # This is the view that will be drawn and redrawn as UI is processed
    self.containerWidget = QWidget()
    self.containerLayout = QGridLayout()

    # Scroll Area defined for the view
    self.scrollBar = QScrollArea()
    self.scrollBar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self.scrollBar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self.scrollBar.setWidgetResizable(True)

    # Adding layout to the container view, setting scrollbar on it
    # and adding the view to the base Layout of the application
    self.containerWidget.setLayout(self.containerLayout)
    self.scrollBar.setWidget(self.containerWidget)
    self.baseLayout.addWidget(self.scrollBar)

    # Communication
    # Connecting signal with appropriate handler/slot function
    self.communicate = Communicate()
    self.communicate.drawSignal.connect(self.drawView)
    self.communicate.updateStrValue[int, str, str].connect(self.updateData)
    self.communicate.updateIntValue[int, str, int].connect(self.updateData)
    self.communicate.updateBoolValue[int, str, bool].connect(self.updateData)
    self.communicate.updateSection[int, int].connect(self.updateSection)
    self.communicate.plotData[int].connect(self.handleDraw)

    self.drawView()

  def clearView(self):
    '''
    Cleaning out the widgets in the containerLayout
    Use this everytime you want to change the view of the data container
    '''
    if self.baseLayout.count() > 0:
      for item in self.containerWidget.findChildren(QWidget):
        self.containerLayout.removeWidget(item)

  def drawView(self):
    '''
    Method to draw base container view
    Kinda like a router function
    '''
    # Cleaning up baseLayout before setting new view
    self.clearView()

    # Creating view for when loaded files data has been processed by the backend
    if self.backend is not None:
      self.handleData()

  def handleLoad(self):
    '''
    Method that defines the view to be displayed while user loads a file to the application
    '''
    self.loadedFileIndicator.setText("please select a file and wait a couple of minutes for the processing to complete.")
    self.loadedFileIndicator.setVisible(True)
    self.drawView()

    currentDir = str(Path.cwd())
    # NOTE homeDir = str(Path.home())
    # TODO decide where the file dialog box should start. Now it is hard-coded to start at examples for testing ease.
    dialogBox = QFileDialog()
    fName = dialogBox.getOpenFileName(self, "select file to load", os.path.join(currentDir, "tests", "examples"))

    # NOTE since fName = ('','') in case dialog is closed via cancel.
    if fName[0] != '':
      # to display the name of the file selected by the user
      pathArr = fName[0].split('/')
      selectedFile = pathArr[len(pathArr) - 1]
      self.backend = BinaryFile(fName[0])
      self.backend.automatic()

      self.loadedFileIndicator.setText(selectedFile)
      self.loadedFileIndicator.setVisible(True)
      self.saveAction.setEnabled(True)
      self.filterAction.setChecked(False)
      self.filterAction.setVisible(True)
      self.drawView()
    else:
      self.loadedFileIndicator.setVisible(False)
      self.saveAction.setEnabled(False)
      self.filterAction.setChecked(False)
      self.drawView()

  def handleSave(self):
    '''
    Method that saves input obtained via user interaction, to a python file
    '''
    # TODO remove this when functionality is stable and application is version published
    self.backend.printList()
    self.backend.savePython()
    self.saveAction.setEnabled(False)

  def handleDraw(self, start):
    '''
    Method that plot primary data identified in the section that user would like to see plotted
    '''
    plot(self.backend, start, True)

  def handleData(self):
    '''
    Method to identify sections of processed data and create
    GUI components to display this information
    '''
    for idx, sec_start in enumerate(self.backend.content):

      props = {
        "id": idx,
        "secKey": sec_start,
        "data": self.backend.content[sec_start],
        "view": self.communicate
      }

      if sectionClass := self._DTYPE_TO_UICLASS.get(props["data"].dType):
        section = sectionClass(props).createWidget()
        sectionWidget = QGroupBox()
        sectionStyleSheet = createStyleSheet(element='groupbox', props=props['data'].dType)
        sectionWidget.setStyleSheet(sectionStyleSheet)
        sectionWidget.setLayout(section)
        sectionWidget.setVisible(False if (self.filterAction.isChecked() and self.backend.content[sec_start].dType in ('b', 'B')) else True)
        self.containerLayout.addWidget(sectionWidget)
      else:
        # sections whose dtype based ui handler component is not defined will be skipped
        # ex, currently sections of dtype == 'B' do not have a ui handler component and we skip past these sections
        continue

  def updateData(self, start, key, value):
    '''
    Method to identify and update a sections key-value with user input
    '''
    updateSection = self.backend.content[start]
    kwargs = {key: value}
    updateSection.setData(**kwargs)
    self.saveAction.setEnabled(True)

  def updateSection(self, currStart, newStart):
    '''
    Method to identify and update a sections key-value with user input
    '''
    section = self.backend.content[currStart]
    sectionData = repr(section)
    sectionData = '|'.join(sectionData.split('|')[:6])
    label(self.backend, newStart, sectionData)
    # TODO remove this when functionality is stable and application is version published
    self.backend.printList()

    self.drawView()

  # Create an option to be displayed on menu bar
  def createMenuOption(self, menu, option):
    '''
    TODO - WRITE DOCSTRING
    '''
    optionName = createVariableNames(option, 'MENU')
    optionName = menu.addMenu(f'&{option}')
    for button in MENU_TREE[option]:
      optionName.addAction(self.createMenuOptionButton(button))
    return optionName

  # Create a button for individual action button within a menu option
  def createMenuOptionButton(self, option):
    '''
    TODO - WRITE DOCSTRING
    '''
    variable = createVariableNames(option, 'BUTTON_ACTION')
    variable = QAction(option, self)
    variable.setStatusTip(option+' button status')
    variable.triggered.connect(self.handleOptionButton)
    return variable

  # Handler for button click within a particular menu option
  # TO DO : MAKE FUNCTIONAL BASED ON DIFF TYPES OF OPTION ACTIONS
  def handleOptionButton(self, s):
    '''
    TODO - WRITE DOCSTRING
    '''
    print('click', s)

def main():
  '''
  Setting up MARBLE GUI application;
  This is also the entry point to the gui app
  '''
  app = QApplication(sys.argv)
  app.setWindowIcon(QIcon(os.path.join(IMAGE_DIR_PATH,"marble_icon.png")))

  window = MainWindow()
  window.show()
  app.exec()

if __name__ == '__main__':
  main()
