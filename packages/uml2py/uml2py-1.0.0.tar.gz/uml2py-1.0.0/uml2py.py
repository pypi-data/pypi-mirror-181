#! /usr/bin/env python3
'''
PlantUML ass diagram to python3 converter

Author: Pedro Reis dos Santos
Date: June 25, 2022
'''
__all__ = [ 'scan', 'grammar', 'uml2py' ]
from os import getenv
from graphlib import TopologicalSorter as toposort
from graphlib import CycleError
from ply import lex, yacc

# -------------- LEX ----------------
reserved = { 'class': 'CLASS', 'interface': 'INTERFACE', 'skinparam': 'SKINPARAM',
    '__': 'SEP4', 'abstract': 'ABSTRACT', 'static': 'STATIC', }
tokens = ( 'ID', 'INT', 'STR', 'SEP', 'SEP2', 'SEP3', 'START', 'END', 'DEPEND',
    'DEPEND2', 'INHERIT', 'INHERIT2', 'COMPOSE', 'COMPOSE2', 'AGGREG', 'AGGREG2',
    'TEMPLATE', ) + tuple(reserved.values())
literals = [',', '(', ')', ':', '{', '}', '[',']', '+', '-', '#', '~', '=' ]
t_ignore = ' \t\r'
t_INT = r'\d+'
t_STR = r'"([^"\\]|\\.)*"'
t_SEP = r'--'
t_SEP2 = r'=='
t_SEP3 = r'\.\.'
t_START = '@startuml'
t_END = '@enduml'
t_INHERIT = r'\<\|--|\<\|..'
t_INHERIT2 = r'--\|>|..\|>'
t_COMPOSE = r'\*--\>?'
t_COMPOSE2 = r'--\*|\<--\*'
t_AGGREG = r'o--\>?'
t_AGGREG2 = r'\<?--o'
t_DEPEND = r'\-\-\>'
t_DEPEND2 = r'\<\-\-'
t_TEMPLATE = r'\<[_A-Za-z][A-Za-z0-9_]*\>'

def t_ID(tok):
    r'[_A-Za-z][A-Za-z0-9_]*'
    tok.type = reserved.get(tok.value,'ID')
    return tok

def t_COMMENT(tok):
    r'\#.*\n'
    tok.lexer.lineno += 1
    # No return value. Token discarded

def t_newline(tok):
    r'\n'
    tok.lexer.lineno += 1
    # No return value. Token discarded

def t_error(tok):
    ''' error handler '''
    print(f"{tok.lexer.lineno}: Illegal character '{tok.value[0]}'")
    print(tok.value)
    tok.lexer.skip(1)

def scan(data): # for debug
    ''' scan input tokens '''
    lexer = lex.lex(debug=True)
    lexer.input(data)
    for tok in lexer:
        print(tok)

# -------------- YACC ----------------
precedence = []
DBG=False
GRAPH = {} # for topological sorting of class dependecies
CLASSES = set() # top level names

def p_uml(node):
    '''uml : START decls END '''
    if DBG:
        print(node[2])
    node[0] = node[2]

def p_decls_0(node):
    '''decls : '''
    node[0] = ()

def p_decls_1(node):
    '''decls : decls SKINPARAM ID ID '''
    node[0] = node[1]

def p_decls_2(node):
    '''decls : decls SKINPARAM ID INT '''
    node[0] = node[1]

def p_decls_3(node):
    '''decls : decls class '''
    node[0] = node[1] + (node[2],)

def p_decls_4(node):
    '''decls : decls assoc '''
    node[0] = node[1] + (node[2],)

def p_class_0(node):
    '''class : abs CLASS ID '{' attribs '}' '''
    node[0] = ('CLASS', node[3], node[5], node[1])
    if node[3] not in GRAPH:
        GRAPH[node[3]] = set()
    global CLASSES
    CLASSES |= { node[3] }

def p_class_1(node):
    '''class : abs INTERFACE ID '{' attribs '}' '''
    node[0] = ('INTERFACE', node[3], node[5], node[1])
    if node[3] not in GRAPH:
        GRAPH[node[3]] = set()
    global CLASSES
    CLASSES |= { node[3] }

def p_abs_0(node):
    '''abs : '''
    node[0] = None

def p_abs_1(node):
    '''abs : ABSTRACT '''
    node[0] = 'ABSTRACT'

def p_attribs_0(node):
    '''attribs : '''
    node[0] = ()

def p_attribs_1(node):
    '''attribs : attribs prot ID vec type init'''
    node[0] = node[1] + ((node[2], node[3], node[5], node[6]),)

def p_attribs_2(node):
    '''attribs : attribs prot ID '(' ')' type'''
    node[0] = node[1] + ((node[2], None, node[3], node[6], ()),)

def p_attribs_3(node):
    '''attribs : attribs prot ID '(' args ')' type'''
    node[0] = node[1] + ((node[2], None, node[3], node[7], node[5]),)

def p_attribs_8(node):
    '''attribs : attribs prot STATIC ID '(' ')' type'''
    node[0] = node[1] + ((node[2], node[3], node[4], node[7], ()),)

def p_attribs_9(node):
    '''attribs : attribs prot STATIC ID '(' args ')' type'''
    node[0] = node[1] + ((node[2], node[3], node[4], node[8], node[6]),)

def p_attribs_10(node):
    '''attribs : attribs prot ABSTRACT ID '(' ')' type'''
    node[0] = node[1] + ((node[2], node[3], node[4], node[7], ()),)

def p_attribs_11(node):
    '''attribs : attribs prot ABSTRACT ID '(' args ')' type'''
    node[0] = node[1] + ((node[2], node[3], node[4], node[8], node[6]),)

def p_attribs_4(node):
    '''attribs : attribs SEP'''
    node[0] = node[1]
    if DBG:
        print("SEP:", node[2])

def p_attribs_5(node):
    '''attribs : attribs SEP2'''
    node[0] = node[1]
    if DBG:
        print("SEP:", node[2])

def p_attribs_6(node):
    '''attribs : attribs SEP3'''
    node[0] = node[1]
    if DBG:
        print("SEP:", node[2])

def p_attribs_7(node):
    '''attribs : attribs SEP4'''
    node[0] = node[1]
    if DBG:
        print("SEP:", node[2])

def p_type_0(node):
    '''type : '''
    node[0] = None

def p_type_1(node):
    '''type : ':' ID vec'''
    node[0] = node[2]

def p_args_0(node):
    '''args : ID type'''
    node[0] = ((node[1], node[2]),)

def p_args_1(node):
    '''args : args ',' ID type'''
    node[0] = node[1] + ((node[3], node[4]),)

def p_prot_0(node):
    '''prot : '+' '''
    node[0] = 'PUBLIC'

def p_prot_1(node):
    '''prot : '-' '''
    node[0] = 'PRIVATE'

def p_prot_2(node):
    '''prot : '~' '''
    node[0] = 'PACKAGE'

def p_prot_3(node):
    '''prot : '#' '''
    node[0] = 'PROTECTED'

def p_prot_4(node): # remove?
    '''prot : '''
    node[0] = None

def p_vec_0(node):
    '''vec : '''
    node[0] = None

def p_vec_1(node):
    '''vec : '[' ']' '''
    node[0] = None

def p_vec_2(node):
    '''vec : '[' INT ']' '''
    node[0] = None

def p_vec_3(node):
    '''vec : TEMPLATE '''
    node[0] = None

def p_init_0(node):
    '''init : '''
    node[0] = None

def p_init_1(node):
    '''init : '=' ID'''
    node[0] = node[2]

def p_init_2(node):
    '''init : '=' STR'''
    node[0] = node[2]

def p_init_3(node):
    '''init : '=' INT'''
    node[0] = node[2]

def p_assoc_0(node):
    '''assoc : ID INHERIT ID'''
    node[0] = ('INHERIT', node[1], node[3])
    global CLASSES
    CLASSES |= { node[1], node[3] }
    if node[1] not in GRAPH:
        GRAPH[node[1]] = set()
    if node[3] not in GRAPH:
        GRAPH[node[3]] = { node[1] }
    else:
        if node[1] not in GRAPH[node[3]]:
            GRAPH[node[3]] = GRAPH[node[3]] | { node[1] }

def p_assoc_1(node):
    '''assoc : ID INHERIT2 ID'''
    node[0] = ('INHERIT', node[3], node[1])
    global CLASSES
    CLASSES |= { node[1], node[3] }
    if node[3] not in GRAPH:
        GRAPH[node[3]] = set()
    if node[1] not in GRAPH:
        GRAPH[node[1]] = { node[3] }
    else:
        if node[3] not in GRAPH[node[1]]:
            GRAPH[node[1]] = GRAPH[node[1]] | { node[3] }

def p_assoc_2(node):
    '''assoc : ID card aggreg card ID type'''
    node[0] = (node[3], node[1] , node[2], node[6], node[4], node[5])
    global CLASSES
    CLASSES |= { node[1], node[5] }
    if node[5] not in GRAPH:
        GRAPH[node[5]] = set()
    if node[1] not in GRAPH:
        GRAPH[node[1]] = set()

def p_assoc_3(node):
    '''assoc : ID card reverse card ID type'''
    node[0] = (node[3], node[5] , node[4], node[6], node[2], node[1])
    global CLASSES
    CLASSES |= { node[1], node[5] }
    if node[1] not in GRAPH:
        GRAPH[node[1]] = set()
    if node[5] not in GRAPH:
        GRAPH[node[5]] = set()

def p_aggreg_0(node):
    '''aggreg : AGGREG '''
    node[0] = 'AGGREG'

def p_aggreg_1(node):
    '''aggreg : COMPOSE '''
    node[0] = 'COMPOSE'

def p_aggreg_2(node):
    '''aggreg : DEPEND '''
    node[0] = 'DEPEND'

def p_aggreg_3(node):
    '''aggreg : SEP '''
    node[0] = 'ASSOC'

def p_aggreg_4(node): # no match for "o--" use ID=='o' and SEP (ply!!!)
    '''aggreg : ID SEP '''
    if node[1] != 'o':
        p_error(node)
    node[0] = 'AGGREG'

def p_aggreg_5(node): # no match for "o-->" use ID=='o' and SEP (ply!!!)
    '''aggreg : ID DEPEND '''
    if node[1] != 'o':
        p_error(node)
    node[0] = 'AGGREG'

def p_reverse_0(node):
    '''reverse : AGGREG2 '''
    node[0] = 'AGGREG'

def p_reverse_1(node):
    '''reverse : COMPOSE2 '''
    node[0] = 'COMPOSE'

def p_reverse_2(node):
    '''reverse : DEPEND2 '''
    node[0] = 'DEPEND'

def p_card_0(node):
    '''card : '''
    node[0] = None

def p_card_1(node):
    '''card : STR '''
    node[0] = node[1]

def p_error(node):
    ''' error handler '''
    print('Rule error:', node)

# -------------- MAIN ----------------

def _defined(ident: str):
    ''' check whether an identifier is defined '''
    try:
        eval(ident)
    except NameError:
        return False
    else:
        return True

def _args(meth: tuple, first: bool):
    ''' convert function argument to code '''
    if not meth or len(meth) <= 4:
        return
    for arg in meth[4]:
        if first:
            first = False
        else:
            print(", ", end='')
        print(arg[0], end='')
        if arg[1]:
            print(":", arg[1], end='')

def _ctor(ident: str, attr: tuple, gram: tuple):
    ''' convert constructor to code '''
    ctor = None
    for item in attr:
        if len(item) > 4 and item[2] == '__init__':
            ctor = item
            break
    if not ctor:
        for item in attr:
            if len(item) > 4 and item[2] == ident:
                ctor = item
                #item[2] = '__init__'
                break
    print("    def __init__(self", end='')
    _args(ctor, False)
    print("):")
    cnt = 0
    for item in attr:
        if len(item) <= 4:
            cnt += 1
            print("        self."+item[1], end='')
            if item[2]:
                print(":", item[2], end='')
            if len(item) > 3 and item[3]:
                print(" =", item[3])
            else:
                print(" = None")
    for item in gram:
        if item[0] in ('COMPOSE', 'AGGREG') and item[1] == ident:
            cnt += 1
            name = item[3] if item[3] else "field"+str(cnt)
            print("        self."+name, ":", item[5], "= None")
    if not cnt:
        print("        pass")

def _methods(ident: str, attr: tuple):
    ''' convert method to code '''
    ctor = None
    for item in attr:
        if len(item) > 4:
            if item[2] == '__init__':
                ctor = item
                continue
            first = False
            if item[2] == ident:
                if not ctor:
                    ctor = item
                    continue
                print("    @classmethod")
                print("    def", item[2], "(cls", end='')
            elif item[1] == 'STATIC':
                print("    @staticmethod")
                print("    def", item[2], "(", end='')
                first = True
            else:
                print("    def", item[2], "(self", end='')
            _args(item, first)
            if item[3]:
                print(") ->", item[3], ":")
            else:
                print("):")
            if item[1] == 'ABSTRACT':
                print("        raise NotImplementedError")
            else:
                print("        pass")

def uml2py(gram):
    ''' convert grammar to code: print to sys.stdout '''
    if DBG:
        print('# classes =', CLASSES)
    abc = False # use abstract classes
    for ident in CLASSES:
        if not _defined(ident):
            print(ident, '= None # type forward declaration (use Self in python3.11+)')
    try:
        if DBG:
            print('## graph =',GRAPH)
        topo = tuple(toposort(GRAPH).static_order())
        if DBG:
            print('## topo =',topo)
        for ident in topo:
            CLASSES.remove(ident)
            nocls = True
            data = None
            for data in gram:
                if data[0] in ('CLASS', 'INTERFACE') and data[1] == ident:
                    nocls = False
                    break
            inherit = ''
            if data and data[0] == 'INTERFACE':
                if not abc:
                    abc = True
                    print("from abc import ABC as abstract")
                inherit = '(abstract'
            for cls in GRAPH[ident]:
                if inherit:
                    inherit += ', ' + cls
                else:
                    inherit = '(' + cls
            if inherit:
                inherit += ')'
            print("class", ident, inherit, ':')
            if nocls:
                _ctor(ident, (), gram)
            else:
                _ctor(ident, data[2], gram)
                _methods(ident, data[2])
            print()
        if DBG:
            print('## missing =', CLASSES)
    except CycleError:
        print("ERROR: Inheritance dependency cyles")

def grammar(data):
    ''' parse input data into grammar tuple '''
    gram = yacc.yacc().parse(data, debug=False, tracking=True, lexer=lex.lex())
    return gram

if getenv("DEBUG"):
    DBG = True
if __name__ == '__main__':
    import sys # for .stdout
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf8") as fp:
            uml = fp.read()
        tree = grammar(uml)
        if DBG:
            print('##', tree)
    else:
        print(f"USAGE: {sys.argv[0]} filename.uml [output.py]")
        sys.exit(1)
    if len(sys.argv) > 2:
        sys.stdout = open(sys.argv[2], "w", encoding="utf8")
    uml2py(tree)
    if len(sys.argv) > 2:
        sys.stdout.close()
