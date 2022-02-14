import signal
from contextlib import contextmanager

###########################################################
# Signal Handling
###########################################################
class Signal:
	SIGINT = signal.SIGINT
	SIGTERM = signal.SIGTERM

	def __init__(self):
		self.__caught = dict()

	def install(self, siglist):
		for signum in siglist:
			self.__caught[signum] = False
			signal.signal(signum, self.__handler)

	def __handler(self, signum, frame):
		self.__caught[signum] = True

	def caught(self, signum=None):
		if signum:
			if signum in self.__caught:
				return self.__caught[signum]
			else:
				return False

		for signum in self.__caught.keys():
			if self.__caught[signum]:
				return True

		return False


class TimeoutException(Exception):
	pass

@contextmanager
def time_limit(seconds):
	def signal_handler(signum, frame):
		raise TimeoutException

	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)

###########################################################
# Interruptible loop
###########################################################
def for_each_item_int(item_list):

	# register signal handler
	signal = Signal()
	signal.install([Signal.SIGINT, Signal.SIGTERM])

	# work with each item
	for idx, item in enumerate(item_list):
		# check for interruption
		if signal.caught():
			break
		yield idx, item

