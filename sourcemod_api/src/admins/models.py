from email.policy import default
from typing import Optional
import ormar
from pydantic import BaseModel

from src.db import BaseMeta, DateFieldsMixins
from src.admins.enums import AuthTypeEnum, GroupOverrideAccessEnum, GroupOverrideTypeEnum


class Group(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "sm_groups"

    id: int = ormar.Integer(primary_key=True)
    flags: Optional[str] = ormar.String(max_length=30)
    name: Optional[str] = ormar.String(max_length=65)
    immunity_level: Optional[int] = ormar.Integer()


class GroupImmunity(ormar.Model):
    class Meta(BaseMeta):
        tablename = "sm_group_immunity"

    id: int = ormar.Integer(primary_key=True)
    group_id: Optional[int] = ormar.Integer()
    other_id: Optional[int] = ormar.Integer()


class GroupOverride(ormar.Model):
    class Meta(BaseMeta):
        tablename = "sm_group_overrides"

    id: int = ormar.Integer(primary_key=True)
    group: Optional[Group] = ormar.ForeignKey(Group, name="group_id")
    type: Optional[str] = ormar.String(
        max_length=7, choices=list(GroupOverrideTypeEnum), default=GroupOverrideTypeEnum.GROUP.value
    )
    name: Optional[str] = ormar.String(max_length=32)
    access: Optional[str] = ormar.String(
        max_length=5, choices=list(GroupOverrideAccessEnum), default=GroupOverrideAccessEnum.DENY.value
    )

class AdminGroup(ormar.Model):
    class Meta(BaseMeta):
        tablename = "sm_admins_groups"

    id: int = ormar.Integer(primary_key=True)
    inherit_order: Optional[int] = ormar.Integer(default=0)


class Admin(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "sm_admins"

    id: int = ormar.Integer(primary_key=True)
    authtype: Optional[str] = ormar.String(
        max_length=5, choices=list(AuthTypeEnum), default=AuthTypeEnum.STEAM.value
    )
    identity: Optional[str] = ormar.String(max_length=65, unique=True)
    password: Optional[str] = ormar.String(max_length=65, nullable=True)
    flags: Optional[str] = ormar.String(max_length=30)
    name: Optional[str] = ormar.String(max_length=65)
    immunity: Optional[str] = ormar.Integer()
    groups: Optional[Group] = ormar.ManyToMany(
        Group,
        through_relation_name="admin_id",
        through_reverse_relation_name="group_id",
        through=AdminGroup,
    )


class Override(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "sm_overrides"

    id: int = ormar.Integer(primary_key=True)
    type: Optional[str] = ormar.String(max_length=64)
    name: Optional[str] = ormar.String(max_length=32)
    flags: Optional[str] = ormar.String(max_length=30)


class Config(ormar.Model):
    class Meta(BaseMeta):
        tablename = "sm_config"

    id: int = ormar.Integer(primary_key=True)
    cfg_key: Optional[str] = ormar.String(max_length=64)
    cfg_value: Optional[str] = ormar.String(max_length=64)