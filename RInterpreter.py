import ply.lex as lex
import sys
import ast
#Arturo Guevara Chávez A01272373.
# Simple R Interpreter in python using PLY.

#Data structures ===============================================================

#Stack stores the different values that a variable gets at runtime
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

#Dictionary variables stores de different variables and their current value
variables={}
#Stack with the path the program takes in the execution part
path = Stack()
#Stack with the different assignments inside a block
asg = Stack()

#Function that gets the nodes of a for loop
def getNodes(ast_tree,j,asg):
    print(ast_tree[j])
    while ast_tree[j] != " '}'" and j<len(ast_tree):
        if(ast_tree[j]==" 'assignment'"):
            asg.push('a'+','+ast_tree[j+1]+',' + ast_tree[j+2]+ ',' + ast_tree[j+3])
        elif ast_tree[j] == " 'print'":
            val = str(ast_tree[j+2])
            print(val)
        j = j + 1
    return asg


#List with all the reserved words ==============================================
reserved = {
    'for' : 'FOR',
    'if' : 'IF',
    'else' : 'ELSE',
    'else_if': 'ELSE_IF',
    'in' : 'IN',
    'next' : 'NEXT',
    'break' : 'BREAK',
    'list' : 'LIST',
    'true' : 'TRUE', #Boolean true value
    'false' : 'FALSE', #Boolean false value
    'readline' : 'READLINE', #Standard input
    'prompt' : 'PROMPT',
    'print' : 'PRINT', #Standard output
}
#List of all the token definition.
tokens =[
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'REMAINDER',
    'QUOTIENT',
    'EXPONENT',
    'EQ',
    'GE',
    'LE',
    'NE',
    'AND',
    'OR',
    'GT',
    'LT',
    'ELA',
    'ELO',
    'NOT',
    'RIGHTASGN',
    'LEFTASGN',
    'COLON',
    'OPEN_PARENTHESES',
    'CLOSE_PARENTHESES',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'OPEN_SQR_BRACKET',
    'CLOSE_SQR_BRACKET',
    'COMA',
    'DOT',
    'COMMENT',
    'NUMERIC',
    'CHAR',
    'ID',
    'NEWLINE',
]+list(reserved.values())
#Token definition for operators.
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_REMAINDER= r'\%%'
t_QUOTIENT = r'\%/%'
t_EXPONENT = r'\^'
#Token definition for logical operators.
t_EQ = r'\=='
t_GE = r'\>='
t_LE = r'\<='
t_NE = r'\!='
t_AND = r'\&&'
t_OR = r'\|\|'
t_GT = r'\>'
t_LT = r'\<'
t_ELA = r'\&'
t_ELO = r'\|'
t_NOT = r'\!'
t_RIGHTASGN = r'\->'
t_LEFTASGN = r'\= | \<\-'
#Token definition for punctuation
t_COLON = r'\:'
t_OPEN_PARENTHESES = r'\('
t_CLOSE_PARENTHESES = r'\)'
t_OPEN_BRACKET = r'\{'
t_CLOSE_BRACKET = r'\}'
t_OPEN_SQR_BRACKET = r'\['
t_CLOSE_SQR_BRACKET = r'\]'
t_COMA= r'\,'
t_COMMENT= r'\#.*'
t_DOT= r'\.'
#Ignored expressions
t_ignore = r' '

#Error handling
def t_error(t):
    print("Invalid Token:",t.value[0],t.lineno)
    t.lexer.skip( 0 )
    return


#Regular Expresions
#Numeric data type
def t_NUMERIC(t):
    r'\d+\.\d+ | \d+'
    t.value = float(t.value)
    return t
#Char data type this includes the strings
def t_CHAR(t):
    r'\'[\S ' ']+\'| \"[\S ' ']+\"'
    t.type = 'CHAR'
    return t
#Valid id
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# Define a rule so we can track line numbers
#def t_NEWLINE(t):
#    r'\n+'
#    t.lexer.lineno += len(t.value)
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
#Build the lexer.
lexer = lex.lex()

#Dictionary with the test cases.

tests ={
    'test1' : '''#Hola''',
    'test2' : '''#Hola mundo''',
    'test3' : '''x = 1''',
    'test4' : '''"This is an R string"''',
    'test5' : '''a = 1 b = 2.3 c='this is a char' d = true ''',
    'test6' : '''for(i in 1:n){
                    if(i>=s){
                        s=true
                    }else{
                        s=false
                    }
    }''',
    'test7' : '''print(x) x<-readline()''',
    'test8' : ''' Wq=1
                    W=1.3
                    L='Hola mundo'
                    Ls=true
                    #Probabilidades de estado
                    for(i in 1:n){
                      if(i>=s){
                        Probabilidad[i]=Wq*Po
                      }else{
                        Probabilidad[i]=W*Po
                      }
                    }
                ''',
    'test9' :'''3 = x''',
    'test10' : '''x = 3.14 * "Radio" ''',
    'test11' : '''for(1.1 in 1:0){
                    print(i)
               }''',
}

#Begin to try the test cases.
i = 1
'''
for test in tests:
    print("Test :",i)
    data=tests[test]
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    i+=1
'''
#R programming language grammar Syntax part.Partial 2
import ply.yacc as yacc
from RCompiler import tokens


#Precedence table for R low first then high
precedence=(
    ('nonassoc','GT', 'GE', 'LT','LE', 'NE'),
    ('right','LEFTASGN'),
    ('right','EQ'),
    ('left','RIGHTASGN'),
    ('left','OR'),
    ('left','AND'),
    ('left','NOT'),
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE'),
    ('right','EXPONENT'),
    ('right','UMINUS'),
)

def p_program(p):
    '''
        program : stmt
    '''
    p[0] = p[1]
def p_stmt(p):
    '''
        stmt : simplestmt
            |  complexstmt
    '''
    p[0] = ('stmt',p[1])
def p_simplestmt(p):
    '''
    simplestmt : small_stmt simplehelper
    '''
    p[0] = p[1],p[2]
def p_simplehelper(p):
    '''
        simplehelper : small_stmt simplehelper
                    | empty

    '''
    p[0]=('simplehelper', p[1])
    if p[1] == "NEWLINE":
        p[0] = ('NEWLINE' , p[1] , p[2])
    else:
        p[0] = p[1]

def p_small_stmt(p):
    '''
        small_stmt : assignment
                    | expression
                    | print
                    | simple_block
                    | readline
                    | conditional
    '''
    p[0] = p[1]

def p_complexstmt(p):
    '''
        complexstmt : complex_block
    '''
    p[0] = ('complexstmt',p[1])

def p_expression_plus(p):
     'expression : expression PLUS term'
     if p[1] in variables and p[3] in variables:
         p[0] = (variables[p[1]] + variables[p[3]])
     elif p[1] in variables:
         p[0] = (variables[p[1]] + p[3])
     elif p[3] in variables:
         p[0] = (p[1] + variables[p[3]])
     else:
         p[0] =(p[1] + p[3])

     path.push(p[0])

def p_expression_minus(p):
     'expression : expression MINUS term'
     if p[1] in variables and p[3] in variables:
         p[0] = variables[p[1]] - variables[p[3]]
     elif p[1] in variables:
         p[0] = variables[p[1]] - p[3]
     elif p[3] in variables:
         p[0] = p[1] - variables[p[3]]
     else:
         p[0] = p[1] - p[3]

     path.push(p[0])

def p_expr_uminus(p):
     'expression : MINUS expression %prec UMINUS'
     p[0] = -p[2]
     path.push(-p[2])
def p_expression_term(p):
     'expression : term'
     p[0] = p[1]

     path.push(p[0])

def p_term_times(p):
     'term : term MULTIPLY factor'
     if p[1] in variables and p[3] in variables:
         p[0] = variables[p[1]] * variables[p[3]]
     elif p[1] in variables:
         p[0] = variables[p[1]] * p[3]
     elif p[3] in variables:
         p[0] = p[1] * variables[p[3]]
     else:
         p[0] = p[1] * p[3]
     path.push(p[0])

def p_term_div(p):
     'term : term DIVIDE factor'
     if p[1] in variables and p[3] in variables:
         p[0] = variables[p[1]] / variables[p[3]]
     elif p[1] in variables:
         p[0] = variables[p[1]] / p[3]
     elif p[3] in variables:
         p[0] = p[1] / variables[p[3]]
     else:
         p[0] = p[1] / p[3]
     path.push(p[0])
def p_term_factor(p):
     'term : factor'
     p[0] = p[1]
     path.push(p[1])
def p_factor_num(p):
     '''factor : NUMERIC
               | ID'''
     p[0] = (p[1])
     path.push(p[1])
def p_factor_expr(p):
     'factor : OPEN_PARENTHESES expression CLOSE_PARENTHESES'
     p[0] = p[2]
     path.push(p[2])


#Logical comparisons (<,>,<=,>=,!=):============================================
def p_logical_expressions(p):
    '''
        log_expression : factor LT factor
                | factor GT factor
                | factor LE factor
                | factor GE factor
                | factor EQ factor
                | factor NE factor
    '''
#=================================== Less than =================================
    if p[2] == "<":
        if p[1] in variables and p[3] in variables:
            p[0] = (variables[p[1]] < variables[p[3]])
        elif p[1] in variables:
            p[0] = (variables[p[1]] < p[3])
        elif p[3] in variables:
            p[0] = (p[1] < variables[p[3]])
        else:
            p[0] = (p[1] < p[3])
#==================================Grater than (GT)=============================
    elif p[2] == ">":
        if p[1] in variables and p[3] in variables:
            p[0] = (variables[p[1]] > variables[p[3]])
        elif p[1] in variables:
            p[0] = (variables[p[1]] > p[3])
        elif p[3] in variables:
            p[0] = (p[1] > variables[p[3]])
        else:
            p[0] = (p[1] > p[3])
#================================== Less Equal (LE)=============================
    elif p[2] == "<=":
        if p[1] in variables and p[3] in variables:
            p[0] = (variables[p[1]] <= variables[p[3]])
        elif p[1] in variables:
            p[0] = (variables[p[1]] <= p[3])
        elif p[3] in variables:
            p[0] = (p[1] <= variables[p[3]])
        else:
            p[0] = (p[1] <= p[3])
#================================== Greater Equal (GE)==========================
    elif p[2] == ">=":
        if p[1] in variables and p[3] in variables:
            p[0] = (variables[p[1]] >= variables[p[3]])
        elif p[1] in variables:
            p[0] = (variables[p[1]] >= p[3])
        elif p[3] in variables:
            p[0] = (p[1] >= variables[p[3]])
        else:
            p[0] = (p[1] >= p[3])
#================================== Equal (EQ)==================================
    elif p[2] == "==":
        if p[1] in variables and p[3] in variables:
            p[0] = (variables[p[1]] == variables[p[3]])
        elif p[1] in variables:
            p[0] = (variables[p[1]] == p[3])
        elif p[3] in variables:
            p[0] = (p[1] == variables[p[3]])
        else:
            p[0] = (p[1] == p[3])
#================================== Not Equal (NE)==============================
    elif p[2] == "!=":
        if p[1] in variables and p[3] in variables:
            p[0] = (variables[p[1]] != variables[p[3]])
        elif p[1] in variables:
            p[0] = (variables[p[1]] != p[3])
        elif p[3] in variables:
            p[0] = (p[1] != variables[p[3]])
        else:
            p[0] = (p[1] != p[3])

#Boolean expressions ().========================================================
def p_bool_expression(p):
    '''
        bool_expression : simple_comparison
                        | complex_comparison
    '''
    p[0] = p[1]

def p_simple_comparison(p):
    '''
        simple_comparison : log_expression AND log_expression
                    | log_expression OR log_expression
                    | log_expression NOT log_expression
    '''
    if len(p) == 4:
        if p[2] == "&&":
            p[0] = ('simple_and',p[1] and p[3])
        elif p[2] == "||":
            p[0] = ('simple_or',p[1] or p[3])
    elif len(p) == 3:
        p[0] = unary_ops[p[1]](p[2])
    else:
        p[0] = p[1]

#Comparison=====================================================================
def p_complex_comparison(p):
    '''
        complex_comparison :  simple_comparison AND complex_comparison
                            | simple_comparison OR complex_comparison
                            | simple_comparison NOT complex_comparison
                            | log_expression
    '''
    if len(p) == 4:
            if p[2] == "&&":
                p[0] = ('complex_and',p[1] and p[3])
            elif p[2] == "||":
                p[0] = ('complex_or',p[1] or p[3])
    elif len(p) == 3:
        p[0] = unary_ops[p[1]](p[2])
    else:
        p[0] = p[1]

#Conditional.===================================================================
def p_conditional_expression(p):
    'conditional : OPEN_PARENTHESES bool_expression CLOSE_PARENTHESES'
    p[0] =('conditional', p[2],p[1])

#Assignment=====================================================================
def p_left_assign_declaration(p):
    '''
    assignment : ID  LEFTASGN expression
                | ID LEFTASGN CHAR
                | ID LEFTASGN TRUE
                | ID LEFTASGN FALSE
    '''
    p[0] = ('assignment',p[1],'=',p[3])
    if p[1] in variables:
        variables[p[1]] = p[3]
    else:
        variables.update({p[1]:p[3]})

#print==========================================================================
def p_print(p):
    '''
        print : PRINT OPEN_PARENTHESES ID CLOSE_PARENTHESES
                | PRINT OPEN_PARENTHESES NUMERIC CLOSE_PARENTHESES
                | PRINT OPEN_PARENTHESES CHAR CLOSE_PARENTHESES
    '''
    p[0] = ('print',p[1],p[2],p[3],p[4])

#Readline=======================================================================
def p_readline(p):
    '''
        readline : READLINE OPEN_PARENTHESES CLOSE_PARENTHESES
                 | READLINE OPEN_PARENTHESES PROMPT LEFTASGN CLOSE_PARENTHESES
    '''
    if len(p)==5:
        p[0] = ('readline',p[1],p[2],p[3],p[4])
    elif len(p)==3:
        p[0] = ('readline',p[1],p[2])
#Simple block====================================================================================================================================================================
def p_simple_block(p):
    '''

        simple_block : IF conditional OPEN_BRACKET simplestmt CLOSE_BRACKET  ELSE_IF conditional OPEN_BRACKET simplestmt CLOSE_BRACKET ELSE OPEN_BRACKET simplestmt CLOSE_BRACKET
                     | IF bool_expression OPEN_BRACKET simplestmt CLOSE_BRACKET  ELSE OPEN_BRACKET simplestmt CLOSE_BRACKET
                     | IF conditional OPEN_BRACKET simplestmt CLOSE_BRACKET  ELSE_IF conditional OPEN_BRACKET simplestmt CLOSE_BRACKET
                     | IF conditional OPEN_BRACKET simplestmt CLOSE_BRACKET
                     | FOR OPEN_PARENTHESES ID IN NUMERIC COLON NUMERIC CLOSE_PARENTHESES OPEN_BRACKET simplestmt CLOSE_BRACKET
    '''
    if len(p)==14:
        p[0] =('simple_block',p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11],p[12],p[13])
    elif len(p)==12:
        p[0] =('simple_block',p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11])
    elif len(p)==11:
        p[0] =('simple_block',p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10])
    elif len(p)==10:
        p[0] =('simple_block',p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10])
    elif len(p)==6:
        p[0]=('simple_block',p[1],p[2],p[3],p[4],p[5])

#Complex block=======================================================================================================================================
def p_complex_block(p):
    '''
        complex_block : IF conditional OPEN_BRACKET simple_block CLOSE_BRACKET
                      | ELSE_IF conditional OPEN_BRACKET simple_block CLOSE_BRACKET
                      | ELSE conditional OPEN_BRACKET simple_block CLOSE_BRACKET
                      | FOR OPEN_PARENTHESES ID IN NUMERIC COLON NUMERIC CLOSE_PARENTHESES OPEN_BRACKET simple_block CLOSE_BRACKET
    '''
    if len(p)==14:
        p[0] =('complex_block',p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11],p[12],p[13])
    elif len(p)==12:
        p[0] =('complex_block',p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11])
    elif len(p)==11:
        p[0] =('complex_block',p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10])
    elif len(p)==6:
        p[0]=('complex_block',p[1],p[2],p[3],p[4],p[5])

#==============================Empty def========================================
def p_empty(p):
     'empty :'
     pass
# Error rule for syntax errors==================================================
def p_error(p):
    print ("Syntax error at '%s'" % p.value)

# Build the parser
syntaxTests={
    'test1' : '''x=0''',
    'test2' : '''for(i in 0:10){
                    if(i<1){
                        x=1
                    }else{

                        x=0'
                    }
                }
                ''',
    'test3' : '''print(a)''',
    'test4' : '''readline(prompt=)''',

    'test5' : '''for(i in 1:10){
                    if(i<1){
                        x=1
                    }else_if(x>0 && y!=0){
                        print(a)
                    }

                    e'
                     'pt=)
                    }'
                }''',
    'test6' : '3=x',
    'test7' : '''if('hola'>0){
                    x=1
                }else{
                    y=0
                }''',
    'test8' : '''for('hola' in 0:10){
                        print(r)
                    }'''
}
parser = yacc.yacc()
result= parser.parse('''
x=5
z = 5 + 3
y = z/2

''')

ast_tree = str(result)
print('--------------------------------AST---------------------------------------------')
print(ast_tree)
print('==================== Parsing variables =========================================')
print('Parsing variables',variables)
print('------------------------------ Path --------------------------------------------')
ast_tree = ast_tree.replace('(','')
ast_tree = ast_tree.replace(')','')
ast_tree = ast_tree.strip('')
ast_tree = ast_tree.split(",")
print(ast_tree)
#==================================== Execution ================================
i = 0
block = False
var= {}
for i in range(0,len(ast_tree)):
    #Getting if its inside a block or not
    if(ast_tree[i] == " '{'"):
        block = True
    elif(ast_tree[i] == " '}'"):
        block =False
    #Getting assignments outside the block
    if(ast_tree[i]==" 'assignment'"):
        if block == False:
            asg.push(ast_tree[i+1] + ast_tree[i+2] + ast_tree[i+3])
            var.update({ast_tree[i+1]:ast_tree[i+3]})

    #Getting the conditionl block
    elif ast_tree[i]==" 'conditional'" and ast_tree[i+1]==' True':
        j=i
        while ast_tree[j] != " '}'" and j<len(ast_tree):
            if(ast_tree[j]==" 'assignment'"):
                asg.push(ast_tree[j+1] + ast_tree[j+2] + ast_tree[j+3])
                var.update({ast_tree[j+1]:ast_tree[j+3]})
            elif ast_tree[j] == " 'print'":
                val = str(ast_tree[j+3])
            j = j + 1

    #Getting the for block instructions
    elif ast_tree[i] == " 'for'":
        times = float(ast_tree[i+6]) - float(ast_tree[i+4])
        times = int(times)
        j=i
        #Excecuting the for
        for y in range(0,times):
            asg = getNodes(ast_tree,j,asg)
            instruction = asg.pop()
            instruction = instruction.split(",")
            if(instruction[0]=='a'):
                index = instruction[1]
                new_val = float(var.get(index)) + float(instruction[3])
                var.update({instruction[1]:new_val})
#i =0


while asg.size() >0:
    print(i,'________________________________________')
    print(asg.pop())
print('=======================Execution variables======================================')
print('variables',var)
'''
test 1:
x=5
if(x<0){
    y=3+1
}
else_if(x>0){
    x=2
    y= 5
}

test 2:
x = 0
for(x in 0:10){
    x = 1 + 2
}
'''
