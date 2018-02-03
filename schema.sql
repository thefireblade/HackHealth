CREATE TABLE Users(
   userId INTEGER PRIMARY KEY,
   calorieTarget INTEGER,
   currentWeight INTEGER,
   lastTransaction VARCHAR(19),
   state INTEGER
  );

CREATE TABLE FoodData(
	userId INTEGER,
	calorieCount INTEGER,
	transactionDate VARCHAR(19)

);