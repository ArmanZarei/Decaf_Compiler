from lark import Lark , Transformer
from CodeGen import CodeGen

grammar = """
start: program

program: decl decl_more -> program
decl_more: decl decl_more -> decl_more
    | -> decl_more_empty

decl: variable_decl
    | function_decl -> decl_function_decl
    | class_decl
    | interface_decl

variable_decl: variable ";" -> variable_decl

variable: type id -> variable

type: "int" -> type_int
    | "double" -> type_double
    | "bool" -> type_bool
    | "string" -> type_string
    | id
    | type "[]" -> type_array

function_decl: type id "(" formals ")" stmt_block -> function_decl
    | "void" id "(" formals ")" stmt_block -> function_decl_void

formals: variable more_variables -> formals
    | -> formals_empty
more_variables: "," variable more_variables -> more_variables
    | 

class_decl: "class" id extends_optional implements_optional "{" fields "}" -> class_decl
extends_optional: "extends" id -> extends_optional
    | -> extends_optional_empty
implements_optional: "implements" id id_more
    | 
id_more: "," id id_more
    | 
fields: field fields
    | 

field: variable_decl
    | function_decl

interface_decl: "interface" id "{" prototypes "}"
prototypes: prototype prototypes
    | 

prototype: type id "(" formals ")" ";"
    |   "void" id "(" formals ")" ";"

stmt_block: "{" variable_decls stmts "}" -> stmt_block
variable_decls: variable_decls variable_decl -> variable_decls
    | -> variable_decls_empty
stmts: stmt stmts -> stmts
    | -> stmts_empty

stmt: expr_optional ";" -> stmt_expr_optional
    | if_stmt -> stmt_if_stmt
    | while_stmt -> stmt_while_stmt
    | for_stmt -> stmt_for_stmt
    | break_stmt -> stmt_break_stmt
    | return_stmt -> stmt_return_stmt
    | print_stmt -> stmt_print_stmt
    | stmt_block -> stmt_stmt_block
expr_optional: expr -> expr_optional
    | -> expr_optional_empty
    
if_stmt: ms -> if_stmt_ms
    | us -> if_stmt_us
ms: "if" "(" expr ")" stmt "else" stmt -> ms
    | "if" "(" expr ")" ms "else" ms -> ms
us: "if" "(" expr ")" stmt -> us
    | "if" "("expr")" ms "else" us -> ms

while_stmt: "while" "(" expr ")" stmt -> while_stmt

for_stmt: "for" "(" expr_optional ";" expr ";" expr_optional ")" stmt -> for_stmt

return_stmt: "return" expr_optional ";" -> return_stmt

break_stmt: "break" ";" -> break_stmt

print_stmt: "Print" "(" expr ")" ";" -> print_stmt
expr_merged: expr expr_more
expr_more: "," expr expr_more
    | 

expr: expr_assign -> expr
expr_assign: left_value "=" expr_assign -> expr_assign
    | expr_or -> expr_assign_pass
expr_or: expr_or "||" expr_and -> expr_or
    | expr_and -> expr_or_pass
expr_and: expr_and "&&" expr_equality -> expr_and
    | expr_equality -> expr_and_pass
expr_equality: expr_equality "==" expr_compare -> expr_equality_equal
    | expr_equality "!=" expr_compare -> expr_equality_not_equal
    | expr_compare -> expr_equality_pass
expr_compare: expr_compare "<" expr_add_sub -> expr_compare_l
    | expr_compare "<=" expr_add_sub -> expr_compare_le
    | expr_compare ">" expr_add_sub -> expr_compare_g
    | expr_compare ">=" expr_add_sub -> expr_compare_ge
    | expr_add_sub -> expr_compare_pass
expr_add_sub: expr_add_sub "+" expr_mul_div_mod -> expr_add_sub_plus
    | expr_add_sub "-" expr_mul_div_mod -> expr_add_sub_minus
    | expr_mul_div_mod -> expr_add_sub_pass
expr_mul_div_mod: expr_mul_div_mod "*" expr_not_negative -> expr_mul_div_mul
    | expr_mul_div_mod "/" expr_not_negative -> expr_mul_div_div
    | expr_mul_div_mod "%" expr_not_negative -> expr_mul_div_mod
    | expr_not_negative -> expr_mul_div_mod_pass
expr_not_negative: "!" expr_not_negative -> expr_not_negative_not
    | "-" expr_not_negative -> expr_not_negative_negative
    | expr_par -> expr_not_negative_pass
expr_par: "(" expr ")" -> expr_par
    | expr_atomic -> expr_par_pass
expr_atomic: constant -> expr_atomic_constant
    | left_value -> expr_atomic_left_value
    | call
    | "this"
    | "ReadInteger()" -> expr_atomic_read_integer
    | "ReadLine()" -> expr_atomic_read_line
    | "new" id
    | "NewArray" "(" expr "," type ")" -> expr_atomic_new_array

left_value: id -> left_value_id
    | expr_atomic "." id
    | expr_atomic "[" expr "]"

call: id "(" actuals ")" -> call
    | expr_atomic "."  id "(" actuals ")"

actuals: expr expr_more
    |

constant: INT -> constant_int
    | DOUBLE -> constant_double
    | BOOL -> constant_bool
    | STRING -> constant_string
    | "null"

id: /(?!(void|int|double|bool|string|class|interface|null|this|extends|implements|for|while|if|else|return|break|new|NewArray|Print|ReadInteger|ReadLine|true|false)([^a-zA-Z0-9_]|$))[A-Za-z][A-Za-z0-9_]{0,30}(?![A-Za-z0-9_])/

INT: /((0x|0X)[0-9a-fA-F]+|[0-9]+)/

DOUBLE: /[0-9]+\.[0-9]*([eE][+-]?[0-9]+)?/ 

BOOL : /(false|true)/

STRING: /"[^"]*"/

%import common.NEWLINE
COMMENT: "//" /(.)+/ NEWLINE
    | "/*" /(.|\\n)*/ "*/"

%import common.WS   
%ignore COMMENT
%ignore WS

"""

parser = Lark(grammar, parser="lalr", transformer=CodeGen(), debug=False)

code = """

int main() {
    double a;
    double b;
    double c;
    a = 2.5;
    b = 1.1;
    c = 1.1;
    Print(a+b);
    Print(a-b);
    Print(b-a);
    Print("-------------");
    Print(a/b);
    Print(b/a);
    Print(b/b);
    Print(b*c);
}

"""
parser.parse(code)
