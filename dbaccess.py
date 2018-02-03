from database import Database

__all__ = ['AuthDatabase']

class AuthDatabase(Database):
	def addLog(self,userid,date,calories):
		self._execute("INSERT INTO FoodData(userId, calorieCount, transactionDate) VALUES(?,?,?);",(userid,calories,date))
	def addUser(self, userid,name,calories):
		self._execute("INSERT INTO FoodData(userId, name, calorieTarget, currentWeight, lastTransaction) VALUES(?,?,?,?,?);",(userid, name, calories, weight, transaction))


