import os
import sys
import lib_code.parse_imports as parse_imports

def read_src(file_path):
    fp = open(file_name, 'r')
    src_code = fp.read()
    fp.close()
    return src_code


def rm_pkg_ns_typ(file_path, pkg_name, target_modules):
    src_code = read_src(file_path)
    include_set, aliased_imports, code_minus_imports = parse_imports.split_imports_typ(src_code)
    for module_name in target_modules:
        if module_name not in aliased_imports:
            continue
        if module_name[0:len(pkg_name)+1] != pkg_name + '.':
            continue
        module_alias = aliased_imports[module_name]
        del aliased_imports[module_name]
        trunc_mod_name = module_name[len(pkg_name)+1:]
        aliased_imports[trunc_mod_name] = module_alias
    return parse_imports.join_imports_typ(include_set, aliased_imports, code_minus_imports)


def rm_pkg_ns_py(file_path, pkg_name, target_modules):
    src_code = read_src(file_path)
    sourced_imports, aliased_imports, code_minus_imports = parse_imports.split_imports_py(src_code)
    for module_name in target_modules:
        if module_name not in aliased_imports:
            continue
        if module_name[0:len(pkg_name)+1] != pkg_name + '.':
            continue
        module_alias = aliased_imports[module_name]
        del aliased_imports[module_name]
        trunc_mod_name = module_name[len(pkg_name)+1:]
        aliased_imports[trunc_mod_name] = module_alias
    for module_name in target_modules:
        if module_name not in sourced_imports:
            continue
        if module_name[0:len(pkg_name)+1] != pkg_name + '.':
            continue
        module_data = sourced_imports[module_name]
        del sourced_imports[module_name]
        trunc_mod_name = module_name[len(pkg_name)+1:]
        sourced_imports[trunc_mod_name] = module_data
    return parse_imports.join_imports_py(sourced_imports, aliased_imports, code_minus_imports)


def append_pkg_ns_typ(file_path, pkg_name, target_modules):
    src_code = read_src(file_path)
    include_set, aliased_imports, code_minus_imports = parse_imports.split_imports_typ(src_code)
    for module_name in target_modules:
        if module_name not in aliased_imports:
            continue
        module_alias = aliased_imports[module_name]
        del aliased_imports[module_name]
        aliased_imports[f'{pkg_name}.{module_name}'] = module_alias
    return parse_imports.join_imports_typ(include_set, aliased_imports, code_minus_imports)


def append_pkg_ns_py(file_path, pkg_name, target_modules):
    src_code = read_src(file_path)
    sourced_imports, aliased_imports, code_minus_imports = parse_imports.split_imports_py(src_code)
    for module_name in target_modules:
        if module_name not in aliased_imports:
            continue
        module_alias = aliased_imports[module_name]
        del aliased_imports[module_name]
        aliased_imports[f'{pkg_name}.{module_name}'] = module_alias
    for module_name in target_modules:
        if module_name not in sourced_imports:
            continue
        module_data = sourced_imports[module_name]
        del sourced_imports[module_name]
        sourced_imports[f'{pkg_name}.{module_name}'] = module_data
    return parse_imports.join_imports_py(sourced_imports, aliased_imports, code_minus_imports)


def change_imports_typ(file_path, imports_to_add, imports_to_remove):
    src_code = read_src(file_path)
    include_set, aliased_imports, code_minus_imports = parse_imports.split_imports_typ(src_code)
    for module_name, module_alias in imports_to_add:
        aliased_imports[module_name] = module_alias
    for module_name in imports_to_remove:
        if module_name in imports_set:
            del aliased_imports[module_name]
    return parse_imports.join_imports_typ(include_set, aliased_imports, code_minus_imports)


def change_imports_py(file_path, imports_to_add, imports_to_remove):
    src_code = read_src(file_path)
    sourced_imports, aliased_imports, code_minus_imports = parse_imports.split_imports_py(src_code)
    for module_name, module_alias in imports_to_add:
        aliased_imports[module_name] = module_alias
    for module_name in imports_to_remove:
        if module_name in imports_set:
            del aliased_imports[module_name]
    return parse_imports.join_imports_py(sourced_imports, aliased_imports, code_minus_imports)
