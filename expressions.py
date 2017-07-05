#pylint: disable=C0103,C0111,W0611
"Clases que utiliza el parser para identificar las expresiones"
from operator import is_, add
from lambda_lexer import global_context

def get_type_str(t):
    if t == bool:
        return "Bool"
    elif t == int:
        return "Nat"
    else:
        # Es una tupla
        a = b = None
        if isinstance(t[0], tuple):
            a = "(%s)" %(get_type_str(t[0]))
        else: 
            a = get_type_str(t[0])
        if isinstance(t[1], tuple):
            b = "(%s)" %(get_type_str(t[1]))
        else: 
            b = get_type_str(t[1])
        return "%s->%s"%(a, b)

def checkType(a, b, err):
    if isinstance(a, tuple):
        for i, _ in enumerate(a):
            checkType(a[i], b[i], err)
    elif a.type != b.type:
        raise TypeError(err)

class Expression(object):
    def evaluate(self):
        raise NotImplementedError

class Application(Expression):
    def __init__(self, expression1, expression2):
        exp1_type = None
        try:
            if expression1.type[0] == int:
                exp1_type = Number(0)
            elif expression1.type[0] == bool:
                exp1_type = Boolean("true")
        except TypeError:
            raise TypeError("La parte izquierda de la aplicación (%s) no es una función con dominio %s" 
                %(str(expression1), get_type_str(expression2.type)))
        checkType(exp1_type, expression2, 
            "La función lambda espera un parametro de tipo %s. Recibio %s" 
            %(get_type_str(exp1_type.type), get_type_str(expression2.type)))
        self.expression1 = expression1
        self.expression2 = expression2
        self.type = expression1.type[1]

    def	evaluate(self):
        return self.expression1.evaluate(self.expression2.evaluate())

    def __str__(self):
        return str(self.expression1) + " " + str(self.expression2)

class ConditionalOperation(Expression):
    def __init__(self, condition, left_branch, right_branch):
        checkType(left_branch, right_branch, "Las dos opciones del if deben tener el mismo tipo")
        checkType(condition, Boolean("true"), "La condición debe ser booleana")

        self.condition = condition
        self.left_branch = left_branch
        self.right_branch = right_branch
        self.type = left_branch.type

    def evaluate(self):
        if self.condition.evaluate():
            return self.left_branch.evaluate()
        else:
            return self.right_branch.evaluate()

    def __str__(self):
        return "if " + str(self.condition) + " then " + \
             str(self.left_branch) + " else " + str(self.right_branch)

class NatOperation(Expression):
    def __init__(self, val, added_val, op):
        if op == is_:
            self.type = bool
        else:
            self.type = int

        self.op = op
        self.val = val
        self.added_val = added_val

        self.op_str = None
        if op == is_:
            self.op_str = "iszero"
        elif op == add and self.added_val.value > 0:
            self.op_str = "succ"
        else:
            self.op_str = "pred"

        checkType(val, added_val, self.op_str + " espera un valor de tipo Nat")

    def evaluate(self):
        val1 = self.val.evaluate()
        val2 = self.added_val.evaluate()
        evaluation = self.op(val1[0], val2[0])
        self.type = type(evaluation)
        self.value = evaluation
        return (self.value, self.type)

    def __str__(self):
        return self.op_str + "(" + str(self.val) + ")"

############### Atomic expressions ###############

class Boolean(Expression):
    def __init__(self, value):
        self.type = bool
        self.value = (value == "true")

    def evaluate(self):
        return (self.value, self.type)

    def __str__(self):
        if self.value:
            return "true"
        else:
            return "false"

class Number(Expression):
    def __init__(self, value):
        self.type = int
        self.value = int(value)

    def evaluate(self):
        return (self.value, self.type)

    def __str__(self):
        return str(self.value)

class Var(Expression):
    def __init__(self, value):
        self.value = value
        self.type = global_context[value]

    def evaluate(self):
        return (global_context[self.value], self.type)

    def __str__(self):
        return self.value

class Lambda(Expression):
    def __init__(self, variable, expression):
        #if isinstance(variable.type, tuple):
        #    l = list(variable.type)
        #    if l[0] == "Nat": l[0] = int
        #    else: l[0] = bool
        #    if l[1] == "Nat": l[1] = int
        #    else: l[1] = bool
        #    self.type = (tuple(l), expression.type)
        #else:
        self.type = (variable.type, expression.type)
        self.variable = variable.value
        self.expression = expression        

    def	evaluate(self, x=None):
        if x:
            global_context[self.variable] = x
            return self.expression.evaluate()
        else:
            return (str(self), self.type)

    def __str__(self):
        return "\\" + self.variable + ":" + get_type_str(self.type[0]) + \
            "." + str(self.expression)
