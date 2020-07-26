from pprint import pprint
import re

class Class:
    classes = []

    def __init__(self, name, parentName=None):
        self.name = name
        self.variables = []
        self.methods = []
        if parentName is not None:
            parent = Class.searchClass(parentName)
            self.extendVariables(parent)
            self.extendMethods(parent)
        Class.classes.append(self)

    # Inherit Variables an Methods from parent
    def extendVariables(self, parent):
        for var in parent.variables:
            self.variables.append(var.copy())

    def extendMethods(self, parent):
        for method in parent.methods:
            self.methods.append(method.copy())

    # Find Offset of Variables and Methods from Start Address
    def offsetVariable(self, name):
        for i in range(len(self.variables)):
            if self.variables[i]['name'] == name:
                return i * 4
        raise Exception("Variable ( " + name + " ) not found !!!")

    def offsetMethods(self, name):
        for i in range(len(self.methods)):
            if self.methods[i]['name'] == name:
                return i * 4
        raise Exception("Method ( " + name + " ) fot found !!!")

    # Check Where a Variable or a Method Exists or not ( Search by name )
    def variableExists(self, name):
        for var in self.variables:
            if var['name'] == name:
                return True
        return False

    def methodExists(self, name):
        for method in self.methods:
            if method['name'] == name:
                return True
        return False

    # Add Variable or Method
    def addVariable(self, name, varType):
        self.variables.append({'name': name, 'type': varType})

    def addMethod(self, name, methodType):
        if self.methodExists(name):
            self.overrideMethod(name)
        else:
            self.methods.append({'name': name, 'type': methodType, 'prefix': self.name})

    def overrideMethod(self, name):
        for method in self.methods:
            if method['name'] == name:
                method['prefix'] = self.name
                return
        raise Exception("Method ( " + name + " ) not found to override !!!")

    # Find & Replace Variables of Object
    def findAndReplace(self , code):
        pattern = re.compile(r'(@(\w+)\|(\d+)@)')
        for m in re.finditer(pattern, code):
            if self.variableExists(m.group(2)):
                offset = self.offsetVariable(m.group(2))
                objOffset = m.group(3)
                getVarCode = "lw $s7 , " + objOffset + "($fp)\n"
                getVarCode += "addi $s7 , $s7 , " + str(offset)
                code = code.replace(m.group(1),getVarCode)
            else:
                raise Exception("Handling Global Variables Here ...")
        return code


    # Search Class By Name
    @staticmethod
    def searchClass(searchKey):
        for c in Class.classes:
            if c.name == searchKey:
                return c
        return None

# A = Class("A")
# A.addMethod("M1" , "T1")
# A.addMethod("M2" , "T2")
# A.addMethod("M3" , "T3")
# A.addVariable("V1" , "T11")
# A.addVariable("V2" , "T22")
# A.addVariable("V3" , "T33")
# A.addVariable("V4" , "T44")
# code = "asdasdas\n@V1|24@\nasdasdads\nasdasdads\naasdasd\n@V2|240@\nasdasd\n@V3|12@\n"
# print(code)
# print("-----------------------------------------------")
# code = A.findAndReplace(code)
# print(code)
# B = Class("B" , "A")
# B.addMethod("M4" , "T4")
# B.addMethod("M2","T2")
# C = Class("C" , "B")
# C.addMethod("M1" , "T1")
# C.addVariable("V3" , "T33")
# pprint(vars(C))