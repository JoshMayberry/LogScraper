import os
username = os.getenv('username')
print (os.getenv('LOCALAPPDATA'))
print (os.path.join(os.getenv('LOCALAPPDATA'), "LogScraper", username))