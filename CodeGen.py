import os
from lark import Transformer
import pprint
import re


class Stack:
    def __init__(self):
        self.stack = []

    def getIndex(self, name):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].name == name:
                return len(self.stack) - i - 1
        raise Exception("No such variable name : " + name)

    def getVar(self, name):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].name == name:
                return self.stack[i]
        raise Exception("No such variable name : " + name)

    def getAddress(self , name):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].name == name:
                code = "addi $s7, $fp, " + str((len(self.stack) - i - 1) * 4) + "\n"
                return code
        raise Exception("No such variable name : " + name)

    def push(self , var):
        self.stack.append(var)

    def pop(self , size):
        for i in range(size):
            self.stack.pop()

class Var:
    def __init__(self, name, var_type):
        self.name = name
        self.type = var_type


class CodeGen(Transformer):
    def __init__(self,functions):
        self.label_num = 0
        self.data_name_num = 0
        self.break_num = 0
        self.data_code = ''
        self.Stack = Stack()
        self.Functions = functions

    def function_type(self , name):
        for function in self.Functions:
            if function['name'] == name:
                return function['type']
        raise Exception("function ( " + name + " ) not found !!!")

    def in_break_labels(self , arr , name):
        for item in arr:
            if item['name'] == name:
                return True
        return False

    def get_count_break_label(self , arr , name):
        for item in arr:
            if item['name'] == name:
                return item['count']
        raise Exception("no label found for " + name)
    ################################################### Assets ###################################################
    def label_generator(self):
        newLabel = "L" + str(self.label_num)
        self.label_num = self.label_num + 1
        return newLabel
    def data_name_generator(self):
        new_name = 'D' + str(self.data_name_num)
        self.data_name_num += 1
        return new_name
    def break_generator(self):
        new_break = 'break' + str(self.break_num)
        self.break_num += 1;
        return new_break
    #[--------------------------------------------------------- Debugging tools ---------------------------------------------------------]
    def log_code(self,code):
        dirname = os.path.dirname(__file__)
        file = open(dirname + "/code.txt","w")
        file.write(code)
        file.close()
    #[--------------------------------------------------------- Semantic Actions ---------------------------------------------------------]
    ############# Program #############
    def start(self, args):
        dirname = os.path.dirname(__file__)
        file = open(dirname + "/Compiler_Functions.txt", "r")
        default_functions = file.read()
        file.close()
        code = '.text\n'
        code += '.globl main\n'
        code += default_functions
        code += args[0]['code']
        self.data_code += "str_false : .asciiz \"false\" \n"
        self.data_code += "str_true : .asciiz \"true\" \n"
        self.data_code += "str_bool : .word str_false , str_true\n"
        self.log_code(code + "\n\n.data\n" + self.data_code)
        return args
    def program(self, args):
        decl = args[0]
        decl_more = args[1]
        code = decl['code'] + decl_more['code']
        return {'code': code}
    def decl_more(self, args):
        decl = args[0]
        decl_more = args[1]
        code = decl['code'] + decl_more['code']
        return {'code' : code}
    def decl_more_empty(self, args):
        return {'code' : ''}
    ######################################################### Variable Declaration #########################################################
    def variable(self, args):
        id = args[1].children[0]
        type = args[0]
        return {'id' : id , 'type' : type}
    def variable_decl(self, args):
        return args[0]
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
        return args[0]
    ############### Variables of Block Statement ###############
    def variable_decls_empty(self, args):
        return {'variable_count' : 0}
    def variable_decls(self, args):
        var_type = args[1]['type']
        var_id = args[1]['id']
        self.Stack.push(Var(var_id,var_type))
        return {'variable_count': args[0]['variable_count'] + 1}
    ######################################################### Expressions #########################################################
    ############### Expr More ###############
    def expr_more(self , args):
        expr = args[0]
        expr_more = args[1]
        return {'code' : expr['code'] + expr_more['code'] , 'variable_count' : expr_more['variable_count'] + 1}
    def expr_more_empty(self , args):
        return {'code' : '' , 'variable_count' : 0}
    ############### Expr Optional ###############
    def stmt_expr_optional(self, args):
        code = args[0]['code']
        if code != '':
            code += "# End of Expression Optional\n"
            code += "addi $sp , $sp 4\n"
            return {'code' : code , 'break_labels' : []}
        return {'code' : '', 'break_labels' : []}
    def expr_optional(self, args):
        return args[0]
    def expr_optional_empty(self, args):
        return {'code': ''}
    def expr(self, args):
        return args[0]
    ############### Assign ###############
    def expr_assign(self, args):
        if args[0]['value_type'] != args[1]['value_type']:
            raise Exception("Types of Right Hand Side of Assign is not the same as Left Side")
        value_type = args[0]['value_type']
        code = args[0]['code'] + args[1]['code']
        code += "# Assign Expression\n"
        code += "lw $t0 , 8($sp)\n"
        if value_type == 'int' or value_type == 'bool' or value_type == 'string':
            code += "lw $t1 , 4($sp)\n"
            code += "sw $t1 , 0($t0)\n"
            code += "sw $t1 , 8($sp)\n"
        else:
            code += "l.s $f0 , 4($sp)\n"
            code += "s.s $f0 , 0($t0)\n"
            code += "s.s $f0 , 8($sp)\n"
        code += "addi $sp , $sp , 4\n"
        return {'code' : code,
                'value_type' : value_type}
    def expr_assign_pass(self, args):
        return args[0]
    ############### Or ###############
    def expr_or(self, args):
        value_type = args[0]['value_type']
        code = "# Or Expression\n"
        if value_type != 'bool':
            raise Exception("Unhandled Type for Or !")
        code += "lw $t0 , 8($sp)\n"
        code += "lw $t1 , 4($sp)\n"
        code += "or $t0 , $t0 , $t1\n"
        code += "sw $t0 , 8($sp)\n"
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'bool'}
    def expr_or_pass(self, args):
        return args[0]
    ############### And ###############
    def expr_and(self, args):
        value_type = args[0]['value_type']
        code = "# And Expression\n"
        if value_type != 'bool':
            raise Exception("Unhandled Type for And !")
        code += "lw $t0 , 8($sp)\n"
        code += "lw $t1 , 4($sp)\n"
        code += "and $t0 , $t0 , $t1\n"
        code += "sw $t0 , 8($sp)\n"
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'bool'}
    def expr_and_pass(self, args):
        return args[0]
    ############### Equal ###############
    def expr_equality_equal(self, args):
        value_type = args[0]['value_type']
        code = "# Equal Expression\n"
        if value_type == 'int' or value_type == 'bool':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "seq $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            labelLower = self.label_generator()
            labelEnd = self.label_generator()
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "c.eq.s $f0 , $f1\n"
            code += "bc1t " + labelLower + " # if first and second are equal\n"
            code += "li $t0 , 0\n"
            code += "j " + labelEnd + " # Jump to Storing This NE Result to Stack\n"
            code += labelLower + ":\n"
            code += "li $t0 , 1\n"
            code += labelEnd + ":\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'string':
            code += "lw $a0 , 8($sp)\n"
            code += "lw $a1 , 4($sp)\n"
            code += "addi $sp , $sp , -8\n"
            code += "sw $fp , 8($sp)\n"
            code += "sw $ra , 4($sp)\n"
            code += "jal StringsEquality # Calling Function to Check Equality of two Strings\n"
            code += "lw $fp , 8($sp)\n"
            code += "lw $ra , 4($sp)\n"
            code += "addi $sp , $sp , 8\n"
            code += "sw $v0 , 8($sp) # Saving Result of Equality of two Strings\n"
        else:
            raise Exception("Unhandled Type for E !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'bool'}
    ############### Not Equal ###############
    def expr_equality_not_equal(self, args):
        value_type = args[0]['value_type']
        code = "# Not Equal Expression\n"
        if value_type == 'int' or value_type == 'bool':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "seq $t0 , $t0 , $t1\n"
            code += "nor $t0 , $t0 , $t0\n"
            code += 'addi $t0 , $t0 , 2\n'
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            labelLower = self.label_generator()
            labelEnd = self.label_generator()
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "c.eq.s $f0 , $f1\n"
            code += "bc1t " + labelLower + " # if first and second are equal\n"
            code += "li $t0 , 1\n"
            code += "j " + labelEnd + " # Jump to Storing This NE Result to Stack\n"
            code += labelLower + ":\n"
            code += "li $t0 , 0\n"
            code += labelEnd + ":\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'string':
            code += "lw $a0 , 8($sp)\n"
            code += "lw $a1 , 4($sp)\n"
            code += "addi $sp , $sp , -8\n"
            code += "sw $fp , 8($sp)\n"
            code += "sw $ra , 4($sp)\n"
            code += "jal StringsInequality # Calling Function to Check inEquality of two Strings\n"
            code += "lw $fp , 8($sp)\n"
            code += "lw $ra , 4($sp)\n"
            code += "addi $sp , $sp , 8\n"
            code += "sw $v0 , 8($sp) # Saving Result of inEquality of two Strings\n"
        else:
            raise Exception("Unhandled Type for NE !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'bool'}
    def expr_equality_pass(self, args):
        return args[0]
    ############### Less ###############
    def expr_compare_l(self, args):
        value_type = args[0]['value_type']
        code = "# Less Expression\n"
        if value_type == 'int':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "slt $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            labelLower = self.label_generator()
            labelEnd = self.label_generator()
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "c.lt.s $f0 , $f1\n"
            code += "bc1t " + labelLower + " # if first is less than second\n"
            code += "li $t0 , 0\n"
            code += "j " + labelEnd + " # Jump to Storing This L Result to Stack\n"
            code += labelLower + ":\n"
            code += "li $t0 , 1\n"
            code += labelEnd + ":\n"
            code += "sw $t0 , 8($sp)\n"
        else:
            raise Exception("Unhandled Type for E !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'bool'}
    ############### Less or Equal ###############
    def expr_compare_le(self, args):
        value_type = args[0]['value_type']
        code = "# Less or Equal Expression\n"
        if value_type == 'int':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "sle $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            labelLower = self.label_generator()
            labelEnd = self.label_generator()
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "c.le.s $f0 , $f1\n"
            code += "bc1t " + labelLower + " # if first is less ( or equal ) than second\n"
            code += "li $t0 , 0\n"
            code += "j " + labelEnd + " # Jump to Storing This LE Result to Stack\n"
            code += labelLower + ":\n"
            code += "li $t0 , 1\n"
            code += labelEnd + ":\n"
            code += "sw $t0 , 8($sp)\n"
        else:
            raise Exception("Unhandled Type for LE !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'bool'}
    ############### Greater ###############
    def expr_compare_g(self, args):
        value_type = args[0]['value_type']
        code = "# Greater Expression\n"
        if value_type == 'int':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "sgt $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            labelLower = self.label_generator()
            labelEnd = self.label_generator()
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "c.le.s $f0 , $f1\n"
            code += "bc1t " + labelLower + " # if first is less ( or equal ) than second\n"
            code += "li $t0 , 1\n"
            code += "j " + labelEnd + " # Jump to Storing This G Result to Stack\n"
            code += labelLower + ":\n"
            code += "li $t0 , 0\n"
            code += labelEnd + ":\n"
            code += "sw $t0 , 8($sp)\n"
        else:
            raise Exception("Unhandled Type for G !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'bool'}
    ############### Greater or Equal ###############
    def expr_compare_ge(self, args):
        value_type = args[0]['value_type']
        code = "# Greater or Equal Expression\n"
        if value_type == 'int':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "sge $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            labelLower = self.label_generator()
            labelEnd = self.label_generator()
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "c.lt.s $f0 , $f1\n"
            code += "bc1t " + labelLower + " # if first is less than second\n"
            code += "li $t0 , 1\n"
            code += "j " + labelEnd + " # Jump to Storing This GE Result to Stack\n"
            code += labelLower + ":\n"
            code += "li $t0 , 0\n"
            code += labelEnd + ":\n"
            code += "sw $t0 , 8($sp)\n"
        else:
            raise Exception("Unhandled Type for GE !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'bool'}
    def expr_compare_pass(self, args):
        return args[0]
    ############### Addition ###############
    def expr_add_sub_plus(self, args):
        value_type = args[0]['value_type']
        code = "# Add Expression\n"
        if value_type == 'int':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "add $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "add.s $f0 , $f0 , $f1\n"
            code += "s.s $f0 , 8($sp)\n"
        else:
            raise Exception("Unhandled Type for Add !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': value_type}
    ############### Subtraction ###############
    def expr_add_sub_minus(self, args):
        value_type = args[0]['value_type']
        code = "# Sub Expression\n"
        if value_type == 'int':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "sub $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "sub.s $f0 , $f0 , $f1\n"
            code += "s.s $f0 , 8($sp)\n"
        else:
            raise Exception("Unhandled Type for Sub !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': value_type}
    def expr_add_sub_pass(self, args):
        return args[0]
    ############### Multiplication ###############
    def expr_mul_div_mul(self, args):
        value_type = args[0]['value_type']
        code = "# Mul Expression\n"
        if value_type == 'int':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "mul $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "mul.s $f0 , $f0 , $f1\n"
            code += "s.s $f0 , 8($sp)\n"
        else:
            raise Exception("Unhandled Type for Mul !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': value_type}
    ############### Division ###############
    def expr_mul_div_div(self, args):
        value_type = args[0]['value_type']
        code = "# Div Expression\n"
        if value_type == 'int':
            code += "lw $t0 , 8($sp)\n"
            code += "lw $t1 , 4($sp)\n"
            code += "div $t0 , $t0 , $t1\n"
            code += "sw $t0 , 8($sp)\n"
        elif value_type == 'double':
            code += "l.s $f0 , 8($sp)\n"
            code += "l.s $f1 , 4($sp)\n"
            code += "div.s $f0 , $f0 , $f1\n"
            code += "s.s $f0 , 8($sp)\n"
        else:
            raise Exception("Unhandled Type for Div !")
        code += "addi $sp , $sp , 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': value_type}
    ############### Mod ###############
    def expr_mul_div_mod(self, args):
        if args[0]['value_type'] != 'int':
            raise Exception("Unhandled Type for Mod !")
        code = "# mod Expression\n"
        code += "lw $t0 , 8($sp)\n"
        code += "lw $t1 , 4($sp)\n"
        code += "rem $t0 , $t0 , $t1\n"
        code += "sw $t0, 8($sp)\n"
        code += "addi $sp, $sp, 4\n"
        return {'code': args[0]['code'] + args[1]['code'] + code,
                'value_type': 'int'}
    def expr_mul_div_mod_pass(self, args):
        return args[0]
    ############### Not ###############
    def expr_not_negative_not(self, args):
        if args[0]['value_type'] != 'bool':
            raise Exception("Unhandled Type for Not !")
        code = args[0]['code']
        code += "lw $t0, 4($sp)\n"
        code += "xori $t0, $t0, 1\n"
        code += "sw $t0, 4($sp)\n"
        return {'code': code,
                'value_type': 'bool'}
    ############### Negative ###############
    def expr_not_negative_negative(self, args):
        value_type = args[0]['value_type']
        code = args[0]['code']
        if value_type == 'double':
            code += "l.s $f0 , 4($sp)\n"
            code += "neg.s $f0 , $f0\n"
            code += "s.s $f0 , 4($sp)\n"
        elif value_type == 'int':
            code += "lw $t0 , 4($sp)\n"
            code += "neg $t0 , $t0\n"
            code += "sw $t0 , 4($sp)\n"
        else:
            raise Exception("Unhandled Type for Negative !")
        return {'code': code,
                'value_type': value_type}
    def expr_not_negative_pass(self , args):
        return args[0]
    ############### Parentheses ###############
    def expr_par(self, args):
        return args[0]
    def expr_par_pass(self, args):
        return args[0]
    ######################################################### Atomic Expressions #########################################################
    ############### Left Value ###############
    def expr_atomic_left_value(self, args):
        code = "# Load Value from Address of ID : " + args[0]['name'] + "\n"
        code += "lw $t0, 4($sp)\n"
        code += "lw $t0 , 0($t0)\n"
        code += "sw $t0 , 4($sp) # Value of " + args[0]['name'] + " Pushed to Stack\n"
        args[0]['code'] += code
        return args[0]
    ############### NewArray ###############
    def expr_atomic_new_array(self, args):
        code = "# NewArray of Type : " + args[1] + "\n"
        code += "lw $t0, 4($sp)\n"
        code += "li $t1, 4\n"
        code += "mul $a0, $t0, $t1\n"
        code += "li $v0, 9\n"
        code += "syscall\n"
        code += "sw $v0, 4($sp)\n"
        return {'code': args[0]['code'] + code,
                'value_type': args[1]}
    ############### Read Integer ###############
    def expr_atomic_read_integer(self, args):
        code = "# Read Integer : \n"
        code += "li $v0 , 5\n"
        code += "syscall\n"
        code += "addi $sp , $sp , -4\n"
        code += "sw $v0 , 4($sp)\n"
        return {'code': code, 'value_type': 'int'}
    ############### Read Line ###############
    def expr_atomic_read_line(self, args):
        code = "# Read Line : \n"
        code += "addi $sp , $sp , -8\n"
        code += "sw $fp , 8($sp)\n"
        code += "sw $ra , 4($sp)\n"
        code += "jal ReadLine # Calling Read Line Function \n"
        code += "lw $fp , 8($sp)\n"
        code += "lw $ra , 4($sp)\n"
        code += "addi $sp , $sp , 4\n"
        code += "sw $v0 , 4($sp)# Saving String Address ( Saved in Heap ) in Stack\n"
        return {'code': code, 'value_type': 'string'}
    ############### Print ###############
    def stmt_print_stmt(self, args):
        args[0]['break_labels'] = []
        return args[0]
    def print_stmt(self, args):
        expr = args[0]
        expr_type = expr['value_type']
        code = expr['code']
        code += "# Print : \n"
        code += "addi $sp , $sp , 4 # Pop Expression of Print\n"
        if expr_type == "string":
            code += "lw $a0 , 0($sp)\n"
            code += "li $v0 , 4\n"
        elif expr_type == "double":
            code += "l.s $f12 , 0($sp)\n"
            code += "li $v0 , 2\n"
        elif expr_type == "bool":
            code += "lw $a0 , 0($sp)\n"
            code += "la $t0 , str_bool\n"
            code += "sll $a0 , $a0 , 2\n"
            code += "add $a0 , $a0 , $t0\n"
            code += "lw $a0 , 0($a0)\n"
            code += "li $v0 , 4\n"
        else:
            code += "lw $a0 , 0($sp)\n"
            code += "li $v0 , 1\n"
        code += "syscall\n"
        code += "li $a0 , '\\n'\n"
        code += "li $v0 , 11\n"
        code += "syscall\n"
        return {'code': code}
    ############### Call ###############
    def expr_atomic_call(self , args):
        return args[0]
    ######################################################### Left Value #########################################################
    ############### Left Value ID ###############
    def left_value_id(self, args):
        name = args[0].children[0].value
        index = self.Stack.getIndex(name)
        value_type = self.Stack.getVar(name).type
        code = "# Loading Address of ID : " + name + "\n"
        code += self.Stack.getAddress(name)
        code += 'sw $s7, 0($sp)' + ' # Push Address of ' + name + ' to Stack\n'
        code += 'addi $sp, $sp, -4\n'
        return {'code': code,
                'name': name,
                'value_type': value_type}
    ######################################################### Constants #########################################################
    def expr_atomic_constant(self , args):
        return args[0]
    ############### Integer Constant ###############
    def constant_int(self , args):
        code = "# Int Constant : " + str(args[0].value) + "\n"
        code += "li $t0 , " + str(args[0].value) + "\n"
        code += 'sw $t0 , 0($sp)\n'
        code += 'addi $sp, $sp, -4\n'
        return {'code': code,
                'value_type': 'int'}
    ############### Double Constant ###############
    def constant_double(self, args):
        code = "# Double Constant : " + str(args[0].value) + "\n"
        code += "li.s $f0, " + str(args[0].value) + "\n"
        code += "s.s $f0, 0($sp)\n"
        code += "addi $sp, $sp, -4\n"
        return {'code': code,
                'value_type': 'double'}
    ############### Bool Constant ###############
    def constant_bool(self, args):
        code = "# Bool Constant : " + str(args[0].value) + "\n"
        if str(args[0].value) == 'true':
            code += 'li $t0 , 1\n'
        elif str(args[0].value) == 'false':
            code += 'li $t0, 0\n'
        code += 'sw $t0 , 0($sp)\n'
        code += 'addi $sp, $sp, -4\n'
        return {'code': code,
                'value_type': 'bool'}
    ############### String Constant ###############
    def constant_string(self, args):
        name = self.data_name_generator()
        code = "# String Constant : " + args[0].value + "\n"
        code += 'la $t0, ' + name + '\n'
        code += 'sw $t0, 0($sp)\n'
        code += 'addi $sp, $sp, -4\n'
        self.data_code += name + ': .asciiz ' + args[0].value + '\n'
        return {'code': code,
                'value_type': 'string'}
    ######################################################### Statement #########################################################
    ############### Statement Block ###############
    def stmt_block(self , args):
        variable_decls = args[0]
        stmts = args[1]
        code = "# Begin of Statement Block\n"
        code += "addi $sp , $sp , -" + str(variable_decls['variable_count'] * 4) + " # Allocate From Stack For Block Statement Variables\n"
        code += "addi $fp , $sp , 4\n"
        code += stmts['code']
        code += "addi $sp , $sp , " + str( variable_decls['variable_count'] * 4) + " # UnAllocate Stack Area (Removing Block Statement Variables)\n"
        code += "addi $fp ,$sp , 4\n"
        code += "# End of Statement Block\n"
        self.Stack.pop(variable_decls['variable_count'])

        # Handling breaks ...
        break_labels = stmts['break_labels']
        pattern = re.compile(r'@(break\d+)@')
        for break_label in re.findall(pattern, code):
            if not self.in_break_labels(break_labels, break_label):
                break_labels.append({'name' : break_label , 'count' : 0})
        for item in break_labels:
            item['count'] += variable_decls['variable_count']

        return {'code' : code , 'break_labels' : break_labels}
    def stmts(self, args):
        code = args[0]['code'] + args[1]['code']
        break_labels = args[0]['break_labels'] + args[1]['break_labels']
        return {'code': code , 'break_labels': break_labels}
    def stmts_empty(self, args):
        return {'code': '' , 'break_labels' : []}
    def stmt_stmt_block(self, args):
        return args[0]
    ############### if Statement ###############
    def stmt_if_stmt(self , args):
        return args[0]
    def if_stmt_ms(self , args):
        return args[0]
    def if_stmt_us(self , args):
        return args[0]
    def ms(self , args):
        expr = args[0]
        stmt1 = args[1]
        stmt2 = args[2]
        elseLabel = self.label_generator()
        endLabel = self.label_generator()
        code = "# Calculating IF Condition\n"
        code += expr['code']
        code += "# Loading IF Condition Result\n"
        code += "addi $sp , $sp , 4\n"
        code += "lw $t0 , 0($sp)\n"
        code += "beqz $t0 , " + elseLabel + " # Jumping to else label if expression is false\n"
        code += "# IF Statement Body\n"
        code += stmt1['code']
        code += "j " + endLabel + " # Jump to end of if_stmt\n"
        code += "# Else Statement Body\n"
        code += elseLabel + ":\n"
        code += stmt2['code']
        code += endLabel + ":\n"
        return {'code' : code , 'break_labels' : stmt1['break_labels'] + stmt2['break_labels']}
    def us(self , args):
        expr = args[0]
        stmt = args[1]
        endLabel = self.label_generator()
        code = "# Calculating IF Condition\n"
        code += expr['code']
        code += "# Loading IF Condition\n"
        code += "addi $sp , $sp , 4\n"
        code += "lw $t0 , 0($sp)\n"
        code += "beqz $t0 , " + endLabel + " # Jumping to end label if expression is false\n"
        code += "# IF Statement Body\n"
        code += stmt['code']
        code += endLabel + ":\n"
        return {'code' : code , 'break_labels' : stmt['break_labels']}
    ############### while loop ###############
    def stmt_while_stmt(self , args):
        return args[0]
    def while_stmt(self , args):
        expr = args[0]
        stmt = args[1]
        startLabel = self.label_generator()
        endLabel = self.label_generator()

        # Handling breaks ...
        break_labels = stmt['break_labels']
        pattern = re.compile(r'@(break\d+)@')
        for break_label in re.findall(pattern, stmt['code']):
            count = self.get_count_break_label(break_labels , break_label)
            code_for_break = "addi $sp , $sp , " + str(count * 4) + " # Pop elements before\n"
            code_for_break += "j " + endLabel + " # Break from loop while\n"
            stmt['code'] = stmt['code'].replace("@" + break_label + "@" , code_for_break)

        code = startLabel + ": # Starting While Loop Body\n"
        code += "# Calculating While Condition\n"
        code += expr['code']
        code += "# Loading While Condition Result\n"
        code += "addi $sp , $sp , 4\n"
        code += "lw $t0 , 0($sp)\n"
        code += "beqz $t0 , " + endLabel + " # Jumping to end label if expression is false\n"
        code += stmt['code']
        code += "j " + startLabel + " # Jumping to beggining of while loop\n"
        code += endLabel + ":\n"
        return {'code' : code , 'break_labels' : []}
    ############### for loop ###############
    def stmt_for_stmt(self , args):
        return args[0]
    def for_stmt(self , args):
        expr_initialization = args[0]
        expr_condition = args[1]
        expr_step = args[2]
        stmt = args[3]
        startLabel = self.label_generator()
        endLabel = self.label_generator()

        # Handling breaks ...
        break_labels = stmt['break_labels']
        pattern = re.compile(r'@(break\d+)@')
        for break_label in re.findall(pattern, stmt['code']):
            count = self.get_count_break_label(break_labels, break_label)
            code_for_break = "addi $sp , $sp , " + str(count * 4) + " # Pop elements before\n"
            code_for_break += "j " + endLabel + " # Break from loop for\n"
            stmt['code'] = stmt['code'].replace("@" + break_label + "@", code_for_break)

        code = "# Initialization Expression of Loop for\n"
        code += expr_initialization['code']
        if expr_initialization['code'] != '':
            code += "addi $sp , $sp , 4 # pop init expr of loop for\n"
        code += startLabel + ": # Starting for Loop Body\n"
        code += "# Calculating For Loop Condition\n"
        code += expr_condition['code']
        code += "# Loading For Loop Condition Result\n"
        code += "addi $sp , $sp , 4\n"
        code += "lw $t0 , 0($sp)\n"
        code += "beqz $t0 , " + endLabel + " # Jumping to end label if Condition Expression of for loop is false\n"
        code += stmt['code']
        code += "# Step Expression of For loop \n"
        code += expr_step['code']
        if expr_step['code'] != '':
            code += "addi $sp , $sp , 4 # pop step expr of loop for\n"
        code += "j " + startLabel + " # Jumping to beggining of while loop\n"
        code += endLabel + ":\n"
        return {'code' : code , 'break_labels' : []}
    ############### Break ###############
    def stmt_break_stmt(self , args):
        args[0]['break_labels'] = []
        return args[0]
    def break_stmt(self , args):
        code = "@" + self.break_generator() + "@\n"
        return {'code' : code}
    ######################################################### Function #########################################################
    ############### Formals and Variables ###############
    def formals(self , args):
        variable = args[0]
        more_variables = args[1]
        variables = [{'id' : variable['id'] , 'type' : variable['type']}] + more_variables['variables']
        for var in variables:
            self.Stack.push(Var(var['id'], var['type']))
        pass
    def formals_empty(self , args):
        pass
    def more_variables(self , args):
        variable = args[0]
        variable_obj = [ {'type' : variable['type'], 'id' : variable['id']} ]
        more_variables = args[1]
        return {'variables' : variable_obj + more_variables['variables']}
    def more_variables_empty(self , args):
        return {'variables' : []}
    ############### Function Declaration ###############
    def decl_function_decl(self , args):
        return args[0]
    def function_decl(self , args):
        returnType = args[0]
        functionName = args[1].children[0]
        formals = args[2]
        stmt_block = args[3]
        label_end = functionName + "_end"
        stmt_block['code'] = stmt_block['code'].replace("@return@","j " + label_end + " # Jump to end function ( return )\n")
        code = functionName + ": # Start function\n"
        code += "addi $s5 , $sp , 0 # Storing $sp of function at beginning in $s5\n"
        code += "# Function Body :\n"
        code += stmt_block['code']
        code += label_end + " :\n"
        code += "jr $ra\n"
        return {'code' : code}
    def function_decl_void(self , args):
        functionName = args[0]
        formals = args[1]
        stmt_block = args[2]
        label_end = functionName + "_end :\n"
        stmt_block['code'] = stmt_block['code'].replace("@return@","j " + label_end + " # Jump to end function\n")
        code = functionName + ": # Start function body\n"
        code += "addi $s5 , $sp , 0 # Storing $sp of function at beginning in $s5\n"
        code += "addi $fp , $sp , 0 # Set Frame Pointer of function\n"
        code += "# Function Body :\n"
        code += stmt_block['code']
        code += label_end
        code += "jr $ra\n"
        return {'code': code}
    ############### return ###############
    def stmt_return_stmt(self, args):
        args[0]['break_labels'] = []
        return args[0]
    def return_stmt(self, args):
        exprOptional = args[0]
        code = ''
        if exprOptional['code'] != '':
            code = exprOptional['code']
            if exprOptional['value_type'] == 'double':
                code += 'l.s $f0 , 4($sp) # Loading Return Value of function\n'
            else:
                code += 'lw $v0 , 4($sp) # Loading Return Value of function\n'
            code += "addi $sp , $sp , 4\n"
            code += "move $sp , $s5\n"
            code += "jr $ra # Return Function\n"
        return {'code' : code}
    ############### Function Call ###############
    def call(self , args):
        id = args[0].children[0]
        value_type = self.function_type(id)
        actuals = args[1]
        code = "# Storing Frame Pointer and Return Address Before Calling the function : " + id + "\n"
        code += "addi $sp , $sp , -12\n"
        code += "sw $fp , 4($sp)\n"
        code += "sw $ra , 8($sp)\n"
        code += "sw $s5 , 12($sp)\n"
        code += "# Function Arguments\n"
        code += actuals['code']
        code += "jal " + id + " # Calling Function\n"
        code += "# Pop Arguments of function\n"
        code += "addi $sp , $sp , " + str(actuals['variable_count']*4) + "\n"
        code += "# Load Back Frame Pointer and Return Address After Function call\n"
        code += "lw $fp , 4($sp)\n"
        code += "lw $ra , 8($sp)\n"
        code += "lw $s5 , 12($sp)\n"
        code += "addi $sp , $sp , 8\n"
        if value_type == 'double':
            code += "s.s $f0 , 4($sp) # Push Return Value from function to Stack\n"
        else:
            code += "sw $v0 , 4($sp) # Push Return Value from function to Stack\n"
        return {'code': code , 'value_type' : value_type}
    def actuals(self , args):
        expr = args[0]
        expr_more = args[1]
        return {'variable_count' : expr_more['variable_count'] + 1 , 'code' : expr['code'] + expr_more['code'] }
    def actuals_empty(self , args):
        return {'variable_count': 0, 'code': ''}
    ######################################################### Class #########################################################
    ############### Class Extends ###############
    def extends_optional(self , args):
        id = args[0].children[0]
        return {'extends' : id}
    def extends_optional_empty(self , args):
        return {'extends' : None}
    ############### Class Declaration ###############
    def class_decl(self , args):
        id = args[0]
        extends_optional = args[1]
        implements_optional = args[2]
        fields = args[3]