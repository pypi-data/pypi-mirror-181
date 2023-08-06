#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config():
    def __init__(self, json):
        self.Indent = " " * (json.get("indent") or 2)
        self.NewLine = json.get("new_line") or chr(10)
