# -*- coding: utf-8 -*-
import os


def get_all_files(src_path, src_suffix):
    src_suffix = '.' + src_suffix
    file_paths = []
    if os.path.isfile(src_path) and os.path.splitext(src_path)[1] == src_suffix:
        file_paths.append(src_path)
    elif os.path.isdir(src_path):
        for file_name in os.listdir(src_path):
            suffix = os.path.splitext(file_name)[1]
            file_path = os.path.join(src_path, file_name)
            if suffix == src_suffix:
                file_paths.append(file_path)
    return file_paths


if __name__ == '__main__':
    print(get_all_files(r'F:\Projects\GATL', 'py'))
