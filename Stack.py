from Class import Class

class Stack:
    def __init__(self , globalVariables):
        self.stack = []
        self.globalVariables = []
        for var in globalVariables:
            self.globalVariables.append(Var(var['id'],var['type']))

    def getVar(self, name):
        # Searching in Local Scope of function
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].name == name:
                return self.stack[i]
        # Searching in Class Properties ( if the function is defined in Class )
        this = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].name == "this":
                this = self.stack[i]
                break
        if this != None:
            c = Class.searchClass(this.type)
            if c is None:
                raise Exception("Class with name " + this.type + " not exists !")
            if c.variableExists(name):
                var = c.getVariable(name)
                return Var(var['name'] , var['type'])
        # Searching in Global Scope
        for i in range(len(self.globalVariables)-1,-1,-1):
            if self.globalVariables[i].name == name:
                return self.globalVariables[i]
        raise Exception("No such variable name : " + name)

    def getAddress(self , name):
        # Searching in Local Scope of function
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].name == name:
                code = "addi $s7 , $fp , " + str((len(self.stack) - i - 1) * 4) + "\n"
                return code
        # Searching in Class Properties ( if the function is defined in Class )
        this = None
        offsetThis = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].name == "this":
                this = self.stack[i]
                offsetThis = len(self.stack) - i - 1
                break
        if this != None:
            c = Class.searchClass(this.type)
            if c is None:
                raise Exception("Class with name " + this.type + " not exists !")
            if c.variableExists(name):
                offset = c.variableOffset(name)
                code = "# Loading Class Variable : " + name + "\n"
                code += "addi $s7 , $fp , " + str(offsetThis * 4) + "\n"
                code += "lw $s7 , 0($s7)\n"
                code += "addi $s7 , $s7 , " + str(offset) + " # add offset of " + name + " from base object pointer\n"
                return code
        # Searching in Global Scope
        for i in range(len(self.globalVariables)-1,-1,-1):
            if self.globalVariables[i].name == name:
                code = "# Loading Global Variable : " + name + "\n"
                code += "la $s7 , data_" + name + "\n"
                return code
        raise Exception("No such variable name : " + name)

    def push(self , var):
        self.stack.append(var)

    def pop(self , size):
        for i in range(size):
            self.stack.pop()

    def log(self):
        pprint.pprint("---------------------")
        for var in self.stack:
            pprint.pprint(var.name + " - " + var.type)

class Var:
    def __init__(self, name, var_type):
        self.name = name
        self.type = var_type