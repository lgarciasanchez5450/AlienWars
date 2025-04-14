if __name__ != '__main__': raise BaseException
import sys
import os
import subprocess as sp
import shutil

MIN_PYINSTALLER_VERSION = 6,11,0
try:
    if (proc := sp.run(['pyinstaller','-v'],capture_output=True)).returncode == 0:
        version = tuple(map(int,proc.stdout.decode().split('.')))
        if version < MIN_PYINSTALLER_VERSION:
            print(f'Minimum Pyinstaller Version: {MIN_PYINSTALLER_VERSION} | Current {proc.stdout.decode()}')
            sys.exit(1)
    else:
        raise FileNotFoundError
except FileNotFoundError:
    print('Missing Dependency "Pyinstaller" (install with "pip install pyinstaller")')
    sys.exit(1)

try:
    action = sys.argv[1]
except IndexError:
    action = 'make'


if action == 'clean':
    try:shutil.rmtree('./dist')
    except:pass
    try:shutil.rmtree('./build')
    except:pass
    try:os.remove('game.spec')
    except:pass

elif action == 'make':
    print('Building Executable (Pyinstaller)')
    proc = sp.run(['pyinstaller','game.py','--onefile','--optimize','2'],capture_output=True,text=True)
    if proc.returncode != 0:
        print("Pyinstaller Error:")
        print(proc.stderr or '')
        sys.exit(1)
    print('Successfully Built Executable')
    try:
        os.replace('dist/game.exe','game.exe')
    except FileNotFoundError:
        print("Error Moving Executable. Check dist/game.exe for executable")
        sys.exit(1)
else:
    raise SyntaxError



sys.exit(0)

