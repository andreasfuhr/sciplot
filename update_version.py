import argparse
import pathlib
import re


VERSION_REGEX_STR = r'[0-9]+\.[0-9]+\.[0-9]+'
VERSION_V_REGEX_STR = r'v[0-9]+\.[0-9]+\.[0-9]+'

IN_FILE_VERSION_REGEX_DICT = {
    'changes': {
        'file_name': 'CHANGES.txt'
    },
    'version': {
        'file_name': 'VERSION',
        'version_prefix': '',
        'version_suffix': ''
    },
    'readme': {
        'file_name': 'README.md',
        'version_prefix': r'{',
        'version_suffix': r'}'
    },
    'setup': {
        'file_name': 'setup.py',
        'version_prefix': r"version='",
        'version_suffix': "'"
    },
}


def version_regex_type(arg_value, pat=re.compile(VERSION_REGEX_STR)):
    if not pat.match(arg_value):
        alt_version_val = re.compile(VERSION_V_REGEX_STR)
        if alt_version_val.match(arg_value):
            arg_value = arg_value[1:]
        else:
            raise argparse.ArgumentTypeError
    return arg_value


def check_changes(file_path, file_type_dict, version_new):
    with open(file_path, 'r') as file:
        content = file.read()

    result_lst = re.findall(version_new, content)
    if version_new not in result_lst:
        raise ValueError(
            "Changes list " + file_type_dict['file_name'] + " not updated for version '" +
            version_new + "'.")

    print('Checked version in ' + file_type_dict['file_name'])


def update_file(file_path, file_type_dict, version_new):
    with open(file_path, 'r') as file:
        content = file.read()

    content_new = re.sub(
        file_type_dict['version_prefix'] + VERSION_REGEX_STR + file_type_dict['version_suffix'],
        file_type_dict['version_prefix'] + version_new + file_type_dict['version_suffix'],
        content,
        flags=re.M
    )

    with open(file_path, 'w') as file:
        file.write(content_new)

    print("Updated version in " + file_type_dict['file_name'] + " to '" + version_new + "'")


def main(version_new):
    # Get all files in directory .
    file_path_lst = [str(p.absolute()) for p in pathlib.Path('.').iterdir() if p.is_file()]

    for file_type in ['changes', 'version', 'readme', 'setup']:
        file_type_dict = IN_FILE_VERSION_REGEX_DICT[file_type]
        for file_path in file_path_lst:
            if file_type == 'changes' and file_path.endswith(file_type_dict['file_name']):
                check_changes(file_path, file_type_dict, version_new)
                continue

            if file_path.endswith(file_type_dict['file_name']):
                update_file(file_path, file_type_dict, version_new)
                continue


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        '-v',
        '--version',
        type=version_regex_type,
        help='Semantic version, e.g. 1.2.3 or v1.2.3',
        required=True
    )
    ARGS = PARSER.parse_args()

    main(ARGS.version)
