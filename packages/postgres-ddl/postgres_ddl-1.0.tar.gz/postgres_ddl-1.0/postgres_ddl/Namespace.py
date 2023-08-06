
#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL

class Namespace(DDL):
    def __init__(self, parent, data, config):
        super().__init__(parent, data, config)

        self.Oid = data.get("oid")
        assert (self.Oid or 0) > 0, \
            "Namespace oid is null"

        self.Name = (data.get("name") or "").strip()
        assert len(self.Name) > 0, \
            "Namespace name is null"

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.GetFullName(),
                "owner_name"    : data.get("owner")
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
            grant["instance_type"] = self.GetTag()
            grant["instance_name"] = self.GetFullName()
            self.Grants.append(Grant(self.GetObjectName(), grant, self.Config))

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "schema"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return self.Name

    def GetTag(self):
        return "SCHEMA"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- Schema: {self.GetFullName()}"
        r += self.NewLine(2)
        r += f"-- {self.DDL_Drop()}"
        r += self.NewLine(2)
        r += f"CREATE {self.GetTag()} {self.GetFullName()};"
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
        return [self.GetFullName()]

    def GetFileName(self):
        return f"{self.GetFullName()}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Comment.GetObjectName()] = self.Comment
        result[self.Owner.GetObjectName()] = self.Owner
        for g in self.Grants:
            result[g.GetObjectName()] = g
        return result
