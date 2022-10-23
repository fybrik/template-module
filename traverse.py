import glob
import os
from jinja2 import Template, Environment, FileSystemLoader, TemplateNotFound
from distutils.dir_util import copy_tree
from shutil import rmtree
import json

def validate_files(paths):
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    for path in paths:
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                if not is_binary_string(f.read(1024)):
                    yield path


def fill_template(paths, config):
    e = Environment(variable_start_string='@{{', variable_end_string='}}', loader=FileSystemLoader("."))
    for path in paths:
        template = e.get_template(path)
        filled = template.render(config)
        yield path, filled


def write_file(files):
    for file in files:
        path, content = file
        with open(path, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    with open("config.json", "r") as f:
        temaplte_config = json.load(f)

    tmp_dir_path = "./tmp/"
    copy_tree("./template-files/", tmp_dir_path)
    files = glob.iglob(tmp_dir_path + "**/*", recursive=True)
    write_file(fill_template(validate_files(files), temaplte_config))
    copy_tree(tmp_dir_path, ".")
    rmtree(tmp_dir_path)
    print('\033[92m'+"Module generated successfully!"+'\033[0m')
    print("Delete redundant template files with:")
    print("rm -r template-files traverse.py config.json")