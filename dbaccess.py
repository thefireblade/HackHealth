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
		else 
			return output[0]
	def 



