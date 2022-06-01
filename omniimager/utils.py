import os
import subprocess
import sys
import yaml

CHECKSUM_TYPES = ['sha256sum', 'md5sum']
TO_BE_CHECKED_KEYS = ['working_dir', 'installer_configs', 'systemd_configs', 'init_script', 'installer_script',
                      'repo_file', 'cached_rootfs_gz', 'log_dir']


def format_path(path):
    path = path.replace(' ', '')
    sep = path[-1]
    if sep == '/':
        path = path[0:len(path) - 1]
    return path


def format_filename(filename):
    filename = filename.replace(' ', '')
    if '/' in filename:
        print(f"Your filename is '{filename}', but filename could not contains '/', exit.")
        sys.exit(1)
    return filename


def parse_config_file(config_file):
    if not os.path.exists(config_file):
        print(f"Cloud not find your config file {config_file}, exit")
        sys.exit(1)
    with open(config_file, 'r') as config_file:
        config_options = yaml.load(config_file, Loader=yaml.SafeLoader)
    for key, value in config_options.items():
        if key in TO_BE_CHECKED_KEYS:
            config_options[key] = format_path(value)
    return config_options


def create_checksum_file(config_options, working_dir, image_name):
    checksum_type = config_options.get('checksum_type', 'sha256sum')
    if checksum_type.lower() not in CHECKSUM_TYPES:
        print('No checksum type you selected... Use default type: sha256sum ')
        checksum_type = 'sha256sum'
    origin_path = os.getcwd()
    os.chdir(working_dir)
    checksum_name = f'{image_name}.{checksum_type}'
    subprocess.run(f'{checksum_type} {image_name} > {checksum_name} ', shell=True)
    print('Generate checksum file successfully.')
    os.chdir(origin_path)
