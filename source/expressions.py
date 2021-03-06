#pylint: disable=C0103,C0111,W0611
"Clases que utiliza el parser para identificar las expresiones"
from operator import is_, add
from lambda_lexer import global_context

def get_type_str(t):
    if hasattr(t, "type"):
        t = t.type
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

def get_input_type_of_function(t):
    if t[0] == int:
        return Number(0)
    elif t[0] == bool:
        return Boolean("true")
    elif isinstance(t[0], tuple):
        return Function(t[0])

def checkType(a, b, err):
    if isinstance(a, Function):
        for i, _ in enumerate(a.type):
            checkType(a.type[i], b.type[i], err)
    else:
        try:
            if a.type != b.type:
                raise TypeError(err)
        except AttributeError:
            if a != b:
                raise TypeError(err)

class Expression(object):
    def evaluate(self):
        raise NotImplementedError

class Brackets(Expression):
    def __init__(self, exp):
        self.exp = exp
        self.type = self.exp.type

    def evaluate(self):
        return self.exp.evaluate()

    def __str__(self):
        return "(" + str(self.exp) + ")"

class Application(Expression):
    def __init__(self, expression1, expression2):
        exp1_type = None
        try:
            exp1_type = get_input_type_of_function(expression1.type)
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
        self.expression1 = self.expression1.evaluate()
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
        evaluation = self.op(val1, val2)
        self.type = type(evaluation)
        self.value = evaluation
        return self.value

    def __str__(self):
        return self.op_str + "(" + str(self.val) + ")"

############### Atomic expressions ###############

class Boolean(Expression):
    def __init__(self, value):
        self.type = bool
        self.value = (value == "true")

    def evaluate(self):
        return self.value

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
        return self.value

    def __str__(self):
        return str(self.value)

class Function(Expression):
    def __init__(self, tuple):
        self.type = tuple

class Var(Expression):
    def __init__(self, value):
        self.value = value
        self.type = global_context[value]

    def evaluate(self):
        return global_context[self.value]

    def __str__(self):
        return self.value

class Lambda(Expression):
    def __init__(self, variable, expression):
        self.type = (variable.type, expression.type)
        self.variable = variable.value
        self.expression = expression

    def	evaluate(self, x=None):
        if x:
            global_context[self.variable] = x
            return self.expression.evaluate()
        else:
            return self

    def __str__(self):
        return "\\" + self.variable + ":" + get_type_str(self.type[0]) + \
            "." + str(self.expression)
