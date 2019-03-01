import ply.lex as lex
import ply.yacc as yacc
import sys

#Arturo Guevara Chávez A01272373.

#List with all the reserved words.
reserved = {
    'for' : 'FOR',
    'if' : 'IF',
    'else' : 'ELSE',
    'in' : 'IN',
    'next' : 'NEXT',
    'break' : 'BREAK',
    'list' : 'LIST',
    'true' : 'TRUE', #Boolean true value
    'false' : 'FALSE',#Boolean false value
    'readline' : 'READLINE', #Standard input
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
#Keeps track of the line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
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
