import os
import json
import lib_compute.graph_alg as graph_alg
import lib_py_parse.utils.fs_mod as fs_mod
import lib_py_parse.utils.parsing_utils as parsing_utils
import lib_py_parse.parse.parse_skeleton as parse_skeleton
import lib_py_parse.parse.parse_L0_skeleton as parse_L0_skeleton

def fmt_json(X):
    S1 = json.dumps(X, indent=4)
    print(S1)
    return S1


def render_indented_stmts( stmt ):
    indent_str = ' ' * 4
    stmts_L1 = []
    for x in stmt['statements']:
        S1 = render_stmt( x )
        stmts_L1.append( S1 )
    stmts_repr = '\n'.join(stmts_L1)
    stmts_repr = parsing_utils.indent_multiline_str(' ' * 4, stmts_repr)
    stmts_repr_L1 = [
            x
            for x in stmts_repr.splitlines()
            if len( x.strip() ) > 0
        ]
    stmts_repr = '\n'.join(stmts_repr_L1)
    return stmts_repr


def render_fxn_repr( stmt ):
    name = stmt['name']
    arguments = stmt['arguments']
    stmts_repr = render_indented_stmts( stmt )
    return f'''
    def {name}{arguments}:
    {stmts_repr}
    '''


def render_class_repr( stmt ):
    name = stmt['name']
    inherits = stmt['inherits']
    stmts_repr = render_indented_stmts( stmt )
    return f'''
    class {name}{inherits}:
    {stmts_repr}
    '''


def render_instruction_repr( stmt ):
    return stmt['expression']


def render_import_repr( stmt ):
    return stmt['expression']


def render_L1_control( stmt ):
    ctl = stmt['type']
    decl = stmt['declaration']
    stmts_repr = render_indented_stmts( stmt )
    return f'''
    {ctl} {decl}:
    {stmts_repr}
    '''


def render_try_repr( stmt ):
    ctl = stmt['type']
    stmts_repr = render_indented_stmts( stmt )
    return f'''
    {ctl}:
    {stmts_repr}
    '''


def render_except_repr( stmt ):
    ctl = stmt['type']
    stmts_repr = render_indented_stmts( stmt )
    return f'''
    {ctl}:
    {stmts_repr}
    '''


def render_stmt( stmt ):
    router = {
            type_name : eval( f'render_{type_name}_repr' )
            for type_name in [
                'fxn',
                'class',
                'instruction',
                'import',
                'try',
                'except',
            ]
        }
    if stmt['type'] in router:
        return router[ stmt['type'] ]( stmt )
    return render_L1_control( stmt )


def rm_comment_U1(mod_skeleton_U1):
    result = [
            render_stmt( stmt )
            for stmt in mod_skeleton_U1
        ]
    return '\n'.join(result)


def rm_comment_module( target_module, module_dir ):
    skeleton = parse_L0_skeleton.select_code_skeletons(target_module, module_dir)
    return rm_comment_U1(skeleton[target_module])


def rm_comment_pkg( pkg_ns, pkg_base ):
    target_module_L1 = fs_mod.iter_py_mod( pkg_ns, pkg_base )
    M1 = {
            target_module : [
                rm_comment_module( target_module, pkg_base ),
                fspath,
            ]
            for target_module, fspath in target_module_L1
        }
    return M1


def rm_comment_pkg_src( pkg_ns, pkg_base ):
    M1 = rm_comment_pkg( pkg_ns, pkg_base )
    for target_module in M1:
        rm_comment_src, fspath = M1[target_module]
        fp = open(fspath, 'w')
        fp.write(rm_comment_src)
        fp.close()
    return M1


def p1():
    target_module = 'lib_dsa.graph_db'
    module_dir = '/home/algorithmspath/vol1/py_lib_src'
    pkg_ns = 'lib_compute'
    pkg_base = '/home/algorithmspath/vol1/py_lib_src'
    result = rm_comment_pkg( pkg_ns, pkg_base )
    S1 = json.dumps(result, indent=4)
    print(S1)


def main():
    pass


if __name__ == '__main__':
    main()
