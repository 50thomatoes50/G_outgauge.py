from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    #base = "Win32GUI"
    base = "Console"

executables = [
    Executable("G_outgauge.py",
               base=base,
               icon="icon.ico"
    )
]

include_files=[]
include_files.append(("LogitechLcdEnginesWrapper.dll","LogitechLcdEnginesWrapper.dll"))

buildOptions = dict(
    compressed=False,
    includes=[],
    packages=[],
    include_files=include_files,
    excludes= ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter'],
    zip_includes=[]
    
    )

setup(
    name = "G_outgauge.py",
    version = "0.1",
    description = "OutGauge python application for Logitech periperal with lcd color screen (G19)",
	options=dict(build_exe=buildOptions),
    executables = executables
)