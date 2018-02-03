import flask
import json
from datetime import datetime
from flask import Flask, request, Response
from interface import Interface
from processors import Processors


app = Flask(__name__)
interface = Interface()
processor = Processors()

db = interface.database
with open("config.json") as config_file:
	config = json.load(config_file)

@app.route('/', methods=['GET', 'POST'])
def index():
	if "hub.challenge" in request.args:
		response = str(request.args["hub.challenge"])
		return response
	data = None

	if request:
		print request.data
		print request.form
		if request.data:
			data = json.loads(request.data)
		elif request.form:
			data = request.form

		if "X-Hub-Signature" in request.headers:
			for entry in data["entry"]:
				for message in entry["messaging"]:
					msgtext = sender = None

					if "sender" in message and "id" in message["sender"]:
						sender = message["sender"]["id"]

					if "message" in message and "text" in message["message"]:
						msgtext = message["message"]["text"]

				if msgtext and sender:
					print "Received " + msgtext + " from " + sender
					if(msgtext == "show me the way"):
						interface.messageFB("The total calorie count for today is : " + str(calculateTotalCalorie(sender)) +  " calories", sender)
						interface.messageFB("You are " + str(round(calculateTotalCalorie(sender)/db.getCalorieTarget(sender)* 100, 2)) + "%" +
						 " to your calorie target", sender )
					else:

						state = db.getUserState(sender)
						if(state == -1):
							db.addUser(sender, 1)
							interface.messageFB("Hi, what is your weight?", sender)
						elif state == 1:
							interface.messageFB("What is your calorie target everyday?", sender)
							db.setUserState(sender, 2)
							db.setCurrentWeight(sender, msgtext)

						elif state == 2:
							db.setUserState(sender, 3)
							db.setCalorieTarget(sender, msgtext)
							interface.messageFB("The data is imported!", sender)
						elif state == 3:
							db.setUserState(sender, 4)
							interface.messageFB("Hi, welcome back. Enter the calorie count for your meal:", sender)
						else:
							db.setUserState(sender, 3)
							db.addLog(sender, datetime.now().date().strftime('%m%d%Y'),msgtext)
							db.setLastTransaction(sender, datetime.now().time().strftime('%H:%M:%S'))
							interface.messageFB("Food data was logged successfully! See you again next time.", sender)
				elif sender:
					interface.messageFB("(y)",sender)
		elif "source" in data:
			ifttthandler()


	return ""

def ifttthandler():
	interface.broadcast("I got ifttt data!")

def calculateTotalCalorie(sender):
	output = interface.database._execute("SELECT calorieCount FROM FoodData WHERE transactionDate = ?",(datetime.now().date().strftime('%m%d%Y'),))
	return sum([row[0] for row in output])


def main():
	app.debug = True
	app.run(host='0.0.0.0', port=config["server_port"])

def printer(instr):
	print instr

if __name__ == '__main__':
	main()
