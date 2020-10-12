# -*- coding: utf-8 -*-
import os


def get_all_files(src_path, src_suffix):
    src_suffix = '.' + src_suffix
    file_paths = []
    main_name, suffix = os.path.splitext(src_path)
    if os.path.isfile(src_path) and suffix == src_suffix:
        file_dir = os.path.split(src_path)[0]
        file_paths.append({'path': src_path, 'dir': file_dir, 'name': main_name})
    elif os.path.isdir(src_path):
        for file_name in os.listdir(src_path):
            main_name, suffix = os.path.splitext(file_name)
            if suffix == src_suffix:
                file_path = os.path.join(src_path, file_name)
                file_paths.append({'path': file_path, 'dir': src_path, 'name': main_name})
    return file_paths


if __name__ == '__main__':
    print(get_all_files(r'F:\Projects\GATL', 'py'))
