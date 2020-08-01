from lark import Lark , Transformer
from CodeGen import CodeGen
from CodeGen_First_Pass import Cg
from Class import Class
import pprint

grammar = """
start: program

program: decl decl_more -> program
decl_more: decl decl_more -> decl_more
    | -> decl_more_empty

decl: variable_decl -> decl_variable_decl
    | function_decl -> decl_function_decl
    | class_decl -> decl_class_decl
    | interface_decl

variable_decl: variable ";" -> variable_decl

variable: type id -> variable

type: "int" -> type_int
    | "double" -> type_double
    | "bool" -> type_bool
    | "string" -> type_string
    | id -> type_id
    | type "[]" -> type_array

function_decl: type id "(" formals ")" stmt_block -> function_decl
    | "void" id "(" formals ")" stmt_block -> function_decl_void

formals: variable more_variables -> formals
    | -> formals_empty
more_variables: "," variable more_variables -> more_variables
    | -> more_variables_empty

class_decl: "class" id extends_optional implements_optional "{" fields "}" -> class_decl
extends_optional: "extends" id -> extends_optional
    | -> extends_optional_empty
implements_optional: "implements" id id_more
    | 
id_more: "," id id_more
    | 
fields: field fields -> fields
    | -> fields_empty

field: variable_decl -> field_variable
    | function_decl -> field_function

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

print_stmt: "Print" "(" print_exprs ")" ";" -> print_stmt
print_exprs: expr print_expr_more -> print_exprs
print_expr_more: "," expr print_expr_more -> print_exprs
    | -> print_expr_more_empty

expr_more: "," expr expr_more -> expr_more
    | -> expr_more_empty

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
    | expr_atomic -> expr_not_negative_pass
expr_atomic: constant -> expr_atomic_constant
    | left_value -> expr_atomic_left_value
    | call -> expr_atomic_call
    | "this" -> expr_atomic_this
    | "ReadInteger()" -> expr_atomic_read_integer
    | "ReadLine()" -> expr_atomic_read_line
    | "new" id -> expr_atomic_new
    | "NewArray" "(" expr "," type ")" -> expr_atomic_new_array
    | "(" expr ")" -> expr_par

left_value: id -> left_value_id
    | expr_atomic "." id -> left_value_obj_var
    | expr_atomic "[" expr "]" -> left_value_array_access

call: id "(" actuals ")" -> call
    | expr_atomic "."  id "(" actuals ")" -> call_obj_method

actuals: expr expr_more -> actuals
    | -> actuals_empty

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

code = """
class table {
	int [][] table;
	string [] chars;
	
	void init() {
		int i;
		int j;
		this.table = NewArray(3, int []);
		for (i = 0;i < 3;i = i + 1) {
			this.table[i] = NewArray(3, int);
		}
		for (i = 0;i < 3;i = i + 1) 
			for (j = 0;j < 3;j = j + 1)
				table[i][j] = 0;
		
		this.chars = NewArray(3, string);
		this.chars[0] = "E";
		this.chars[1] = "X";
		this.chars[2] = "O";
	}
	
	bool set(int x, int y, int player) {
		if (this.table[x][y] != 0) {
			Print("Illegal point!");
			return false;
		}
		this.table[x][y] = player;
		return true;
	}
	
	int winner() {
		int i;
		int player;
		i = 0;
		while (i < 3) {
			player = this.table[i][0];
			if (this.table[i][0] == this.table[i][1] && this.table[i][1] == this.table[i][2] && player != 0)
				return player;
			player = this.table[0][i];
			if (this.table[0][i] == this.table[1][i] && this.table[1][i] == this.table[2][i] && player != 0)
				return player;
			i = i + 1;
		}
		if (this.table[0][0] == this.table[1][1] && this.table[1][1] == this.table[2][2] && this.table[0][0] != 0)
			return this.table[0][0];
		if (this.table[0][2] == this.table[1][1] && this.table[1][1] == this.table[2][0] && this.table[2][0] != 0)
			return this.table[0][2];
		return 0;
	}
	
	bool is_full() {
		int i;
		int j;
		for (i = 0;i < 3;i = i + 1) 
			for (j = 0;j < 3;j = j + 1)
				if (table[i][j] == 0)
					return false;
		return true;
	}
	
	void print() {
		int i;
		for (i = 0;i < 3;i = i + 1) {
			Print(chars[table[i][0]], "|", chars[table[i][1]], "|", chars[table[i][2]]);
		}
	}
}

class dooz {
	table table;
	int nobat;
	
	void init() {
		table = new table;
		table.init();
		this.nobat = 1;
	}
	
	bool round(int x, int y) {
		bool ret;
		int win;
		ret = table.set(x, y, this.nobat);
		if (!ret) {
			Print("Try another point!");
			return false;
		}
		win = table.winner();
		if (win != 0) {
			Print("Player ", win, " winnes!");
			return true;
		}
		if (table.is_full()) {
			Print("Draw!");
			return true;
		}
		this.nobat = 3 - this.nobat;
		table.print();
		Print("player", nobat, " choose your point:");
		return false;
	}
}

int main() {
	dooz game;
	int x;
	int y;
	game = new dooz;
	game.init();
	Print("Player1 choose your point:");
	x = ReadInteger();
	y = ReadInteger();
	while(!game.round(x - 1, y - 1)) {
		x = ReadInteger();
		y = ReadInteger();
	}
}
"""

CodeGen_First_Pass = Cg()
parser_first_pass = Lark(grammar , parser="lalr" , transformer=CodeGen_First_Pass , debug=False)
parser_first_pass.parse(code)
# Class.log()
# raise Exception("First Pass !!!")
parser = Lark(grammar,
              parser="lalr",
              transformer=CodeGen(
                  CodeGen_First_Pass.get_functions(),
                  CodeGen_First_Pass.get_global_vars(),
                  CodeGen_First_Pass.get_structure()
              ),
              debug=False)
parser.parse(code)
