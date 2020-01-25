from data.game_data import constants

class MsgLog:

	# TODO: Add event - after 5 seconds of no new messages - pop them all.
	
	def __init__(self):
		self.messages = [] # list of Message's instances.
	
	def clear(self):
		self.messages = []

	def add_msg(self, msg):

		if len(self.messages) > constants.MESSAGES_ON_SCREEN - 1:
			self.messages.pop(0)

		self.messages.append(msg)
