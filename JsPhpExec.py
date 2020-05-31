# -*- coding: utf-8 -*-
# @Author: user
# @Date:   2020-05-31 22:10:07
# @Last Modified by:   user
# @Last Modified time: 2020-05-31 22:42:01


import sublime
import sublime_plugin
import subprocess

class JsPhpExec(sublime_plugin.TextCommand):
    def run(self, edit):

        view = self.view
        sel = view.sel()
        text = sel[0]
        cmd = view.substr(text)
        res = subprocess.check_output(['node', '-e', cmd, '--print'], shell=True).decode('UTF-8')
        self.view.show_popup(res)
