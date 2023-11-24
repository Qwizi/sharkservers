
from typing import Optional
from pydantic import BaseModel
from src.admins.enums import AuthTypeEnum, GroupOverrideAccessEnum, GroupOverrideTypeEnum
from src.admins.models import Admin, Group, GroupOverride


admin_out =  Admin.get_pydantic()
group_out = Group.get_pydantic()
group_override_out = GroupOverride.get_pydantic()

class AdminOut(admin_out):
    pass

class GroupOut(group_out):
    pass


class GroupOverrideOut(group_override_out):
    pass

class CreateAdminSchema(BaseModel):
    authtype: Optional[AuthTypeEnum]
    identity: str
    password: Optional[str]
    flags: str = "abcdefghijklmnzopqrst"
    name: str
    immunity: int
    groups_id: Optional[list[int]]

class UpdateAdminSchema(BaseModel):
    authtype: Optional[AuthTypeEnum]
    identity: Optional[str]
    password: Optional[str]
    flags: Optional[str]
    name: Optional[str]
    immunity: Optional[int]
    groups_id: Optional[list[int]]


class CreateGroupSchema(BaseModel):
    name: str
    immunity_level: int
    flags: str = "abcdefghijklmnzopqrst"


class CreateGroupOverrideSchema(BaseModel):
    group_id: int
    type: GroupOverrideTypeEnum
    name: str
    access: GroupOverrideAccessEnum