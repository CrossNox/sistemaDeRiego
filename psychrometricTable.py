import math

class psychrometricTable:

	@staticmethod
	def getHR(dryBulbTemp, wetBulbTemp):
		#A Method to Measure Humidity Based on Dry-Bulb and Wet-Bulb Temperatures
		#Yongping Huang, Ke Zhang, Shufan Yang and Yushan Jin
		ew = 6.112*(math.e**((17.502*wetBulbTemp)/(240.97+wetBulbTemp)))
		ed = 6.112*(math.e**((17.502*dryBulbTemp)/(240.97+dryBulbTemp)))
		A = 0.00066*(1.0+0.0015*wetBulbTemp)
		P = 1013.25024
		dT = dryBulbTemp-wetBulbTemp
		return ((ew - A*P*dT)*100.0)/ed