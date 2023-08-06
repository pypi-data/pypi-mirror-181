"""
ngm
==========
License: BSD, see LICENSE for more details.
"""
import shlex
import subprocess
# get distro
import distro
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import json
import re
import os

from tabulate import tabulate

from .__about__ import __version__

# load modules by soname
modules_json = os.path.dirname(os.path.realpath(__file__)) + '/modules.json'
with open(modules_json, encoding='utf-8') as json_file:
    modules_data = json.load(json_file)


def modules_list_installed(format='console'):
    modules_dir = '/etc/nginx/modules'
    module_files = [f for f in os.listdir(modules_dir)
                    if f.endswith('.so') and not f.endswith('-debug.so')]
    # TODO add update column (have to consult RPM db)
    all_modules = [['Module ID', 'Feature Summary', 'Enabled', 'Load Directive used by "ngm enable <module id>"']]
    loaded_sonames = nginx_get_loaded_sonames()
    os_codename = None  # e.g. el7
    # get distro
    if module_files:
        import distro
        d = distro.info()
        if d['id'] in ['centos', 'rhel', 'oracle']:
            os_codename = f"el{d['version_parts']['major']}"

    for module_file in module_files:
        enabled = 'No'
        package_name = '-'
        feature_summary = ''
        url = ''
        soname = module_file.replace('.so', '')
        if soname in loaded_sonames:
            enabled = 'Yes'
        if soname in modules_data['by_soname']:
            handle = modules_data['by_soname'][soname]
            package_name = handle
            module_data = modules_data['by_handle'][handle]
            feature_summary = shorten_feature_summary(module_data['summary'])
            url = f"https://github.com/{module_data['repo']}"
            # if 'ref' in module_data and os_codename in module_data['ref']:
            #     url = module_data['ref'][os_codename]
        else:
            print(f'{soname} not in modules_data')
        all_modules.append([handle, feature_summary, enabled, f"load_module modules/{module_file};"])
    tablefmt = "github" if format == 'md' else 'psql'
    print(
        tabulate(all_modules, headers="firstrow", tablefmt=tablefmt)
    )


def shorten_feature_summary(summary):
    module_for = re.compile(re.escape('NGINX module for '), re.IGNORECASE)
    summary = module_for.sub('', summary)
    module_to = re.compile(re.escape('NGINX module to '), re.IGNORECASE)
    summary = module_to.sub('', summary)
    return summary.capitalize()


def module_list_available(format='console'):
    all_modules = [['ID', 'Feature Summary', 'Load Directive', 'Reference URL']]
    os_codename = None  # e.g. el7
    d = distro.info()
    if d['id'] in ['centos', 'rhel', 'oracle']:
        os_codename = f"el{d['version_parts']['major']}"

    for handle, module in modules_data['by_handle'].items():
        sonames = module['soname']
        if not isinstance(sonames, list):
            sonames = [sonames]
        for soname in sonames:
            feature_summary = shorten_feature_summary(module['summary'])
            url = f"https://github.com/{module['repo']}"
            if 'ref' in module and os_codename in module['ref']:
                url = module['ref'][os_codename]
            if format == 'md':
                handle = f"[{handle}]({url})"
                all_modules.append([handle, feature_summary, f"load_module modules/{soname}.so;"])
            else:
                all_modules.append([handle, feature_summary, f"load_module modules/{soname}.so;", url])

    tablefmt = "github" if format == 'md' else 'psql'
    print(
        tabulate(all_modules, headers="firstrow", tablefmt=tablefmt)
    )


def nginx_get_loaded_sonames():
    nginx_config_p = subprocess.run(['/usr/sbin/nginx', '-T'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sonames = []
    nginx_config = nginx_config_p.stdout.decode('ascii', 'ignore').splitlines()
    for line in nginx_config:
        line = line.strip()
        if line.startswith('load_module'):
            sonames.append(
                shlex.split(line)[-1].split('/')[-1].rstrip(';').split('.')[0]
            )
    return sonames


def module_enable(module_ids):
    already_enabled_sonames = nginx_get_loaded_sonames()

    enabling_modules = []

    for module_id in module_ids:
        module = modules_data['by_handle'][module_id]
        soname = module['soname']
        if isinstance(soname, list):
            soname = soname[0]
        soname_full_path = f"/etc/nginx/modules/{soname}.so"
        if soname not in already_enabled_sonames and os.path.exists(soname_full_path):
            print(f"Enabling modules/{soname}.so")
            enabling_modules.append(soname)

    nginx_conf_filename = '/etc/nginx/nginx.conf'
    nginx_conf_tmp_filename = nginx_conf_filename + '.tmp'
    # open original file in read mode and dummy file in write mode
    with open(nginx_conf_filename, 'r') as nginx_conf, open(nginx_conf_tmp_filename, 'w') as nginx_conf_tmp:
        for soname in enabling_modules:
            nginx_conf_tmp.write(f"load_module modules/{soname}.so;" + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in nginx_conf:
            if line.startswith('#') and 'load_module' in line:
                pass
            else:
                nginx_conf_tmp.write(line)
    # remove original file
    os.remove(nginx_conf_filename)
    # Rename dummy file as the original file
    os.rename(nginx_conf_tmp_filename, nginx_conf_filename)


def main():
    parser = argparse.ArgumentParser(description='CLI tool for managing NGINX configuration.',
                                     prog='ngm')

    subparsers = parser.add_subparsers(help='Command/area to run', dest="command")

    # list action is for modules only
    parser_list = subparsers.add_parser('list', help='Listing modules')
    parser_list.add_argument('kind', nargs='?', default='installed',
                             choices=['available', 'installed'],
                             help='Kind of modules to be listed')
    parser_list.add_argument('--format', nargs='?', default='console',
                             choices=['console', 'md'],
                             help='Console output or Markdown format')

    # enable action is for modules only
    parser_enable = subparsers.add_parser('enable', help='Enabling modules')
    parser_enable.add_argument('module_ids', nargs='+',
                               help='Module IDs to enable')

    parser_modules = subparsers.add_parser('modules', help='Manage dynamic NGINX modules')
    modules_subparsers = parser_modules.add_subparsers(dest='action',
                                                       help='An action for managing dynamic NGINX modules')
    # list:
    modules_list_subparser = modules_subparsers.add_parser('list', help='List modules')
    modules_list_subparser.add_argument('kind', nargs='?', default='installed',
                                        choices=['available', 'installed'],
                                        help='Kind of modules to be listed')
    # info:
    # TODO use lastversion for info about latest version
    modules_info_subparser = modules_subparsers.add_parser('info', help='Details about a module')
    modules_info_subparser.add_argument('id', choices=['pagespeed', 'nbr'],
                                        help='ID of a module to query information for')

    parser_sites = subparsers.add_parser('sites', help='Manage NGINX websites')
    sites_subparsers = parser_sites.add_subparsers(dest='action',
                                                   help='An action for managing NGINX websites')
    sites_list_subparser = sites_subparsers.add_parser('list', help='List websites')
    sites_list_subparser.add_argument('kind', nargs='?', default='enabled',
                                      choices=['available', 'enabled'],
                                      help='Kind of websites to be listed')

    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    modules_list_subparser.add_argument('--format', nargs='?', default='console',
                                        choices=['console', 'md'],
                                        help='Console output or Markdown format')

    argcomplete.autocomplete(parser)
    parser_modules.set_defaults(action='list', format='md')
    parser_sites.set_defaults(action='list')

    args = parser.parse_args()

    if args.command == 'modules' and args.action == 'list' or args.command == 'list':
        if 'kind' in args and args.kind == 'available':
            module_list_available(args.format)
        else:
            modules_list_installed(args.format)
    if args.command == 'enable':
        module_enable(args.module_ids)
