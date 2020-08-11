# -*- coding: utf-8 -*-
# @Author: user
# @Date:   2020-05-31 22:10:07
# @Last Modified by:   root
# @Last Modified time: 2020-08-11 10:30:20


import sublime
import sublime_plugin
import subprocess
import re
import os
import tempfile
from tempfile import NamedTemporaryFile

class JsPhpExec(sublime_plugin.TextCommand):
    def run(self, edit):
        print(os.name)
        if (os.name == "posix"):
            self.linux(self)
        elif (os.name == 'nt'):
            self.dos(self)


    @staticmethod
    def linux(self):
        dirName = os.path.dirname(self.view.file_name())
        settings = sublime.load_settings('JsPhpExec.sublime-settings')
        tempName = 'execTemp';
        path = dirName+'/execTemp';
        bas = open(path, 'tw', encoding='utf-8')
        print(self.view.file_name())

        extension = os.path.splitext(self.view.file_name())[1]

        view = self.view

        sel = self.view.sel()
        text = sel[0]
        cmd = view.substr(text)



        if(extension == '.js'):
            execPath = settings.get('node')
            cmd = ';\n'+cmd;
            cmd = re.sub(r'\n([^\n]+)\s*$', r';console.log( \1 );', cmd)

            fd, path = tempfile.mkstemp()
            with open(path, 'w') as f:
              f.write(cmd)

            res = subprocess.check_output(['cd', dirName, '&', execPath, '-f', path], startupinfo=startupinfo).decode('UTF-8')
            os.close(fd)
            os.remove(path)
        elif(extension == '.php'):
            execPath = settings.get('php')
            cmd = '<?php \n;'+cmd;
            cmd = re.sub(r'([^;]+);*\s*$', r'print_R( \1 );', cmd)
            bas.write(cmd)

            print(['cd', dirName, '&', execPath, tempName])
            res = subprocess.check_output(['cd', dirName, '&', execPath, '-f', path], startupinfo=startupinfo).decode('UTF-8')
            print(res)
            #
            #os.close(fd)
            os.remove(path)
        else:
            return False;

        self.view.show_popup(res)



    @staticmethod
    def dos(self):
        dirName = os.path.dirname(self.view.file_name())+'\\'
        settings = sublime.load_settings('JsPhpExec.sublime-settings')
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= (
            subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
        )
        startupinfo.wShowWindow = subprocess.SW_HIDE

        view = self.view

        sel = view.sel()
        text = sel[0]
        cmd = view.substr(text)
        extension = os.path.splitext(view.file_name())[1]

        if(extension == '.js'):
            execPath = settings.get('node')
            cmd = ';\n'+cmd;
            cmd = re.sub(r'\n([^\n]+)\s*$', r';console.log( \1 );', cmd)

            fd, path = tempfile.mkstemp()
            with open(path, 'w') as f:
              f.write(cmd)

            res = subprocess.check_output(['cmd', '/c' , 'cd', dirName, '&', execPath, path], startupinfo=startupinfo).decode('UTF-8')
            os.close(fd)
            os.remove(path)
        elif(extension == '.php'):
            execPath = settings.get('php')
            fd, path = tempfile.mkstemp()
            cmd = '<?php \n;'+cmd;
            cmd = re.sub(r'([^;]+);*\s*$', r'print_R( \1 );', cmd)
            with open(path, 'w') as f:
              f.write(cmd)
            print('cd', dirName, '&', execPath, '-f', path)
            res = subprocess.check_output(['cmd', '/c' , 'cd', dirName, '&', execPath, '-f', path], startupinfo=startupinfo).decode('UTF-8')
            os.close(fd)
            os.remove(path)
        else:
            return False;

        self.view.show_popup(res)


    @staticmethod
    def execute_command(command, working_dir=None):
        startupinfo = None
        # hide console window on windows
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        output = None
        try:
            output = subprocess.check_output(
                command,
                cwd=working_dir,
                startupinfo=startupinfo
            )
        except (subprocess.CalledProcessError, AttributeError):
            # Git will return an error when the given directory
            # is not a repository, which means that we can ignore this error
            pass
        else:
            output = str(output, encoding="utf-8").strip()

        return output
