import cx_Freeze
from cx_Freeze import bdist_msi
# from cx_Freeze import *
import sys
includefiles=['icon.ico','icons2','vpad.py']
base=None
if sys.platform=="win32":
    base="Win32GUI"

shortcut_table=[
    ("DesktopShortcut",
     "DesktopFolder",
     "Vpad Editor",
     "TARGETDIR",
     "[TARGETDIR]\vpad.exe",
     None,
     None,
     None,
     None,
     None,
     None,
     "TARGETDIR",
     )
]
msi_data={"Shortcut":shortcut_table}

bdist_msi_options={'data':msi_data}
cx_Freeze.setup(
    version="0.1",
    description="Snake Game",
    author="Hari Singh",
    name="Snake Game",
    options={'build_exe':{'include_files':includefiles},'bdist_msi':bdist_msi_options,},
    executables=[
        cx_Freeze.Executable(
            script="vpad.py",
            base=base,
            icon='icon.ico',
        )
    ]
)
