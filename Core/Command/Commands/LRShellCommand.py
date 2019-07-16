import os
import locale
import subprocess
import shlex
import threading
from ..LRCommand import LRCommand
from ...LREnvironments import LREnvironments

class LRShellCommand(LRCommand):
    def __init__(self):
        super().__init__()
        
        self.__shell = LREnvironments.singleton().SHELL
        self.__currentIn = None
        assert len(self.__shell) > 0, 'Missing environment SHELL!'

    def input(self, input:str):
        assert self.__currentIn is not None
        toWrite = input + os.linesep
        self.__currentIn.write(bytes(toWrite, encoding=locale.getpreferredencoding()))
        self.__currentIn.flush()

    @staticmethod
    def __processOutput(p):
        while True:
            line = p.stdout.readline()
            if len(line) == 0:
                break
            line = str(line, encoding=locale.getpreferredencoding())
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            print(line)

    def getCwd(self, args):
        return '.'
    def doInput(self, args):
        raise NotImplementedError

    def execute(self, args):
        
        print('Executing...')
        p = subprocess.Popen(shlex.split(self.__shell),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        cwd=self.getCwd(args),
                        )
        t = threading.Thread(
                        target=LRShellCommand.__processOutput,
                        args=[p],
                        name='Executing '+self.myName)
        t.start()
        
        self.__currentIn = p.stdin
        self.doInput(args)
        p.stdin.close()
        
        p.wait()
        print(p.returncode)
        t.join()
