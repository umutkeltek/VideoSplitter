from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    'packages': ['PyQt5', 'moviepy'],
    'excludes': ['tkinter'],
    'optimize': 2
}

setup(
    name='VideoSplitter',
    version='0.1',
    description='Video Splitter Application',
    options={'build_exe': build_exe_options},
    executables=[Executable('video_splitter.py', base=base)]
)
