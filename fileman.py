# -*- coding: utf-8 -*-
import os
import shutil


def get_all_files(src_path, src_suffix):
    file_paths = {'dir': {}, 'file': []}
    fp_no_sfx, suffix = os.path.splitext(src_path)
    if os.path.isfile(src_path) and suffix.lower() in src_suffix:
        file_dir, file_name = os.path.split(src_path)
        dir_name = os.path.split(file_dir)[1]
        main_name = os.path.split(fp_no_sfx)[1]
        file_paths['dir'] = {'path': file_dir, 'name': dir_name}
        file_paths['file'].append({'path': src_path, 'fname': file_name, 'mname': main_name, 'suffix': suffix})
    elif os.path.isdir(src_path):
        dir_name = os.path.split(src_path)[1]
        file_paths['dir'] = {'path': src_path, 'name': dir_name}
        for file_name in os.listdir(src_path):
            main_name, suffix = os.path.splitext(file_name)
            if suffix.lower() in src_suffix:
                file_path = os.path.join(src_path, file_name)
                file_paths['file'].append({'path': file_path, 'fname': file_name, 'mname': main_name, 'suffix': suffix})
    return file_paths


def get_ruled_files(src_dirs, src_suffixs, rule):
    if len(src_dirs) < 2:
        return None
    file_paths = {'dirix': [], 'mname': []}
    main_names = []
    for src_dir, src_suffix in zip(src_dirs, src_suffixs):
        file_paths['dirix'].append({'dir': src_dir, 'suffix': src_suffix})
        main_names.append([os.path.splitext(x)[0] for x in os.listdir(src_dir) if os.path.splitext(x)[1] == src_suffix])
    file_paths['mname'] = main_names[0]
    rule_operation = 'file_paths["'"mname"'"] = list(set(file_paths["'"mname"'"]).' + rule + '(main_name))'
    for main_name in main_names:
        exec(rule_operation)
    return file_paths


def copy_files(src_paths, dst_dir):
    for src_path in src_paths:
        dst_path = os.path.join(dst_dir, src_path['fname'])
        shutil.copyfile(src_path['path'], dst_path)


if __name__ == '__main__':
    print(get_all_files(r'F:\Projects\Win10\GATL', ['.py']))
    exit(0)
