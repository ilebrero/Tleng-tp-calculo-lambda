#Cuando armemos los objetos de T se van a saber evaluar por compatibles
def checkType(a, b):
	if a.type != b.type:
		err_message = "No matchean los tipos | agregar algun error de otro tipo para esto?"
		raise NotImplementedError(err_message)

class Expression(object):

	def evaluate(self):
		raise NotImplementedError

class Lambda(Expression):

	def __init_(self, variable, typeVal, expression):
		#TODO: ver que tipos hay que matchear aca
		self.type = typeVal
		self.variable   = variable
		self.expression = expression

	def	evaluate(self):
		#TODO: completar lo que deberia hacer
		return expression.evaluate()

class BinaryExpression(Expression):

	def __init_(self, expression1, expression2):
		#checkType(expression1, expression2)
		self.expression1 = expression1
		self.expression2 = expression2

	def	evaluate(self):
		exp1_eval = self.expression1.evaluate()
		exp2_eval = self.expression2.evaluate()
		#TODO: completar lo que deberia hacer
		return expression1.evaluate()

class ConditionalOperation(Expression):

	def __init__(self, condition, left_branch, rigth_branch):
		checkType(left_branch, rigth_branch)
		checkType(condition, Boolean("true"))

		self.condition = condition
		self.left_branch  = left_branch
		self.rigth_branch = rigth_branch

	def evaluate(self):
		condition_evaluation = self.condition.evaluate()

		if condition_evaluation == "true":
			return self.left_branch.evaluate()
		else:
			return self.rigth_branch.evaluate()

class BinaryNumericOperation(Expression):
	def __init__(self, val, added_val, op):
		checkType(val, added_val)

		self.op   = op
		self.val  = val
		self.type = "int"
		self.added_val = added_val

	def evaluate(self):
		val_eval = self.val.evaluate()
		added_val_eval = self.added_val.evaluate()

		#Hardcodeado?
		if (val_eval <= 0 and added_val_eval == -1):
			return val_eval
		else:
			return self.op(val_eval, added_val_eval)

############### Atomic expressions ###############

class Boolean(Expression):
	def __init__(self, value):
		self.type  = "bool"
		self.value = value

	def evaluate(self):
		return self.value

class Number(Expression):

	def __init__(self, value):
		self.type  = "int"
		self.value = value

	def evaluate(self):
		return self.value

class Var(Expression):

	def __init__(self, value):
		self.value = value

	def evaluate(self):
		return self.value

