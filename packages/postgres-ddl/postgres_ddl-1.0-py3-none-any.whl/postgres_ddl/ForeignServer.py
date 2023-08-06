#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL

class ForeignServer(DDL):
    def __init__(self, parent, data, config):
        super().__init__(parent, data, config)

        self.Schema = "_foreign"

        self.Name = (data.get("server_name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "Foreign server name is null"

        self.FDW = (data.get("fdw_name") or "").strip().lower()
        assert len(self.FDW) > 0, \
            "Foreign server FDW is null"

        self.Options = data.get("options")

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : "SERVER",
                "instance_name" : self.Name,
                "owner_name"    : data.get("owner_name")
            },
            self.Config
        )

        self.Comment = Comment(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.Name,
                "comment"       : data.get("comment")
            },
            self.Config
        )

        self.Grants = []
        for grant in ParseACL(data.get("acl"), self.Owner.Owner):
            grant["instance_type"] = self.GetTag()
            grant["instance_name"] = self.Name
            self.Grants.append(Grant(self.GetObjectName(), grant, self.Config))

    def __str__(self):
        return self.Name

    def GetObjectType(self):
        return "foreign_server"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.Name}"

    def GetTag(self):
        return "FOREIGN SERVER"

    def DDL_Drop(self):
        return f"DROP SERVER IF EXISTS {self.Name};"

    def DDL_Create(self):
        r = f"-- Server: {self.Name}"
        r += self.NewLine(2)
        r += f"-- {self.DDL_Drop()}"
        r += self.NewLine(2)
        r += f"CREATE SERVER {self.Name}"
        r += self.NewLine(1)
        r += f"FOREIGN DATA WRAPPER {self.FDW}"
        r += self.NewLine(1)
        r += "OPTIONS("
        r += self.NewLine(1)
        r += self.DDL_Options()
        r += self.NewLine(1)
        r += ");"
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

    def DDL_Options(self):
        result = []

        for o in sorted(self.Options):
            o = o.split("=")
            if len(o) != 2:
                continue
            result.append(f"{self.Indent()}{o[0]} = '{o[1]}'")

        return f",{self.NewLine(1)}".join(result)

    def GetPath(self):
        return [self.Schema]

    def GetFileName(self):
        return f"{self.Name}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Comment.GetObjectName()] = self.Comment
        result[self.Owner.GetObjectName()] = self.Owner
        for v in self.Grants:
            result[v.GetObjectName()] = v
        return result
