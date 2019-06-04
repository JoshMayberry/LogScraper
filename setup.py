import os
import sys
import shutil

from API_Exe import exe_cx_freeze
from API_Exe import exe_innoSetup

import __version__

print("Creating Installer...")
exe = exe_cx_freeze.build("runMe.py")

exe.title = "LogScraper"
exe.author = "Joshua Mayberry"
exe.version = __version__.version
exe.author_email = "joshua.mayberry1991@gmail.com"
exe.description = "Scrapes a log file for ip addresses that had invalid login credentials"

exe.icon = "resources/scraper.ico"
exe.shortcut_name = "log_scraper.exe"
exe.destination = os.path.join(os.path.dirname(__file__), "build")

exe.optimized = True
exe.includeFile("settings.ini")
exe.includeModule("controller")
# exe.excludeZip("validator_collection")
# exe.excludeZip("jsonschema")
exe.includeFile("resources", folder = "resources")
exe.create()

installer = exe_innoSetup.build(exe)
installer.icon_installer = "resources/setup.ico"
installer.create(issFile = "installer.iss", exeName = exe.shortcut_name)
