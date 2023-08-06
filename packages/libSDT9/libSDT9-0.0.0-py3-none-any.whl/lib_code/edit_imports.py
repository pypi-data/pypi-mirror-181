import os
import sys
import lib_code.parse_imports as parse_imports

def read_src(file_path):
    fp = open(file_name, 'r')
    src_code = fp.read()
    fp.close()
    return src_code

# remove [pkg_ns] to [target_modules] in [file_path] s.t. [pkg_ns]. == import[ : len([pkg_ns].) ]
# assume [file_path] is validly formatted typon code
# ex: pkg_name = "package1", target_modules = ['mod1', 'mod2']
def rm_pkg_ns_typ(file_path, pkg_name, target_modules):
    src_code = read_src(file_path)

    include_set, aliased_imports, code_minus_imports = parse_imports.split_imports_typ(src_code)

    for module_name in target_modules:
        if module_name not in aliased_imports:
            # raise Exception( f'module does not exist: {module_name}' )
            continue
        # literal = "[pkg_ns]."
        if module_name[0:len(pkg_name)+1] != pkg_name + '.':
            continue

        module_alias = aliased_imports[module_name]
        del aliased_imports[module_name]
        trunc_mod_name = module_name[len(pkg_name)+1:]
        aliased_imports[trunc_mod_name] = module_alias

    return parse_imports.join_imports_typ(include_set, aliased_imports, code_minus_imports)

# remove [pkg_ns] to [target_modules] in [file_path] s.t. [pkg_ns]. == import[ : len([pkg_ns].) ]
# assume [file_path] is validly formatted typon code
# ex: pkg_name = "package1", target_modules = ['mod1', 'mod2']
def rm_pkg_ns_py(file_path, pkg_name, target_modules):
    src_code = read_src(file_path)

    sourced_imports, aliased_imports, code_minus_imports = parse_imports.split_imports_py(src_code)

    for module_name in target_modules:
        if module_name not in aliased_imports:
            # raise Exception( f'module does not exist: {module_name}' )
            continue
        # literal = "[pkg_ns]."
        if module_name[0:len(pkg_name)+1] != pkg_name + '.':
            continue

        module_alias = aliased_imports[module_name]
        del aliased_imports[module_name]
        trunc_mod_name = module_name[len(pkg_name)+1:]
        aliased_imports[trunc_mod_name] = module_alias

    for module_name in target_modules:
        if module_name not in sourced_imports:
            # raise Exception( f'module does not exist: {module_name}' )
            continue
        # literal = "[pkg_ns]."
        if module_name[0:len(pkg_name)+1] != pkg_name + '.':
            continue

        module_data = sourced_imports[module_name]
        del sourced_imports[module_name]
        trunc_mod_name = module_name[len(pkg_name)+1:]
        sourced_imports[trunc_mod_name] = module_data

    return parse_imports.join_imports_py(sourced_imports, aliased_imports, code_minus_imports)

# append [pkg_ns] to [target_modules] in [file_path]
# assume [file_path] is validly formatted typon code
# target_modules = list[ module_name ]
# map is import[module] = [pkg_ns].[import[module_name]]
def append_pkg_ns_typ(file_path, pkg_name, target_modules):
    src_code = read_src(file_path)

    include_set, aliased_imports, code_minus_imports = parse_imports.split_imports_typ(src_code)

    for module_name in target_modules:
        if module_name not in aliased_imports:
            # raise Exception( f'module does not exist: {module_name}' )
            continue
        module_alias = aliased_imports[module_name]
        del aliased_imports[module_name]
        aliased_imports[f'{pkg_name}.{module_name}'] = module_alias

    return parse_imports.join_imports_typ(include_set, aliased_imports, code_minus_imports)

# append [pkg_ns] to [target_modules] in [file_path]
# assume [file_path] is validly formatted typon code
# target_modules = list[ module_name ]
# map is import[module] = [pkg_ns].[import[module_name]]
def append_pkg_ns_py(file_path, pkg_name, target_modules):
    src_code = read_src(file_path)

    sourced_imports, aliased_imports, code_minus_imports = parse_imports.split_imports_py(src_code)

    for module_name in target_modules:
        if module_name not in aliased_imports:
            # raise Exception( f'module does not exist: {module_name}' )
            continue
        module_alias = aliased_imports[module_name]
        del aliased_imports[module_name]
        aliased_imports[f'{pkg_name}.{module_name}'] = module_alias

    for module_name in target_modules:
        if module_name not in sourced_imports:
            # raise Exception( f'module does not exist: {module_name}' )
            continue
        module_data = sourced_imports[module_name]
        del sourced_imports[module_name]
        sourced_imports[f'{pkg_name}.{module_name}'] = module_data

    return parse_imports.join_imports_py(sourced_imports, aliased_imports, code_minus_imports)

# edit import statements by absolute module references
# imports_to_add = list[ module_name, module_alias ]
# imports_to_remove = list[ module_name ]
def change_imports_typ(file_path, imports_to_add, imports_to_remove):
    src_code = read_src(file_path)

    include_set, aliased_imports, code_minus_imports = parse_imports.split_imports_typ(src_code)

    for module_name, module_alias in imports_to_add:
        aliased_imports[module_name] = module_alias

    for module_name in imports_to_remove:
        if module_name in imports_set:
            del aliased_imports[module_name]

    return parse_imports.join_imports_typ(include_set, aliased_imports, code_minus_imports)

# edit import statements by absolute module references
# imports_to_add = list[ module_name, module_alias ]
# imports_to_remove = list[ module_name ]
# assume changes to aliased_imports only
def change_imports_py(file_path, imports_to_add, imports_to_remove):
    src_code = read_src(file_path)

    sourced_imports, aliased_imports, code_minus_imports = parse_imports.split_imports_py(src_code)

    for module_name, module_alias in imports_to_add:
        aliased_imports[module_name] = module_alias

    for module_name in imports_to_remove:
        if module_name in imports_set:
            del aliased_imports[module_name]

    return parse_imports.join_imports_py(sourced_imports, aliased_imports, code_minus_imports)
