from database import Database

__all__ = ['AuthDatabase']

class AuthDatabase(Database):
	def addLog(self,userid,date,calories):
		self._execute("INSERT INTO FoodData(userId,calorieCount,transactionDate) VALUES(?,?,?);",(userid,date,calories))


