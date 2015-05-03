#!/usr/bin/python

import Queue
import datetime

import pyautogui

baseX = 20
baseY = 240
mouseSpeed = 0.25

def clearPlates( ):
	for i in range(0, 6):
		pyautogui.moveTo(baseX + 80 + (100 * i), baseY + 210, 0)
		pyautogui.click()

def finishOrder( ):
	pyautogui.moveTo(baseX + 200, baseY + 380, mouseSpeed)
	pyautogui.click()

def buyIngredient( ID ):
	pyautogui.moveTo(baseX + 555, baseY + 360, mouseSpeed)
	pyautogui.click()

	if ID == 1:
		pyautogui.moveTo(baseX + 497, baseY + 290, mouseSpeed)
		pyautogui.click()

		pyautogui.moveTo(baseX + 542, baseY + 279, mouseSpeed)
		pyautogui.click()

	else:
		pyautogui.moveTo(baseX + 494, baseY + 269, mouseSpeed)
		pyautogui.click()

		if (ID == 0) or (ID == 2) or (ID == 4):
			newX = baseX + 490
		else:
			newX = baseX + 570

		if (ID == 0) or (ID == 5):
			newY = baseY + 220
		elif (ID == 2) or (ID == 3):
			newY = baseY + 277
		else:
			newY = baseY + 330

		pyautogui.moveTo(newX, newY, mouseSpeed)
		pyautogui.click()

	pyautogui.moveTo(baseX + 490, baseY + 293, mouseSpeed)
	pyautogui.click()

def addIngredient( ID ):
	if (ID == 0) or (ID == 2) or (ID == 4):
		newX = baseX + 35
	else:
		newX = baseX + 90

	if (ID == 0) or (ID == 1):
		newY = baseY + 330
	elif (ID == 2) or (ID == 3):
		newY = baseY + 385
	else:
		newY = baseY + 430

	pyautogui.moveTo(newX, newY, mouseSpeed)
	pyautogui.click()

def skipIntro( ):

	#play
	pyautogui.moveTo(baseX + 310, baseY + 205, mouseSpeed)
	pyautogui.click()

	#continue 1
	pyautogui.moveTo(baseX + 312, baseY + 387, mouseSpeed)
	pyautogui.click()

	#continue 2
	pyautogui.moveTo(baseX + 312, baseY + 387, mouseSpeed)
	pyautogui.click()

	#skip
	pyautogui.moveTo(baseX + 578, baseY + 447, mouseSpeed)
	pyautogui.click()

	#continue 3
	pyautogui.moveTo(baseX + 312, baseY + 387, mouseSpeed)
	pyautogui.click()


CLEAR_PLATES = "clearPlates"
RESTOCK = "restock"
ORDER = "order"

ORDER_PRIORITY = 10
PLATES_PRIORITY = 5
RESTOCK_PRIORITY = 1

actionsQ = Queue.PriorityQueue()

class Action:
	def __init__(self,priority,actionType,value):
		self.priority = priority
		self.actionType = actionType
		self.value = value

	def __cmp__(self,other):
		return cmp(self.priority,other.priority)

class Ingredient:
	def __init__(self,amount):
		self.amount = amount
		self.lastRestockTimestamp = datetime.datetime.utcfromtimestamp(0) #datetime.datetime.now()



orderTemplates = [ [ 1, 1, 2], [1, 2, 3], [1, 2, 3, 3] ]
orderImageHashes = [ 5996548660431658855, -2598077304484467701, -8722492923913262121 ]

def handleOrder(orderID):
	print "Handling order %d" % orderID
	orderIngredients = orderTemplates[orderID]
	
	notEnough = False
	for ingredientID in orderIngredients:
		if ingredients[ingredientID].amount <= 5:
			notEnough = True
			timeDelta = datetime.datetime.now() - ingredients[ingredientID].lastRestockTimestamp
			if timeDelta.total_seconds() > 10:
				restockIngredient(ingredientID)

	if notEnough:
		actionsQ.put(Action(ORDER_PRIORITY,ORDER,orderID))
		return

	for ingredientID in orderIngredients:
		useIngredient(ingredientID)

	finishOrder()

def handleRestock(ingredientID):
	timeDelta = datetime.datetime.now() - programStartTime
	if timeDelta.total_seconds() < 40:
		actionsQ.put(Action(RESTOCK_PRIORITY,RESTOCK,ingredientID))
		return

	print "Restocking ingredient %d" % ingredientID

	buyIngredient(ingredientID)

	ingredients[ingredientID].amount = ingredients[ingredientID].amount + ingredientRestockAmount[ingredientID]
	ingredients[ingredientID].lastRestockTimestamp = datetime.datetime.now()

def handleClearPlates():
	print "Clearing Plates"
	clearPlates()

# go click on ingredient to add to order
# update amount of ingredient we have
def addIngredientToOrder(ingredientID):
	# mouse clicks
	addIngredient(ingredientID)
	ingredients[ingredientID].amount = ingredients[ingredientID].amount - 1

def restockIngredient(ingredientID):
	print "Restock request added for ingredient %d" % ingredientID
	actionsQ.put(Action(RESTOCK_PRIORITY,RESTOCK,ingredientID))
	ingredients[ingredientID].lastRestockTimestamp = datetime.datetime.now()

# and restock ingredient if necessary
def useIngredient(ingredientID):
	addIngredientToOrder(ingredientID)


# initialize ingredients tracking
ingredients = [ Ingredient(5), Ingredient(10), Ingredient(10), Ingredient(10), Ingredient(5), Ingredient(5) ]
ingredientRestockAmount = [ 3, 10, 10, 10, 3, 3]


def orderForImageHash(img,index):
	imgHash = hash(img.tobytes())
	# print "%d:  %d" % (index, imgHash)

	idx = 0
	for imageHash in orderImageHashes:
		if imageHash == imgHash:
			return idx
		idx = idx + 1

	return -1

# TEMP
# actionsQ.put(Action(ORDER_PRIORITY,ORDER,1))
# actionsQ.put(Action(ORDER_PRIORITY,ORDER,1))
# actionsQ.put(Action(ORDER_PRIORITY,ORDER,0))
# actionsQ.put(Action(ORDER_PRIORITY,ORDER,2))
# actionsQ.put(Action(ORDER_PRIORITY,ORDER,2))
# actionsQ.put(Action(RESTOCK_PRIORITY,RESTOCK,5))


lastPlateClearedTimestamp = datetime.datetime.now()


pyautogui.moveTo(baseX + 310, baseY + 205)
pyautogui.click()

skipIntro()

# 58 + baseX (101 * i), 50 + baseY, 40, 35
orderRegions = [ (baseX + 38, baseY + 50, 40, 35), (baseX + 139, baseY + 50, 40, 35), (baseX + 240, baseY + 50, 40, 35), (baseX + 341, baseY + 50, 40, 35), (baseX + 442, baseY + 50, 40, 35), (baseX + 543, baseY + 50, 40, 35) ]
currentCustomers = [ -1, -1, -1, -1, -1, -1 ]

programStartTime = datetime.datetime.now()

# run loop
while True:
	# orderID = input("Order ID: ")
	# actionsQ.put(Action(ORDER_PRIORITY,ORDER,orderID))

	# pyautogui.moveTo(baseX + 310, baseY + 205)
	# pyautogui.click()

	# check for customer orders
	index = 0
	for region in orderRegions:
		# print region
		img = pyautogui.screenshot(region=region)
		orderID = orderForImageHash(img,index)

		if orderID != currentCustomers[index]:
			currentCustomers[index] = orderID
			if orderID != -1:
				actionsQ.put(Action(ORDER_PRIORITY,ORDER,orderID))
		index = index + 1


	if (datetime.datetime.now() - lastPlateClearedTimestamp).total_seconds() > 20:
		actionsQ.put(Action(PLATES_PRIORITY,CLEAR_PLATES,0))
		lastPlateClearedTimestamp = datetime.datetime.now()

	if not actionsQ.empty():
		action = actionsQ.get()
		if action.actionType == ORDER:
			handleOrder(action.value)
		elif action.actionType == RESTOCK:
			handleRestock(action.value)
		elif action.actionType == CLEAR_PLATES:
			handleClearPlates()
		else:
			print "Unknown Action was pulled off ActionsQ"







