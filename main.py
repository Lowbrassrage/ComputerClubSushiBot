import Queue
import datetime

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

ingredients = []

class Ingredient:
	def __init__(self,amount):
		self.amount = amount
		self.lastRestockTimestamp = datetime.datetime.utcfromtimestamp(0) #datetime.datetime.now()

orderTemplates = [ [ 1, 1, 2], [1, 2, 3], [1, 2, 3, 3] ]

def ingredientsForOrder(orderID):
	return orderTemplates[orderID]

def handleOrder(orderInfo):
	print "Handling order"
	orderIngredients = ingredientsForOrder(orderInfo[1])
	for ingredient in orderIngredients:
		useIngredient(ingredient)

def handleRestock(ingredientID):
	print "Handling restock"

def handleClearPlates():
	print "Handling clear plates"


# go click on ingredient to add to order
# update amount of ingredient we have
def addIngredientToOrder(ingredientID):
	# mouse clicks

	ingredients[ingredientID].amount = ingredients[ingredientID].amount - 1

def restockIngredient(ingredientID):
	print "restock ingredient"
	ingredients[ingredientID].amount = ingredients[ingredientID].amount + ingredientRestockAmount[ingredientID]

# and restock ingredient if necessary
def useIngredient(ingredientID):
	addIngredientToOrder(ingredientID)
	if ingredients[ingredientID].amount < 5:
		timeDelta = datetime.datetime.now() - ingredients[ingredientID].lastRestockTimestamp
		if timeDelta.total_seconds() > 10:
			restockIngredient(ingredientID)




# initialize ingredients tracking
ingredients = [ Ingredient(5), Ingredient(10), Ingredient(10), Ingredient(10), Ingredient(5), Ingredient(5) ]
ingredientRestockAmount = [ 3, 10, 10, 10, 3, 3]


# TEMP
actionsQ.put(Action(ORDER_PRIORITY,ORDER,(1,0)))
actionsQ.put(Action(ORDER_PRIORITY,ORDER,(1,0)))
actionsQ.put(Action(ORDER_PRIORITY,ORDER,(1,0)))
actionsQ.put(Action(ORDER_PRIORITY,ORDER,(2,2)))
actionsQ.put(Action(ORDER_PRIORITY,ORDER,(2,2)))
# actionsQ.put(Action(RESTOCK_PRIORITY,RESTOCK,5))


lastPlateClearedTimestamp = datetime.datetime.now()

# run loop
while True:
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







