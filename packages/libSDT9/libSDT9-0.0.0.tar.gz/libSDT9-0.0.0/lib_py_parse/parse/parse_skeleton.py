import json
import lib_py_parse.helper.type_resolver as type_resolver
import lib_py_parse.parse.parse_L0_skeleton as parse_L0_skeleton
import lib_py_parse.utils.fs_mod as fs_mod
import lib_py_parse.utils.parsing_utils as parsing_utils
import lib_compute.graph_alg as graph_alg

def gen_mod_repr( mod_skeleton_U1 ):
    U1_repr_L1 = []
    for stmt in mod_skeleton_U1:
        if stmt['type'] == 'fxn':
            X = 'def ' + stmt['name'] + stmt['arguments']
            U1_repr_L1.append( X )
            U1_repr_L1.append( '' )
            continue
        if stmt['type'] == 'class':
            X = 'class ' + stmt['name'] + stmt['inherits']
            U1_repr_L1.append( X )
            for stmt2 in stmt['statements']:
                if stmt2['type'] == 'fxn':
                    X2 = ' ' * 4 + 'def ' + stmt2['name'] + stmt2['arguments']
                    U1_repr_L1.append( X2 )
                    U1_repr_L1.append( '' )
                    continue
            U1_repr_L1.append( '' )
    return '\n'.join( U1_repr_L1 )


def generate_api_def(target_module, module_dir, target_only=False):
    mod_skeleton = parse_L0_skeleton.select_code_skeletons(target_module, module_dir)
    api_def_L1 = []
    if not target_only:
        for module_name in mod_skeleton:
            mod_repr = gen_mod_repr( mod_skeleton[module_name] )
            mod_repr = parsing_utils.indent_multiline_str(' ' * 4, mod_repr)
            api_def_L1.append( f'{module_name}' )
            api_def_L1.append( '' )
            api_def_L1.append( mod_repr )
            api_def_L1.append( '' )
        api_def = '\n'.join(api_def_L1)
        return api_def
    mod_repr = gen_mod_repr( mod_skeleton[target_module] )
    mod_repr = parsing_utils.indent_multiline_str(' ' * 4, mod_repr)
    api_def_L1.append( f'{target_module}' )
    api_def_L1.append( '' )
    api_def_L1.append( mod_repr )
    api_def_L1.append( '' )
    api_def = '\n'.join(api_def_L1)
    return api_def


def generate_pkg_api_def( pkg_ns, pkg_base ):
    target_module_L1 = fs_mod.iter_py_mod( pkg_ns, pkg_base )
    L2 = [
            generate_api_def( target_module, pkg_base, target_only=True )
            for target_module, fspath in target_module_L1
        ]
    return '\n'.join(L2)


def read_relative_skeleton(target_module, module_dir):
    skeleton = parse_L0_skeleton.select_code_skeletons(target_module, module_dir)
    return skeleton


def p1():
    target_module = 'lib_dsa.graph_db'
    module_dir = '/home/algorithmspath/vol1/py_lib_src'
    pkg_ns = 'lib_compute'
    pkg_base = '/home/algorithmspath/vol1/py_lib_src'
    skeleton = read_relative_skeleton(target_module, module_dir)
    S1 = json.dumps(skeleton['lib_dsa.kv_iter'], indent=4)
    print(S1)


def main():
    p1()
    pass


if __name__ == '__main__':
    main()
