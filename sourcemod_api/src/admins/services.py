
from fastapi import HTTPException
from src.db import BaseService
from src.admins.models import Admin, Group, GroupOverride
from src.admins.schemas import CreateAdminSchema, UpdateAdminSchema


admin_not_found_exception = HTTPException(
    status_code=404,
    detail="Admin not found",
)

group_not_found_exception = HTTPException(
    status_code=404,
    detail="Group not found",
)

class AdminService(BaseService):
    
    class Meta:
        model = Admin
        not_found_exception = admin_not_found_exception


    async def _create(self, data: CreateAdminSchema, groups_list: list[Group] | None):
        data_dict = data.dict()
        group_id = data_dict.pop("groups_id", None)
        new_admin = await self.create(**data_dict)
        if groups_list:
            for group in groups_list:
                await new_admin.groups.add(group)
        return new_admin
    
    async def _update(self, admin: Admin, updated_data: UpdateAdminSchema, groups_list: list[Group] | None):
        data_dict = updated_data.dict(exclude_none=True)
        group_id = data_dict.pop("groups_id", None)
        if admin.identity == updated_data.identity:
            identity = data_dict.pop("identity")
        await admin.update(**data_dict)
        if groups_list:
            for group in admin.groups:
                await admin.groups.remove(group)
            
            for group in groups_list:
                await admin.groups.add(group)

        return admin



class GroupService(BaseService):
    
    class Meta:
        model = Group
        not_found_exception = group_not_found_exception


class GroupOverrideService(BaseService):
    class Meta:
        model = GroupOverride
        not_found_exception = group_not_found_exception