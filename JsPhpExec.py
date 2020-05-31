# -*- coding: utf-8 -*-
# @Author: user
# @Date:   2020-05-31 22:10:07
# @Last Modified by:   Lokres
# @Last Modified time: 2020-05-31 23:34:25


import sublime
import sublime_plugin
import subprocess
import re
class JsPhpExec(sublime_plugin.TextCommand):
    def run(self, edit):

        view = self.view
        sel = view.sel()
        text = sel[0]
        cmd = view.substr(text)

        import re
        cmd = re.sub(r'\n\s*{', r'{', cmd).lower()
        cmd = re.sub(r'\n\s*([^\s{])', r';\1', cmd)

        res = subprocess.check_output(['node', '--eval', cmd, '--print'], shell=True).decode('UTF-8')
        self.view.show_popup(res)
