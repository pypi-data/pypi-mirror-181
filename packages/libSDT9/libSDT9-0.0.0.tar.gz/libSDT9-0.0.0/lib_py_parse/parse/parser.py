import json
import lib_py_parse.utils.exceptions as exceptions
import lib_py_parse.utils.parsing_utils as parsing_utils

def parse_def(code, index, scope):
    K1 = 4
    assert code[index:index+K1] == 'def '
    i1 = parsing_utils.read_next_cleared_char(code, index, ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid fxn declaration, closing colon not found')
    s1 = code[index:i1]
    i2 = s1.find('(', 0)
    if i2 == -1:
        exceptions.raise_exception_msgs(code, index, ['Invalid fxn declaration, parenthesis not found', f'Line: {s1}'])
    name = s1[K1:i2].strip()
    arguments = s1[i2:].strip()
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
            'type' : 'fxn',
            'index' : index,
            'name' : name,
            'arguments' : arguments,
            'statements' : statements,
        }
    return result, end_index


def parse_class(code, index, scope):
    K1 = 6
    assert code[index:index+K1] == 'class '
    i1 = parsing_utils.read_next_cleared_char(code, index, ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid class declaration, closing colon not found')
    s1 = code[index:i1]
    i2 = s1.find('(', 0)
    if i2 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid class declaration, parenthesis not found')
    name = s1[K1:i2].strip()
    inherits = s1[i2:].strip()
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
            'type' : 'class',
            'index' : index,
            'name' : name,
            'inherits' : inherits,
            'statements' : statements,
        }
    return result, end_index


def parse_try(code, index, scope):
    K1 = 4
    assert code[index:index+K1] == 'try:'
    i1 = parsing_utils.read_next_cleared_char(code, index, ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid try declaration, closing colon not found')
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
            'type' : 'try',
            'index' : index,
            'statements' : statements,
        }
    return result, end_index


def parse_except(code, index, scope):
    K1 = 7
    assert code[index:index+K1] == 'except:' or code[index:index+K1] == 'except '
    i1 = parsing_utils.read_next_cleared_char(code, index, ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid class declaration, closing colon not found')
    s1 = code[index:i1]
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
            'type' : 'except',
            'index' : index,
            'declaration' : s1,
            'statements' : statements,
        }
    return result, end_index


def parse_L1_CE(code, index, scope, token):
    assert code[index:index+len(token)] == token
    i1 = parsing_utils.read_next_cleared_char(code, index+len(token), ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, f'Invalid {token} declaration, closing colon not found')
    declaration = code[index+len(token):i1].strip()
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
            'type' : token,
            'index' : index,
            'declaration' : declaration,
            'statements' : statements,
        }
    return result, end_index


def parse_L0_statement(code, index, scope):
    i1 = parsing_utils.read_next_cleared_char(code, index, '\n')
    if i1 == -1:
        i1 = len(code)
    expression = code[index:i1]
    result = {
            'type' : 'instruction',
            'index' : index,
            'expression' : expression,
        }
    return result, i1


def parse_import(code, index, scope):
    assert code[index:index+6] == 'import'
    i1 = parsing_utils.read_next_cleared_char(code, index, '\n')
    if i1 == -1:
        i1 = len(code)
    result = {
            'type' : 'import',
            'index' : index,
            'expression' : code[index:i1],
        }
    return result, i1


def parse_include(code, index, scope):
    assert code[index:index+7] == 'include'
    i1 = parsing_utils.read_next_cleared_char(code, index, '\n')
    if i1 == -1:
        i1 = len(code)
    result = {
            'type' : 'include',
            'index' : index,
            'expression' : code[index:i1],
        }
    return result, i1


def parse_abstract_statement(code, index, scope, start_token):
    L2_router = {
            'class' : parse_class,
            'def' : parse_def,
        }
    L1_CE_router = {
            'for' : 1,
            'while' : 1,
            'with' : 1,
            'if' : 1,
            'elif' : 1,
            'else' : 1,
        }
    L1_special_items = {
            'try' : parse_try,
            'except' : parse_except,
        }
    L0_misc_router = {
            'import' : parse_import,
            'include' : parse_include,
        }
    if start_token in L2_router:
        return L2_router[start_token](code, index, scope)
    if start_token in L1_special_items:
        return L1_special_items[start_token](code, index, scope)
    if start_token in L1_CE_router:
        return parse_L1_CE(code, index, scope, start_token)
    if start_token in L0_misc_router:
        return L0_misc_router[start_token](code, index, scope)
    return parse_L0_statement(code, index, scope)


def read_scope(code, index, scope):
    result = []
    N = float('inf')
    ctr = 0
    while True and ctr < N:
        start_token, i1 = parsing_utils.read_init_token(code, index, scope)
        if start_token == '#':
            i1 = code.find('\n', i1)
            if i1 == -1:
                return result, len(code)
            index = i1
            continue
        if start_token in ['EOF', 'EOS']:
            return result, i1
        assert start_token == code[i1-len(start_token):i1]
        abstract_statement, index = parse_abstract_statement(code, i1 - len(start_token), scope, start_token)
        result.append(abstract_statement)
        ctr += 1
    raise Exception('parse timeout')
