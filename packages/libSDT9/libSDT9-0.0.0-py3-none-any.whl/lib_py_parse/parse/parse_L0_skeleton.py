import os
import traceback
import lib_py_parse.parse.parser as parser
import lib_py_parse.utils.fmt_utils as fmt_utils
import lib_py_parse.utils.exceptions as exceptions
import lib_py_parse.helper.eval_helper as eval_helper
import lib_py_parse.helper.eval_service as eval_service

def select_modules_to_read(item_skeleton):
    L1 = [
        x for x in item_skeleton
        if x['type'] == 'import'
    ]
    result = []
    for T1 in L1:
        T2 = [
            T3.strip()
            for T3 in T1['expression'][6:].split(' as ')
        ]
        if len(T2) != 2:
            continue
        # if len(T2) != 2:
        #     error_msgs = [
        #         'invalid import statement',
        #         'import statement must be formatted as:',
        #         'import {module_name} as {module_alias}',
        #     ]
        #     exceptions.raise_exception_ue(error_msgs)
        module_name, module_alias = T2
        result.append(module_name)
    return result

def read_import_to_skeleton(item, module_L0_skeleton, current_module):
    T1 = [
        T2.strip()
        for T2 in item['expression'][6:].split(' as ')
    ]
    assert len(T1) == 2
    # print(T1)
    module_name, module_alias = T1
    module_L0_skeleton['imports']['alias_map'][module_alias] = module_name

def read_L0_skeleton(current_module, item_skeleton):
    try:
        modules_to_read = select_modules_to_read(item_skeleton)
        # module_L0_skeleton = format_L0_skeleton(item_skeleton, current_module)
        module_L0_skeleton = item_skeleton
    except Exception as e:
        e_msg = f'''
error reading module: {current_module}
error_msg: {str(e)}
'''
        traceback.print_exc()
        exit(1)
        # raise Exception(e_msg)

    return modules_to_read, module_L0_skeleton

def fmt_code(src_dir):
    S1 = open(src_dir, 'r').read()
    L1 = S1.splitlines()
    L2 = []
    for line in L1:
        l1 = line.lstrip()
        if len(l1) == 0:
            L2.append(l1)
            continue
        if l1[0] == '#':
            L2.append('')
            continue
        L2.append(line)

    L2.append('')
    result = '\n'.join(L2)
    return result

# module_dir -> base directory of module
def select_code_skeletons(target_module, module_dir):
    q = [target_module]
    L0_skeleton = {}
    # item_skeletons = {}
    visited_modules = {}
    # source_codes = {}
    included_c_exts_map = {}
    while len(q) > 0:
        current_module = q.pop()
        # print(current_module)
        if current_module in visited_modules:
            continue

        try:
            src_file = fmt_utils.select_module_src_dir(module_dir, current_module)
        # if not os.path.exists(src_file):
        except Exception as e:
            continue

        fp = open(src_file, 'r')
        code = fp.read()
        fp.close()


        try:
            item_skeleton, end_index = parser.read_scope(code, 0, 0)
        except Exception as e:
            traceback.print_exc()
            print(src_file)
            exit(1)
            # exceptions.raise_parsing_exception(str(e), current_module, src_dir)
        # fmt_utils.print_json(item_skeleton)
        modules_to_read, module_L0_skeleton = read_L0_skeleton(current_module, item_skeleton)
        visited_modules[current_module] = 1
        # item_skeletons.append(item_skeleton)
        q += [
            tgt_module
            for tgt_module in modules_to_read
            if tgt_module not in visited_modules
        ]
        L0_skeleton[current_module] = module_L0_skeleton

    return L0_skeleton
