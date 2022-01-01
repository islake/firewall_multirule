# Looks for executable files within a path and its subdirectories,
# then creates Windows Firewall rules to allow/block their internet access

import subprocess
import sys
import ctypes
from pathlib import Path

extension = 'exe'
action = 'block' # allow or block


def main():
    print('')

    if not ctypes.windll.shell32.IsUserAnAdmin():
        sys.exit('Error: must be running as administrator to create firewall rules.')

    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit('Error: path must be specified as an argument.')

    matches = [m for m in Path(path).glob(f'**/*.{extension}')]

    if not matches:
        sys.exit(
            f'Error: no .{extension} files found in path or subdirectories.')

    print(f'.{extension} files found:')
    for m in matches:
        m_fullpath = m.resolve()
        print(m_fullpath)
    print('')

    choice = ''
    while choice.lower() != 'y':
        choice = input(f"Create '{action}' rules in Windows Firewall (y/n)?")
        if choice.lower() == 'n':
            quit()

    for m in matches:
        m_fullpath = m.resolve()
        print(f'Creating rules for {m_fullpath}...', end='')
        try:
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule',
                           fr'name="autoadded_{action}_{m}"', 'dir=out', fr'program="{m_fullpath}"', f'action={action}'], check=True)
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule',
                           fr'name="autoadded_{action}_{m}"', 'dir=in', fr'program="{m_fullpath}"', f'action={action}'], check=True)
        except subprocess.CalledProcessError as e:
            print(e)
        print('Done.')


if __name__ == "__main__":
    main()
