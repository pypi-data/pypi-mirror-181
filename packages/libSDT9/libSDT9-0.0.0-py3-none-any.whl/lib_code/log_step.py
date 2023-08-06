import sys
import re
import lib_py_parse.utils.parsing_utils as parsing_utils

# [file_src] => [log_step_file_src]
# assume [file_src] is syntactically correct
def log_step_transform(file_src):
    # lines = file_src.splitlines()
    code_statements = []

    index = 0
    current_line = ''
    # parse all code statements
    while index < len(file_src):

        # append current line
        if file_src[index] == '\n':
            # if current_line.find('\n') == -1:
            code_statements.append(current_line)
            current_line = ''
            index += 1
            continue

        # append string literal
        if file_src[index] in ['\'', '\"']:
            target_index = parsing_utils.get_quote_closure(file_src, index)
            current_line += file_src[ index : target_index ]
            index = target_index
            continue

        # append bracket closure
        if file_src[index] in '[{(':
            target_index = parsing_utils.get_char_closure(file_src, index+1)
            current_line += file_src[ index : target_index ]
            index = target_index
            continue

        current_line += file_src[index]
        index += 1
        continue

    if len(current_line) > 0:
        code_statements.append(current_line)

    # add print(statement) for statement in code_statements
    result_lines = []
    for line in code_statements:
        ls_str = line.lstrip()
        s_str = line.strip()
        nl_index = line.find('\n')

        if ls_str[0:6] == 'class ' or ls_str[0:4] == 'fxn ':
            result_lines.append(line)
            continue

        if nl_index != -1 or len(line) == 0 or len(ls_str) == 0 or ls_str[0] == '#':
            result_lines.append(line)
            continue

        if ls_str[0:8] == 'include ' or ls_str[0:7] == 'import ':
            result_lines.append(line)
            continue

        # if nl_index != -1:
        #     result_lines.append(line)
        #     continue

        line_indent = line[ 0 : len(line) - len(ls_str) ]
        s_str_esc = parsing_utils.escape_quote(s_str)
        # s_str_esc = repr(s_str)
        print_stmt = f'{line_indent}print(\'{s_str_esc}\')'
        result_lines.append(print_stmt)
        result_lines.append(line)

    return '\n'.join(result_lines)

def log_step_transform_write(file_name):
    fp = open(file_name, 'r')
    fsource = fp.read()
    fp.close()

    log_step_source = log_step_transform(fsource)
    print(log_step_source)

    fp = open(file_name, 'w')
    fp.write(log_step_source)
    fp.close()

def supress_log_step_write(file_name):
    fp = open(file_name, 'r')
    fsource = fp.read()
    fp.close()

    new_source = fsource.replace('print(', '# print(')
    print(new_source)

    fp = open(file_name, 'w')
    fp.write(new_source)
    fp.close()

def invert_log_step_transform( fsource ):
    regex_src = r'\n(\s+)print\((.*)\)'
    # regex_src = r''
    # regex_replace = r'\n'
    regex_replace = r''
    # regex_obj = re.compile(regex_src)
    new_source = re.sub(regex_src, regex_replace, fsource)
    # new_source = regex_obj.sub(regex_replace, fsource)
    # print(new_source)
    return new_source

def remove_print_statements(file_name):
    fp = open(file_name, 'r')
    fsource = fp.read()
    fp.close()

    new_source = invert_log_step_transform(fsource)

    fp = open(file_name, 'w')
    fp.write(new_source)
    fp.close()

def p1():
    # file_name = '/home/algorithmspath/sdev/hb_api_typon/api/login/lambda_function.typ'
    # file_name = '/home/algorithmspath/sdev/hb_api_typon/api/post_content/insert_hypothesis.typ'
    file_name = '/home/algorithmspath/sdev/hb_api_typon/api/_api_generic/distributed_linked_list_api/insert_utils.typ'
    file_name = '/home/algorithmspath/sdev/hb_api_typon/api/select_hypothesis/selection/hypothesis_module.typ'
    file_name = '/home/algorithmspath/sdev/hb_api_typon/api/list_hypotheses/list_utils.typ'

    if len(sys.argv) < 3:
        print(f'usage: {sys.argv[0]} ' + ' {target_file_name} {log_step_transform|remove_print_statements}')
        return

    argument_names = [
        'target_file_name',
        'log_step_transform|remove_print_statements'
    ]

    status_str_L1 = [
        f'{argument_names[i]}: {sys.argv[i+1]}'
        for i in range(0, len(argument_names))
    ]
    status_str = 'log_step_transform|remove_print_statements:\n' + '\n'.join(status_str_L1)

    print(status_str)
    print()

    file_name = sys.argv[1]
    op_code = sys.argv[2]

    if op_code == '0':
        log_step_transform_write(file_name)
        return

    if op_code == '1':
        remove_print_statements(file_name)
        return

    print('no_op')
    # supress_log_step_write(file_name)

def main():
    p1()
    pass

if __name__ == '__main__':
    main()
