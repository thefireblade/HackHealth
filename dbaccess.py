from database import Database

__all__ = ['AuthDatabase']

class AuthDatabase(Database):
	def addLog(self,userid,date,calories):
		self._execute("INSERT INTO FoodData(userId, calorieCount, transactionDate) VALUES(?,?,?);",(userid,calories,date))
	def addUser(self, userid, state):
		self._execute("INSERT INTO Users(userId, state) VALUES(?,?);",(userid, state))
	def getUserState(self, userid):
		output = self._execute("SELECT state FROM Users WHERE userid = ?",(userid,))
		if(len(output) == 0):
			return -1
		else:
			return output[0][0]
	def setUserState(self, userid, state):
		self._execute("UPDATE Users SET state = ? WHERE userid = ?", (state, userid))
	def getCalorieTarget(self, userid):
		output = self._execute("SELECT calorieTarget FROM Users WHERE userid = ?",(userid,))
		if(len(output) == 0):
			return -1
		else:
			return output[0][0]
	def setCalorieTarget(self, userid, calorieTarget):
		self._execute("UPDATE Users SET calorieTarget = ? WHERE userid = ?", (calorieTarget, userid,))
	def getCurrentWeight(self, userid):
		output = self._execute("SELECT currentWeight FROM Users WHERE userid= ?", (userid,))
		return output[0][0]
	def setCurrentWeight(self, userid, currentWeight):
		self._execute("UPDATE Users SET currentWeight = ? WHERE userid = ?", (currentWeight, userid))
	def getLastTransaction(self, userid):
		output = self._execute("SELECT lastTransaction FROM Users WHERE userid = ?", (userid,))
		return output[0][0]
	def setLastTransaction(self, userid, lastTransaction):
		self._execute("UPDATE Users SET lastTransaction = ? WHERE userid = ?", (lastTransaction, userid,))

	def getAllUsers(self):
		return self._execute("SELECT userid FROM Users")
	def deleteuser(self,userid):
		self._execute("DELETE FROM Users WHERE userid = ?",(userid,))
		self._execute("DELETE FROM FoodData WHERE userid=?",(userid,))
