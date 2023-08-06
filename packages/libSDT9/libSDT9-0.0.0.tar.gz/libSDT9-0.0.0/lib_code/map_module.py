import os, json

def bfs_files(base_dir, target_exts):
    target_exts_map = { x : 1 for x in target_exts }
    q = [base_dir]
    result = []
    while len(q) > 0:
        fspath = q.pop()
        if os.path.isdir(fspath):
            for file in os.listdir(fspath):
                q.append( f'{fspath}/{file}' )
            continue
        i1 = fspath.rfind('.', 0)
        ext = fspath[i1+1 : len(fspath) ]
        if ext in target_exts_map or len(target_exts) == 0:
            result.append(fspath)
    return result


def transforms( base_dir, target_exts ):
    abs_fspaths = bfs_files(base_dir, target_exts)
    rel_fspaths = [ x[len(base_dir)+1:] for x in abs_fspaths ]
    file_names = [ x[ x.rfind('/', 0) + 1 : ] for x in abs_fspaths ]
    return [ abs_fspaths, rel_fspaths, file_names ]


def read_imports(src_fspath):
    fp = open(src_fspath, 'r')
    fsource = fp.read()
    fp.close()
    lines = fsource.splitlines()
    index = len(lines)
    for i in range(0, len(lines)):
        line = lines[i]
        if len(line) > 0 and line[0] == '#':
            continue
        if line[0:7] != 'import ':
            index = i
            break
    import_list = []
    imports = lines[0:index]
    for line in imports:
        if len(line) > 0 and line[0] == '#':
            continue
        S1 = line[7:]
        L1 = [ x.strip() for x in S1.split(',')  ]
        import_list += [
                    x.strip() for x in import_seg.split(' as ')
                    for import_seg in L1
                ]
    return lines, index, import_list


def transform_imports(src_fspath, dst_fspath, src_pkg_name, dst_pkg_name, module_correspondence):
    fp = open(src_fspath, 'r')
    fsource = fp.read()
    fp.close()
    lines = fsource.splitlines()
    index = len(lines)
    lines, index, import_list = read_imports(src_fspath)
    revised_imports = []
    for L2 in import_list:
        if len(L2) == 1:
            revised_imports.append( f'import {L2[0]}' )
            continue
        if L2[0] not in module_correspondence:
            e_msgs_L1 = [
                            f'uncontained module collection',
                            f'mapping for package: {L2[0]} is undefined',
                        ]
            e_msg = '\n'.join(e_msgs_L1)
            raise Exception( e_msg )
        revised_imports.append( f'import {module_correspondence[L2[0]]} as {L2[1]}' )
    dst_repr = '\n'.join( revised_imports + lines[index:] )
    fp = open(dst_fspath, 'w')
    fp.write(dst_repr)
    fp.close()


def check_transform(module_space_map):
    module_paths = [
            [ x[ x.rfind('/', 0) + 1 : ], x ]
            for module_name in module_space_map
            for x in module_space_map[module_name]
        ]
    unq_file_names = {}
    unq_rel_fspaths = {}
    for file_name, rel_path in module_paths:
        if file_name in unq_file_names:
            print( file_name )
        if rel_path in unq_rel_fspaths:
            print( rel_path )
        unq_file_names[file_name] = 1
        unq_rel_fspaths[rel_path] = 1
    b1 = len( unq_rel_fspaths ) == len( module_paths )
    b2 = len( unq_file_names ) == len( module_paths )
    print( b1 )
    print( b2 )


def compute_module_correspondence( src_pkg_name, dst_pkg_name, module_transform ):
    result = {}
    L1 = [ x for module_name in module_transform for x in module_transform[module_name] ]
    result_values = {}
    for dst_module_name in module_transform:
        for rel_path in module_transform[dst_module_name]:
            I1 = rel_path.rfind('/', 0) + 1
            X1 = rel_path[ I1 : ]
            if X1[-3:] == '.py':
                X1 = X1[:-3]
            src_module_name = rel_path[ : I1-1 ].replace('/', '.')
            src_mod = f'{src_pkg_name}.{src_module_name}.{X1}'
            dst_mod = f'{dst_pkg_name}.{dst_module_name}.{X1}'
            if src_mod in result:
                e_msgs_L1 = [
                                    f'given module_mapping is not injective',
                                    f'{src_mod} is not uniquely defined',
                                ]
                e_msg = '\n'.join(e_msgs_L1)
                raise Exception( e_msg )
            if dst_mod in result_values:
                e_msgs_L1 = [
                                    f'given module_mapping is not surjective',
                                    f' F[{result_values[dst_mod]}] = F[{src_mod}] = {dst_mod}',
                                ]
                e_msg = '\n'.join(e_msgs_L1)
                raise Exception( e_msg )
            result[ src_mod ] = dst_mod
            result_values[ dst_mod ] = src_mod
    return result


def build_base_pkgs( dst_base_dir, module_transform ):
    for dst_pkg in module_transform:
        dst_fmt = dst_pkg.replace('.', '/')
        pkg_dir = f'{dst_base_dir}/{dst_fmt}'
        pkg_init = f'{dst_base_dir}/{dst_fmt}/__init__.py'
        if not os.path.isdir(pkg_dir):
            os.mkdir(pkg_dir)
        if os.path.exists(pkg_init):
            continue
        file_repr = ''
        fp = open(pkg_init, 'w')
        fp.write(file_repr)
        fp.close()


def assert_module_closure(src_base, dst_base, module_correspondence):
    src_rel = src_mod.replace('.', '/')
    dst_rel = module_correspondence[src_mod].replace('.', '/')
    src_fspath = f'{src_base}/{src_rel}.py'
    dst_fspath = f'{dst_base}/{dst_rel}.py'
    lines, index, import_list = read_imports(src_fspath)
    revised_imports = []
    for L2 in import_list:
        if len(L2) > 1 and L2[0] not in module_correspondence:
            e_msgs_L1 = [
                            f'uncontained module collection',
                            f'mapping for package: {L2[0]} is undefined',
                        ]
            e_msg = '\n'.join(e_msgs_L1)
            raise Exception( e_msg )


def eval_map( src_base, dst_base, src_pkg_name, dst_pkg_name, module_mapping ):
    dst_base_dir = f'{dst_base}/{dst_pkg_name}'
    build_base_pkgs( dst_base_dir, module_mapping )
    module_correspondence = compute_module_correspondence( src_pkg_name, dst_pkg_name, module_mapping )
    assert_module_closure(src_base, dst_base, module_correspondence)
    for src_mod in module_correspondence:
        src_rel = src_mod.replace('.', '/')
        dst_rel = module_correspondence[src_mod].replace('.', '/')
        src_fspath = f'{src_base}/{src_rel}.py'
        dst_fspath = f'{dst_base}/{dst_rel}.py'
        transform_imports(src_fspath, dst_fspath, src_pkg_name, dst_pkg_name, module_correspondence)
