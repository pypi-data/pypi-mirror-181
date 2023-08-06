#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config():
    Indent = " " * 2
    NL = chr(10)

    @staticmethod
    def Parse(json):
        Config.Indent = " " * (json.get("indent") or 2)
        Config.NL = json.get("new_line") or chr(10)
