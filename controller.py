import os
import sys

import re
import validator_collection

import GUI_Maker
from API_Database import settingsLoader

import MyUtilities.logger
import MyUtilities.wxPython

#Setup logging
MyUtilities.logger.getLogger("API_Database.controller").quiet()
MyUtilities.logger.getLogger("MyUtilities.threadManager").quiet()

wrap_skipEvent = MyUtilities.wxPython.wrap_skipEvent

class Module_Scraper():
	def __init__(self):
		pass

	def onBeginScrape(self, event):
		addresses = set()
		with open("s20190513.log", "r", encoding = "iso-8859-15") as fileHandle:
			for line in fileHandle:
				if ("Authentication credentials invalid" in line):
					match = re.search("^(\d*\.\d*\.\d*\.\d*)", line)
					if (not match):
						print(f"Unable to find IP Address in line: {line}")
						continue

					addresses.add(match.group(1))

		print(addresses)

	def check_input(self, toggle_buttonEnable = True):
		"""Makes sure the input path is correctly formatted."""

		value = self.getSettingAppWidget("input_filepath").getValue()
		if (not value):
			self.frame_main.setStatusText("Missing Input Path")
			state = False
		elif ((not validator_collection.checkers.is_file(value)) or (not os.path.exists(value))):
			self.frame_main.setStatusText("Invalid Input Path")
			state = False
		else:
			state = True

		if (not toggle_buttonEnable):
			return state
		
		if (state):
			state = self.check_output(toggle_buttonEnable = False)
		self.setButtonEnable(state = state)

		return state

	def check_output(self, toggle_buttonEnable = True):
		"""Makes sure the output path is correctly formatted."""

		value = self.getSettingAppWidget("output_filepath").getValue()
		if (not value):
			self.frame_main.setStatusText("Missing Output Path")
			state = False
		else:
			state = True

		if (not toggle_buttonEnable):
			return state
		
		if (state):
			state = self.check_input(toggle_buttonEnable = False)
		self.setButtonEnable(state = state)

		return state

	def onCheck_input(self, event):
		"""A wxEvent version of check_input()."""
		self.check_input()
		event.Skip()

	def onCheck_output(self, event):
		"""A wxEvent version of check_output()."""
		self.check_output()
		event.Skip()

	def setButtonEnable(self, state):
		if (state):
			self.frame_main.setStatusText("Ready")

		self.button_go.setEnable(state = state)

class Module_Settings():
	def __init__(self, filePath = "settings.ini", section = "parameters"):
		self.settings = settingsLoader.build(self, filePath = filePath, section = section)
		self.settings.applyUserFunctions()

class Module_GUI():
	def __init__(self):
		self.gui = GUI_Maker.build()

	# def onViewAbout(self, event):
	# 	"""Lets the user see the information window."""

	# 	myDialog = self.frame_about.makeDialogCustom()
	# 	myDialog.show()

	# 	event.Skip()

	# def onViewTermsAndConditions(self, event):
	# 	"""Lets the user see the terms and conditions window."""

	# 	self.frame_html.setWindowTitle(f"Terms and Conditions v.{__version__.version}")

	# 	myDialog = self.frame_html.makeDialogCustom()
	# 	with open("resources/_termsAndConditions.html", "r") as fileHandle:
	# 		self.widget_html.setValue(fileHandle.read())
	# 	myDialog.show()

	# 	event.Skip()

	def buildGUI(self):
		"""The GUI build routine.

		Example Input: buildGUI()
		"""

		self.log_info("Building GUI")
		self.makeWindows()
		self.buildMain()

	def makeWindows(self):
		self.frame_main = self.gui.addWindow(label = "main")

	def buildMain(self):
		with self.frame_main as myFrame:
			# myFrame.setWindowSize((400, 200))
			myFrame.addStatusBar()

			with myFrame.addMenu(text = "&File") as myMenu:
				with myMenu.addItem(text = "&Exit") as myMenuItem:
					myMenuItem.addToolTip("Closes the software")
					myMenuItem.setFunction_click(myFunction = myFrame.onExit)
				
				myMenu.addSeparator()
				
				# with myMenu.addItem(text = "View &Change Log", label = "menu_changeLog") as myMenuItem:
				#   myMenuItem.addToolTip("View recently made changes")
				#   myMenuItem.setFunction_click(myFunction = html_viewer.onShow, myFunctionKwargs = {"mode": "changeLog"})
				
				if (myFrame != self.frame_main):
					with myMenu.addItem(text = "Main Menu") as myMenuItem:
						myMenuItem.addToolTip("Returns to the main menu")
						myMenuItem.setFunction_click(myFunction = myFrame.onSwitchWindow, myFunctionArgs = self.frame_main)

			with myFrame.addMenu(text = "&Help") as myMenu:
				with myMenu.addItem(text = "&About", enabled = False) as myMenuItem:
					myMenuItem.addToolTip("What this software is")

				myMenu.addSeparator()

				with myMenu.addItem(text = "Terms of Use", enabled = False) as myMenuItem:
					myMenuItem.addToolTip("The terms of use document")

			with myFrame.addSizerGridFlex(rows = 2, columns = 1) as mainSizer:
				mainSizer.growFlexColumnAll()

				with mainSizer.addSizerGridFlex(rows = 2, columns = 2) as contentSizer:
					contentSizer.growFlexColumn(1)

				with mainSizer.addSizerGridFlex(rows = 1, columns = 1) as mySizer:
					with mySizer.addButton("Go!") as myWidget:
						self.button_go = myWidget
						myWidget.setFunction_click(self.onBeginScrape)
						myWidget.addToolTip("Begin searching the file")

				with contentSizer:
					contentSizer.addText("Input:")
					with contentSizer.addPickerFile(text = "The file(s) to search", label = "input_filepath", openFile = True, fileMustExist = True, addInputBox = True) as myWidget:
						self.addSettingWidget("input_filepath", myWidget, checkFunction = self.check_input, toggleWidget = self.button_go)
						# myWidget.setFunction_click(self.onCheck_input)
						myWidget.setFunction_click(myFunction = self.onChangeSetting, myFunctionKwargs = {"myWidget": myWidget, "check": True})
						myWidget.addToolTip("What file(s) to search through")

					contentSizer.addText("Output:")
					with contentSizer.addPickerFile(text = "Select where to save output...", label = "output_filepath", saveFile = True, saveConfirmation = True, addInputBox = True) as myWidget:
						self.addSettingWidget("output_filepath", myWidget, checkFunction = self.check_output, toggleWidget = self.button_go)
						# myWidget.setFunction_click(self.onCheck_output)
						myWidget.setFunction_click(myFunction = self.onChangeSetting, myFunctionKwargs = {"myWidget": myWidget, "check": True})
						myWidget.addToolTip("Where the file should be saved")

class Controller(MyUtilities.logger.LoggingFunctions, Module_Settings, Module_GUI, Module_Scraper):
	logger_config = {
		None: {
			"level": 1,
		},

		"console": {
			"type": "stream",
			"level": 1,
		},
	}

	def __init__(self, logger_name = None, logger_config = None):
		MyUtilities.logger.LoggingFunctions.__init__(self, label = logger_name or __name__, config = logger_config or self.logger_config, force_quietRoot = __name__ == "__main__")
		Module_Settings.__init__(self)
		Module_GUI.__init__(self)
		Module_Scraper.__init__(self)


	def begin(self):
		self.buildGUI()

		self.log_info("GUI Finished")
		self.settings.setBuilding(False)
		self.check_input()
		self.frame_main.showWindow()
		self.frame_main.updateWindow(updateNested = True)
		self.gui.finish()

if (__name__ == "__main__"):
	controller = Controller()
	controller.begin()
