# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bobalkkagi']

package_data = \
{'': ['*'], 'bobalkkagi': ['dumpfiles/*', 'log/*']}

install_requires = \
['capstone>=4.0.2,<5.0.0',
 'distorm3>=3.5.2,<4.0.0',
 'fire>=0.4,<0.5',
 'lief>=0.12.2',
 'pefile>=2022.5.30,<2023.0.0',
 'pyinstaller>=5.7.0,<6.0.0',
 'unicorn>=2.0.1.post,<3.0.0']

entry_points = \
{'console_scripts': ['bobalkkagi = bobalkkagi.application:main']}

setup_kwargs = {
    'name': 'bobalkkagi',
    'version': '0.2.0',
    'description': 'Unpack and unwrapping executables protected with Themida 3.1.3 by BOB11_Bobalkkagi',
    'long_description': "# TEAM Bobalkkagi\n\nBOB11 project\n\nUnpacking & Unwrapping & Devirtualization(Not yet) of Themida 3.1.3 packed program(Tiger red64)\n\n### API Hook\n\nHooking API based win10_v1903  \n\n## How to\n\n### Install\n\n```\npip install bobalkkagi\n```\n**or**\n\n```\npip install git+https://github.com/hackerhoon/bobalkkagi.git\n```\n\n### Notes\n\nNeed default Dll folder(win10_v1903) or you can give dll folder path\n\nwin10_v1903 folder is in https://github.com/hackerhoon/bobalkkagi\n\n### Use\n```\nNAME\n    bobalkkagi\n\nSYNOPSIS\n    bobalkkagi PROTECTEDFILE <flags>\n\nPOSITIONAL ARGUMENTS\n    PROTECTEDFILE\n        Type: str\n\nFLAGS\n    --mode=MODE\n        Type: str\n        Default: 'f'\n    --verbose=VERBOSE\n        Type: str\n        Default: 'f'\n    --dllPath=DLLPATH\n        Type: str\n        Default: 'win10_v1903'\n    --oep=OEP\n        Type: str\n        Default: 't'\n    --debugger=DEBUGGER\n        Type: str\n        Default: 'f'\n\nNOTES\n    You can also use flags syntax for POSITIONAL ARGUMENTS\n\n```\n\n### Option Description\n---\n\n\n#### Mode: f[fast], c[hook_code], b[hook_block]\n--- \n\nDescription: Mean emulating mode, we implement necessary api to unpack protected excutables by themida 3.1.3. \n\nRunning on **fast mode** compare rip with only hook API function area size 32(0x20), but **hook_block mode** and **hook_code mode** compare rip with all mapped DLL memory (min 0x1000000) to check functions. block mode emulate block size(call, jmp) code mode do it opcode by opcode.\n\n#### verbose\n---\n\n**verbose** show Loaded DLL on memory, we will update it to turn on/off HOOKING API CALL info.\n\n#### dllPath\n---\n\n**dllPath** is directory where DLLs to load on memory exists. DLLs are different for each window version. \nThis tool may be not working with your window DLL path(C:\\Windows\\System32)\n\n#### oep\n---\n\n**oep** is option to find original entry point. If you turn off this option, you can emulate program after oep**(fast mode can't do it, it works on hook_block and hook_code)**\n\n#### debugger\n---\n\nIf you want unpack another protector or different version of themida, you should add necessary hook_api functions(anti debugging, handle, syscall). you can analyze protected program hook_code mode or hook_block mode(more detail in https://github.com/unicorn-engine/unicorn) with **debugger ** option**(working only hook_code mode!)**\n\n\n\n\n\n",
    'author': 'hackerhoon',
    'author_email': 'gkswlgns21@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
