from lark import Transformer

class Cg(Transformer):
    def __init__(self):
        self.Functions = []

    def get_functions(self):
        return self.Functions
    ############# Types #############
    def type_int(self, args):
        return "int"
    def type_double(self, args):
        return "double"
    def type_bool(self, args):
        return "bool"
    def type_string(self, args):
        return "string"
    def type_array(self, args):
        return args[0] + "[]"

    ############# Function #############
    def decl_function_decl(self , args):
        function = args[0]
        self.Functions.append({'name' : function['name'] , 'type' : function['type']})
    def function_decl(self , args):
        type = args[0]
        id = args[1].children[0]
        return {'name' : id , 'type' : type}
    def function_decl_void(self , args):
        type = 'void'
        id = args[0].children[0]
        return {'name': id, 'type': type}