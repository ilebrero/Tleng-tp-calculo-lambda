#pylint: disable=C0103,C0111,W0611
"Clases que utiliza el parser para identificar las expresiones"
from operator import is_
from lambda_lexer import global_context


def checkType(a, b):
    if type(a) == tuple:
        for i, _ in enumerate(a):
            checkType(a[i], b[i])
    elif a.type != b.type:
        err_message = "Los tipos no coinciden"
        raise TypeError(err_message)

class Expression(object):
    def evaluate(self):
        raise NotImplementedError

class Application(Expression):
    #TODO
    def __init__(self, expression1, expression2):
        exp1_type = None
        if expression1.type[0] == int:
            exp1_type = Number(0)
        elif expression1.type[0] == bool:
            exp1_type = Boolean("true")
        checkType(exp1_type, expression2)
        self.expression1 = expression1
        self.expression2 = expression2

    def	evaluate(self):
        return self.expression1.evaluate(self.expression2.evaluate())

class ConditionalOperation(Expression):

    def __init__(self, condition, left_branch, right_branch):
        checkType(left_branch, right_branch)
        checkType(condition, Boolean("true"))

        self.condition = condition
        self.left_branch = left_branch
        self.right_branch = right_branch

    def evaluate(self):
        if self.condition.evaluate():
            return self.left_branch.evaluate()
        else:
            return self.right_branch.evaluate()

class NatOperation(Expression):
    def __init__(self, val, added_val, op):
        checkType(val, added_val)
        if op == is_:
            self.type = bool
        else:
            self.type = int

        self.op = op
        self.val = val
        self.added_val = added_val

    def evaluate(self):
        val1 = self.val.evaluate()
        val2 = self.added_val.evaluate()
        evaluation = self.op(val1, val2)
        self.type = type(evaluation)
        self.value = evaluation
        return self.value

############### Atomic expressions ###############

class Boolean(Expression):
    def __init__(self, value):
        self.type = bool
        self.value = (value == "true")

    def evaluate(self):
        return self.value

class Number(Expression):
    def __init__(self, value):
        self.type = int
        self.value = int(value)

    def evaluate(self):
        return self.value

class Var(Expression):
    def __init__(self, value):
        self.value = value
        self.type = global_context[value]

    def evaluate(self):
        return global_context[self.value]

class Lambda(Expression):
    def __init__(self, variable, expression):
        self.type = (variable.type, expression.type)
        self.variable = variable.value
        self.expression = expression

    def	evaluate(self, x):
        global_context[self.variable] = x
        return self.expression.evaluate()
