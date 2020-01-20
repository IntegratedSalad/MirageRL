import constants

class MsgLog:
	
	def __init__(self):
		self.messages = [] # list of Message's instances.
	
	def clear(self):
		self.messages = []

	def add_msg(self, msg):

		if len(self.messages) > constants.MESSAGES_ON_SCREEN:
			self.messages.pop()

		self.messages.append(msg)
