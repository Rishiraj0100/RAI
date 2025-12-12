"""
RAI Project

Copyright 2025 Rishiraj0100

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
"""

import bcrypt

from tortoise import fields
from quart_auth import AuthUser
from tortoise.models import Model
from tortoise.fields import BigIntField, TextField, CharField


class User(Model, AuthUser):
    id = BigIntField(pk=True)
    
    @property
    def _auth_id(self):
        return self.id
    
    @property
    def admin(self) -> bool:
        return self.role=="admin"
    
    username = CharField(unique=True, required=True, max_length=30)
    email = CharField(unique=True, required=True, max_length=100)
    password = TextField(required=True)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    role = CharField(default="user", max_length=20)

    @classmethod
    async def create(cls, **kwargs):
        if "password" in kwargs:
            hashed = bcrypt.hashpw(kwargs["password"].encode(), bcrypt.gensalt())
            kwargs["password"] = hashed.decode()
        return await super().create(**kwargs)
    
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password.encode())

class ModelRecord(Model):
    id = BigIntField(pk=True)
    username = CharField(unique=True, required=True, max_length=100)
    name = CharField(required=True, max_length=100)
    engine = CharField(required=True, max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    owner = fields.ForeignKeyField("models.User", related_name="models", null=False)
    description = TextField(null=True)
    backstory = TextField(null=True)


class ContactForum(Model):
    id = BigIntField(pk=True)
    name = CharField(required=True, max_length=100)
    email = CharField(required=True, max_length=100)
    message = TextField(required=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    subject = CharField(null=True, max_length=200, default="No Subject")