# -*- coding: utf-8 -*-
import os


def get_all_files(src_path, src_suffix):
    file_paths = {'dir': {}, 'file': []}
    fp_no_sfx, suffix = os.path.splitext(src_path)
    if os.path.isfile(src_path) and suffix.lower() in src_suffix:
        file_dir = os.path.split(src_path)[0]
        dir_name = os.path.split(file_dir)[1]
        main_name = os.path.split(fp_no_sfx)[1]
        file_paths['dir'] = {'path': file_dir, 'name': dir_name}
        file_paths['file'].append({'path': src_path, 'name': main_name, 'suffix': suffix})
    elif os.path.isdir(src_path):
        dir_name = os.path.split(src_path)[1]
        file_paths['dir'] = {'path': src_path, 'name': dir_name}
        for file_name in os.listdir(src_path):
            main_name, suffix = os.path.splitext(file_name)
            if suffix.lower() in src_suffix:
                file_path = os.path.join(src_path, file_name)
                file_paths['file'].append({'path': file_path, 'name': main_name, 'suffix': suffix})

    return file_paths


if __name__ == '__main__':
    print(get_all_files(r'F:\Projects\Win10\GATL', ['.py']))
