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

					if((msgtext.replace(" ","").lower() == "showmetheway") or (msgtext.replace(" ","").lower() == "doyouknowdewey")):
						total(sender)
					elif msgtext.replace(" ","").lower() == "deleteme":
						interface.messageFB("You have been deleted. RIP", sender)
						db.deleteuser(sender)
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
							interface.messageFB("Got it! Message me when you eat a meal. I'll check in with you every night and help you track your progress", sender)
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
		else:
			ifttthandler()


	return ""

def ifttthandler():

	users = interface.database.getAllUsers()
	for user in users:
		interface.messageFB("Time for your nightly checkin",user[0])
		total(user[0])


def total(sender):
	calories = calculateTotalCalorie(sender)
	target = db.getCalorieTarget(sender)
	interface.messageFB("The total calorie count for today is : " + str(calories) +  " calories", sender)
	interface.messageFB("You ate " + str(round(calories*1.0/target* 100, 2)) + "%" +
	 " of your calorie target", sender )
	net = calories - target
	diff = "gained" if net > 0 else "loss"
	net = net * -1 if net < 0 else net
	interface.messageFB("You " + diff + " a net of " + str(net) + " calories today. That's " + str(round(net/3500.0,2)) + " pounds", sender)

def calculateTotalCalorie(sender):
	output = interface.database._execute("SELECT calorieCount FROM FoodData WHERE transactionDate = ? AND userid = ?",(datetime.now().date().strftime('%m%d%Y'), sender))
	return sum([row[0] for row in output])


def main():
	app.debug = True
	app.run(host='0.0.0.0', port=config["server_port"])

def printer(instr):
	print instr

if __name__ == '__main__':
	main()
