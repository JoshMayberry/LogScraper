import os
import sys

def main():
	"""The first function that should run."""

	preventClose = True
	try:
		import controller
		controller.main()

	except SystemExit:
		preventClose = False
		raise

	except:
		import traceback
		
		#Display what happened
		traceback.print_exc()

		# if (restart(cmdArgs)):
		# 	preventClose = False
		# 	# os.execl(sys.executable, sys.executable, *sys.argv)

	finally:
		import time

		#Keep the cmd window from closing
		if (preventClose):
			while True:
				time.sleep(1)

if (__name__ == "__main__"):
	main()