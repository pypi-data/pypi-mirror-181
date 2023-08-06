#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL

class ForeignTable(DDL):
    def __init__(self, parent, data, config):
        super().__init__(parent, data, config)

        self.Schema = (data.get("schema_name") or "").strip().lower()
        assert len(self.Schema) > 0, \
            "Foreign table schema is null"

        self.Name = (data.get("table_name") or "").strip().lower()
        assert len(self.Name) > 0, \
            "Foreign table name is null"

        self.Server = (data.get("server_name") or "").strip()
        assert len(self.Server) > 0, \
            "Foreign table server is null"

        self.Options = data.get("options")

        self.Columns = data.get("columns_list") or []
        assert len(self.Columns) > 0, \
            "Foreign table columns is null"

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.GetFullName(),
                "owner_name"    : data.get("owner_name")
            },
            self.Config
        )

        self.Comment = Comment(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.GetFullName(),
                "comment"       : data.get("comment")
            },
            self.Config
        )

        self.Grants = []
        for grant in ParseACL(data.get("acl"), self.Owner.Owner):
            grant["instance_type"] = "TABLE"
            grant["instance_name"] = self.GetFullName()
            self.Grants.append(Grant(self.GetObjectName(), grant, self.Config))

    def __str__(self):
        return self.Name

    def GetObjectType(self):
        return "foreign_server"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Name}"

    def GetTag(self):
        return "FOREIGN TABLE"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- Foreign Table: {self.GetFullName()}"
        r += self.NewLine(2)
        r += f"-- {self.DDL_Drop()}"
        r += self.NewLine(2)
        r += f"CREATE {self.GetTag()} {self.GetFullName()}("
        r += self.NewLine(1)
        r += self.DDL_Columns()
        r += self.NewLine(1)
        r += ")"
        r += self.NewLine(1)
        r += f"SERVER {self.Server}"
        r += self.NewLine(1)
        r += "OPTIONS("
        r += self.NewLine(1)
        r += self.DDL_Options()
        r += self.NewLine(1)
        r += ");"
        r += self.NewLine(2)

        if self.Owner.Owner is not None:
            r += self.Owner.DDL_Create()
            r += self.NewLine(2)

        for grant in self.Grants:
            r += grant.DDL_Create()
            r += self.NewLine(1)

        if self.Comment.IsExists:
            r += self.NewLine(1)
            r += self.Comment.DDL_Create()

        return r.strip() + self.NewLine(1)

    def DDL_Options(self):
        result = []

        for o in sorted(self.Options):
            o = o.split("=")
            if len(o) != 2:
                continue
            result.append(f"{self.Indent()}{o[0]} '{o[1]}'")

        return f",{self.NewLine(1)}".join(result)

    def DDL_Columns(self):
        result = []
        for col in self.Columns:
            result.append(f"{self.Indent()}{col}")
        return f",{self.NewLine(1)}".join(result)

    def GetPath(self):
        return [self.Schema, "foreign_table"]

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
