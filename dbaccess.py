from database import Database

__all__ = ['AuthDatabase']

class AuthDatabase(Database):
	def addLog(self,userid,date,calories):
		self._execute("INSERT INTO FoodData(userId, calorieCount, transactionDate) VALUES(?,?,?);",(userid,calories,date))
	def addUser(self, userid, state):
		self._execute("INSERT INTO Users(userId, state) VALUES(?,?);",(userid, state))
	def getUserState(self, userid):
		output = self._execute("SELECT state FROM Users WHERE userid = ?",(userid,))
	def setUserState(self, state):
		self._execute("UPDATE Users SET userId = self WHERE state = 1)
	def getCalorieTarget(self, calorieTarget):
		if(len(output) == 0):
			return -1
		else:
			return output[0][0]
	def setCalorieTarget(self, state):
		self._execute("UPDATE Users SET calorieTarget = self WHERE state = 2")
	def getCurrentWeight(self, userId):
		output = self._execute("SELECT currentWeight FROM Users WHERE userid= ?", (currentWeight,))
		return output[0][0]
	def setCurrentWeight(self, state):
		self._execute("UPDATE Users SET currentWeight = self WHERE state = 3")
	def getLastTransaction(self, lastTransaction):
		output = self._execute("SELECT lastTransaction FROM Users WHERE lastTransaction = ?", (lastTransaction,))
		return output[0][0]
	def setLastTransaction(self, state):
		self._execute("UPDATE Users SET lastTransaction = self WHERE state = 4")
