from lark import Transformer
from Class import Class

class Cg(Transformer):
    def __init__(self):
        self.Functions = [
            {'name' : 'itod' , 'type' : 'double'},
            {'name' : 'dtoi' , 'type' : 'int'},
            {'name' : 'itob' , 'type' : 'bool'},
            {'name' : 'btoi' , 'type' : 'int'}
        ]
        self.Global_Variables = []

        self.structure = []

    def get_functions(self):
        return self.Functions
    def get_global_vars(self):
        return self.Global_Variables
    def get_structure(self):
        return self.structure
    ############# Class Variables and Functions #############
    def class_decl(self , args):
        id = args[0].children[0]
        extends = args[1]
        fields = args[3]
        cls = Class(id,extends)
        variables = fields['variables']
        functions = fields['functions']
        for var in variables:
            cls.addVariable(var['id'] , var['type'])
        for f in functions:
            cls.addMethod(f['name'] , f['type'])
        self.structure.append({'type' : 'class' , 'name' : id})
    ### Extends ###
    def extends_optional(self , args):
        return args[0].children[0]
    def extends_optional_empty(self , args):
        return None
    ### Class Fields ###
    def fields(self , args):
        if 'function' in args[0]:
            args[1]['functions'].insert(0,args[0]['function'])
        elif 'variable' in args[0]:
            args[1]['variables'].insert(0,args[0]['variable'])
        else:
            raise Exception("Unknown Field Type in Class !!!")
        return args[1]
    def fields_empty(self , args):
        return {'functions' : [] , 'variables' : []}
    def field_variable(self , args):
        return {'variable' : args[0]}
    def field_function(self , args):
        return {'function' : args[0]}

    ############# Global Variables #############
    def decl_variable_decl(self, args):
        self.Global_Variables.append(args[0])
    def variable_decl(self , args):
        return args[0]
    def variable(self, args):
        id = args[1].children[0]
        type = args[0]
        return {'id' : id , 'type' : type}

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
    def type_id(self , args):
        return args[0].children[0]
    ############# Function #############
    def decl_function_decl(self , args):
        function = args[0]
        self.Functions.append({'name' : function['name'] , 'type' : function['type']})
        self.structure.append({'type' : 'funtion' , 'name' : function['name']})
    def function_decl(self , args):
        type = args[0]
        id = args[1].children[0]
        return {'name' : id , 'type' : type}
    def function_decl_void(self , args):
        type = 'void'
        id = args[0].children[0]
        return {'name': id, 'type': type}