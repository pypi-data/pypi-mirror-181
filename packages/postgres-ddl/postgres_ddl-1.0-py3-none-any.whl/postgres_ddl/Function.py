#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL

class Function(DDL):
    def __init__(self, parent, data, config):
        super().__init__(parent, data, config)

        self.Oid = (data.get("oid") or 0)
        assert self.Oid > 0, \
            "Function oid is null"

        self.Schema = (data.get("schema") or "").strip()
        assert len(self.Schema) > 0, \
            "Function schema is null"

        self.Name = (data.get("proc") or "").strip()
        assert len(self.Name) > 0, \
            "Function name is null"

        self.ArgsInTypes = (data.get("args_in_types") or "").strip()

        self.NameWithParams = f"{self.Schema}.{self.Name}({self.ArgsInTypes})"

        self.ArgsIn = (data.get("args_in") or "").strip()

        self.ArgsOut = (data.get("args_out") or "").strip()

        self.Cost = data.get("cost") or 0

        self.Rows = data.get("rows") or 0

        self.Language = (data.get("lang") or "").strip()
        assert len(self.Language) > 0, \
            "Function language is null"

        self.Volatility = (data.get("volatility") or "").strip()
        assert len(self.Volatility) > 0, \
            "Function volatility"

        self.HasDuplicate = data.get("has_duplicate") or False
        self.IsTrigger = data.get("is_trigger") or False

        self.Code = (data.get("code") or "").strip()
        assert len(self.Code) > 0, \
            "Function code is null"

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.NameWithParams,
                "owner_name"    : data.get("owner")
            },
            self.Config
        )

        self.Comment = Comment(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.NameWithParams,
                "comment"       : data.get("comment")
            },
            self.Config
        )

        self.Grants = []
        for grant in ParseACL(data.get("acl"), self.Owner.Owner):
            grant["instance_type"] = self.GetTag()
            grant["instance_name"] = self.NameWithParams
            self.Grants.append(Grant(self.GetObjectName(), grant, self.Config))

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "function"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        if self.HasDuplicate:
            return f"{self.Schema}.{self.Name}({self.ArgsInTypes}).sql"
        else:
            return f"{self.Schema}.{self.Name}"

    def GetTag(self):
        return "FUNCTION"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.Schema}.{self.Name}({self.ArgsInTypes});"

    def DDL_ArgsIn(self):
        if len(self.ArgsIn or "") == 0:
            return "()" + self.NewLine(1)
        else:
            args = self.ArgsIn.replace(",", f",{self.NewLine(1)}   ")
            r = ""
            r += "("
            r += self.NewLine(1)
            r += f"    {args}"
            r += self.NewLine(1)
            r += ")"
            r += self.NewLine(1)
            return r

    def DDL_Create(self):
        r = f"-- Function: {self.Schema}.{self.Name}({self.ArgsInTypes})"
        r += self.NewLine(2)
        r += f"-- {self.DDL_Drop()}"
        r += self.NewLine(2)
        r += f"CREATE OR REPLACE {self.GetTag()} {self.Schema}.{self.Name}"
        r += self.DDL_ArgsIn()
        r += f"RETURNS {self.ArgsOut} AS"
        r += self.NewLine(1)
        r += "$BODY$"
        r += self.NewLine(1)
        r += self.Code
        r += self.NewLine(1)
        r += "$BODY$"
        r += self.NewLine(1)
        r += f"{self.Indent()}LANGUAGE {self.Language} {self.Volatility}"

        if self.Cost > 0:
            r += self.NewLine(1)
            r += f"{self.Indent()}COST {int(self.Cost)}"

        if self.Rows > 0:
            r += self.NewLine(1)
            r += f"{self.Indent()}ROWS {int(self.Rows)}"

        r += ";"
        r += self.NewLine(2)
        r += self.Owner.DDL_Create()
        r += self.NewLine(2)

        for grant in self.Grants:
            r += grant.DDL_Create()
            r += self.NewLine(1)
        r += self.NewLine(1)

        if self.Comment.IsExists:
            r += self.Comment.DDL_Create()
            r += self.NewLine(1)

        return r.strip() + self.NewLine(1)

    def GetPath(self):
        return [self.Schema, "triggers" if self.IsTrigger else "functions"]

    def GetFileName(self):
        if self.HasDuplicate:
            return f"{self.Name}({self.ArgsInTypes}).sql"
        else:
            return f"{self.Name}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Comment.GetObjectName()] = self.Comment
        result[self.Owner.GetObjectName()] = self.Owner
        for g in self.Grants:
            result[g.GetObjectName()] = g
        return result

    def Diff(self, another):
        if (
            self.ArgsIn     != another.ArgsIn     or
            self.ArgsOut    != another.ArgsOut    or
            self.Code       != another.Code       or
            self.Cost       != another.Cost       or
            self.Language   != another.Language   or
            self.Rows       != another.Rows       or
            self.Volatility != another.Volatility
        ):
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]
        else:
            return []
