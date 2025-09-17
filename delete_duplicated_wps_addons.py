'''
delete_duplicated_wps_addons.py
删除wps过时的插件
对比版本号: https://geek-docs.com/python/python-ask-answer/96_python_how_do_i_compare_version_numbers_in_python.html
'''

import os
import sys
import shutil
import argparse
from packaging import version

def get_newest_addon(filename_list):
    if not filename_list:
        raise ValueError('get_newest_addon(filename_list): filename_list is empty')

    newest_filename = filename_list[0]
    try:
        max_version = version.parse(newest_filename.split('_')[-1])
        for filename in filename_list[1:]:
            current_version = version.parse(filename.split('_')[-1])
            if current_version > max_version:
                max_version = current_version
                newest_filename = filename
    except version.InvalidVersion as e:
        print(f"Warning: Could not parse version for an addon. Skipping group. Error: {e}")
        # Depending on desired behavior, you might want to return the first filename
        # or handle it differently. For now, we print a warning and return the first.
        return filename_list[0]
    return newest_filename

def find_addon_path():
    """Tries to find the WPS addons path by checking common locations."""
    base_path = os.path.join(os.environ.get('APPDATA'), 'kingsoft', 'wps', 'addons')

    pool_dirs = ['pools', 'pool']
    arch_dirs = ['win-x64', 'win-i386']

    for pool in pool_dirs:
        for arch in arch_dirs:
            path = os.path.join(base_path, pool, arch)
            if os.path.exists(path):
                return path
    return None

def main():
    """Main function to find and delete old addons."""
    parser = argparse.ArgumentParser(description='Clean up old and duplicated WPS Office addons.')
    parser.add_argument('--dry-run', action='store_true', help='Print which addons would be deleted without actually deleting them.')
    parser.add_argument('-y', '--yes', action='store_true', help='Automatically answer yes to the confirmation prompt.')
    args = parser.parse_args()

    if not sys.platform.startswith('win'):
        print('This script is intended for Windows only.')
        sys.exit(1)

    addon_path = find_addon_path()
    if not addon_path:
        print('Error: Could not find the WPS addons directory.')
        sys.exit(1)

    print(f'Scanning path: {addon_path}')

    all_addons = [d for d in os.listdir(addon_path) if os.path.isdir(os.path.join(addon_path, d))]

    addons_map = {}
    for addon in all_addons:
        try:
            main_name = addon.rsplit('_', 1)[0]
            if main_name not in addons_map:
                addons_map[main_name] = []
            addons_map[main_name].append(addon)
        except IndexError:
            print(f"Warning: Could not determine main name for '{addon}'. Skipping.")
            continue

    to_delete = []
    for main_name, addon_list in addons_map.items():
        if len(addon_list) <= 1:
            continue

        newest_addon = get_newest_addon(addon_list)
        print(f"\nFound duplicates for '{main_name}':")
        print(f"  All versions: {addon_list}")
        print(f"  Newest version: {newest_addon}")

        for addon in addon_list:
            if addon != newest_addon:
                to_delete.append(addon)

    if not to_delete:
        print("\nNo old addons found to delete.")
        return

    print("\nAddons to be deleted:")
    for addon in to_delete:
        print(f"  - {addon}")

    if args.dry_run:
        print("\n--dry-run mode is active. No files will be deleted.")
        return

    if not args.yes:
        try:
            confirm = input("\nDo you want to proceed with the deletion? (y/N): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled by user.")
                return
        except KeyboardInterrupt:
            print("\nDeletion cancelled by user.")
            return

    print("\nStarting deletion...")
    for addon_to_delete in to_delete:
        print(f"  Deleting old version: {addon_to_delete}")
        try:
            shutil.rmtree(os.path.join(addon_path, addon_to_delete))
            print(f"  Successfully deleted {addon_to_delete}")
        except (OSError, PermissionError) as e:
            print(f"  Error: Could not delete {addon_to_delete}. It might be locked.")
            print(f"    Details: {e}")

if __name__ == '__main__':
    main()
