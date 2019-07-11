'''
LocalRunner

LocalRunner is a Python3 lib that provide a tool with GUI.
Users can add a serias commands (predefined or customized), and trigger these commands by GUI.
'''

from .Console.LRCmd import LRCmd

def runConsole():
    cmd = LRCmd()
    cmd.initialize()
    cmd.run()

'''
from .LRApp import LRApp
from .Commands.LRCBase import LRCBase
from .Commands.LRCFactory import LRCFactory
from .UI.AttrEditor.AWFactory import AWFactory

def registerCustomLRC(lrcClass):
    pass

def registerCustomAW(awClass):
    pass

def runUI(workingDir:Path=Path(os.getcwd())):
    assert workingDir.exists(), 'workingDir is NOT existant!'
    assert workingDir.is_dir(), 'workingDir is NOT a directory!'

    currentApp = LRApp(workingDir)
    currentApp.exec()
'''