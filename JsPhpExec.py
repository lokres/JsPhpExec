# -*- coding: utf-8 -*-
# @Author: user
# @Date:   2020-05-31 22:10:07
# @Last Modified by:   Lokres
# @Last Modified time: 2020-06-01 18:58:58


import sublime
import sublime_plugin
import subprocess
import re
import os
import tempfile
from tempfile import NamedTemporaryFile
class JsPhpExec(sublime_plugin.TextCommand):
    def run(self, edit):

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
            cmd = re.sub(r'\n\s*{', r'{', cmd)
            cmd = re.sub(r'\n\s*([^\s{])', r';\1', cmd)

            res = subprocess.check_output(['node', '--eval', cmd, '--print'], startupinfo=startupinfo).decode('UTF-8')
        elif(extension == '.php'):

            fd, path = tempfile.mkstemp()
            cmd = '<?php \n;'+cmd;
            cmd = re.sub(r'([^;]+);*\s*$', r'print_R( \1 );', cmd)
            with open(path, 'w') as f:
              f.write(cmd)
            res = subprocess.check_output(['php', '-f', path], startupinfo=startupinfo).decode('UTF-8')
            os.close(fd)
            os.remove(path)
        else:
            return False;

            # cmd = re.sub(r'\n', r'', cmd)
            # cmd = re.sub(r'([^;]+);$', r'return \1', cmd)
            # cmd = "print_r(eval('"+cmd+";'));"
            # res = subprocess.check_output(['php', '-r', cmd], startupinfo=startupinfo).decode('UTF-8')
        self.view.show_popup(res)
