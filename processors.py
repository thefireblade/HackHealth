
class Processors:

	def __init__(self):
		pass

	def echo(self,textIn):
		return "You said: " + textIn

	def storeData(self, textIn):
		if(textIn == "Log"):
			addLog()
