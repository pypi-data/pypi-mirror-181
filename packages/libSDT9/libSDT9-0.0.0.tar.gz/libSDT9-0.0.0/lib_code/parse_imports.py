
def split_imports_py(src_code):
    lines = src_code.splitlines()
    import_lines = []
    break_index = -1
    for i in range(0, len(lines)):
        if len(lines[i]) == 0 or lines[i][0] == '#':
            continue
        if lines[i][0:7] != 'import ' and lines[i][0:5] != 'from ':
            break_index = i
            break
        import_lines.append(lines[i])
    sourced_imports = {}
    aliased_imports = {}
    for import_line in import_lines:
        if import_line[0:7] == 'import ':
            L1 = [
                            [ z.strip() for z in y.strip().split(' as ') ]
                            for y in x.lstrip()[7:].strip().split(',')
                        ]
            for L2 in L1:
                if len(L2) == 1:
                    aliased_imports[L2[0]] = L2[0]
                    continue
                assert len(L2) == 2
                aliased_imports[L2[0]] = L2[1]
                continue
            continue
        if import_line[0:5] == 'from ':
            L0 = [
                            x.strip()
                            for x in import_line[5:].strip().split(' import ')
                        ]
            assert len(L0) == 2
            module_name = L0[0]
            L1 = [
                            [ z.strip() for z in y.strip().split(' as ') ]
                            for y in L0[1].split(',')
                        ]
            sourced_imports[module_name] = {}
            for L2 in L1:
                if len(L2) == 1:
                    sourced_imports[module_name][L2[0]] = L2[0]
                    continue
                sourced_imports[module_name][L2[0]] = L2[1]
                continue
            continue
    code_minus_imports_L1 = lines[break_index:]
    code_minus_imports = '\n'.join(code_minus_imports_L1)
    return sourced_imports, aliased_imports, code_minus_imports


def split_imports_typ(src_code):
    lines = src_code.splitlines()
    import_lines = []
    break_index = -1
    for i in range(0, len(lines)):
        if len(lines[i]) == 0 or lines[i][0] == '#':
            continue
        if lines[i][0:6] != 'import' and lines[i][0:7] != 'include':
            break_index = i
            break
        import_lines.append(lines[i])
    include_set = {
            x.lstrip()[8:].strip() : 1
            for x in import_lines
            if x.lstrip()[0:8] == 'include '
        }
    aliased_imports = {
            module_name : module_alias
            for x in import_lines
            if x.lstrip()[0:7] == 'import '
            for module_name, module_alias in [
                [
                    y.strip()
                    for y in x.lstrip()[7:].strip().split(' as ')
                ]
            ]
        }
    code_minus_imports_L1 = lines[break_index:]
    code_minus_imports = '\n'.join(code_minus_imports_L1)
    return include_set, aliased_imports, code_minus_imports


def join_imports_py(sourced_imports, aliased_imports, code_minus_imports):
    import_repr_L1 = [
            f'from {module_name} import {module_item} as {module_alias}'
            for module_name in sourced_imports
            for module_item in sourced_imports[module_name]
            for module_alias in [ sourced_imports[module_name][module_item] ]
        ] + [
            f'import {module_name} as {module_alias}'
            for module_name in aliased_imports
            for module_alias in [ aliased_imports[module_name] ]
        ]
    import_repr = '\n'.join(import_repr_L1)
    return f'''
    {import_repr}
    {code_minus_imports}
    '''


def join_imports_typ(include_set, aliased_imports, code_minus_imports):
    import_repr_L1 = [
            f'include {c_ext_name}'
            for c_ext_name in include_set
        ] + [
            f'import {module_name} as {module_alias}'
            for module_name in aliased_imports
            for module_alias in [ aliased_imports[module_name] ]
        ]
    import_repr = '\n'.join(import_repr_L1)
    return f'''
    {import_repr}
    {code_minus_imports}
    '''
