#!/bin/bash
# This script generates a module with the given name
# and creates the necessary files and directories
# for the module to be used in the project.
# Usage: ./generate-module.sh <module-name>

module_name=$1
module_name_uppercase=$(echo "$module_name" | sed 's/\(.\)/\u\1/')
module_name_full_uppercase=$(echo "$module_name" | sed 's/\(.\)/\u\1/g')
module_service_name="${module_name_uppercase}Service"
module_service_instance_name="${module_name}_service"
module_exception_name="${module_name_uppercase}ExceptionEnum"
module_event_name="${module_name_uppercase}EventsEnum"
module_exception_instance_name="${module_name}_not_found_exception"
module_schema_out_name="${module_name_uppercase}Out"
module_create_schema_name="Create${module_name_uppercase}Schema"
module_update_schema_name="Update${module_name_uppercase}Schema"
module_get_valid_name="get_valid_${module_name}"
# Check if the module name was given
if [ -z "$module_name" ]; then
    echo "Usage: ./generate-module.sh <module-name>"
    exit 1
fi

# Create the module directory
mkdir -p src/"$module_name"

# Create init.py, dependencies.py files
touch src/"$module_name"/__init__.py src/"$module_name"/dependencies.py
# Create enums.py file
cat > src/"$module_name"/enums.py << EOF
# $1 enums
from enum import Enum


class ${module_exception_name}(str, Enum):
    NOT_FOUND = "${module_name_uppercase} not found"


class ${module_event_name}(str, Enum):
    """R${module_name_uppercase} events enum."""

    GET_ALL = "${module_name_full_uppercase}_GET_ALL"
    GET_ONE = "${module_name_full_uppercase}_GET_ONE"
    CREATE = "${module_name_full_uppercase}_CREATE"
    UPDATE = "${module_name_full_uppercase}_UPDATE"
    DELETE = "${module_name_full_uppercase}_DELETE"
    ADMIN_GET_ALL = "${module_name_full_uppercase}_ADMIN_GET_ALL"
    ADMIN_GET_ONE = "${module_name_full_uppercase}_ADMIN_GET_ONE"
    ADMIN_CREATE = "${module_name_full_uppercase}_ADMIN_CREATE"
    ADMIN_UPDATE = "${module_name_full_uppercase}_ADMIN_UPDATE"
    ADMIN_DELETE = "${module_name_full_uppercase}_ADMIN_DELETE"



EOF

# Create exceptions.py file

cat > src/"$module_name"/exceptions.py << EOF
# $1 exceptions
from fastapi import status
from fastapi.exceptions import HTTPException
from src.${module_name}.enums import ${module_exception_name}


${module_exception_instance_name} = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=${module_exception_name}.NOT_FOUND,
)



EOF

# Create services.py file
cat > src/"$module_name"/services.py << EOF
# $1 services
from src.db import BaseService
from src.${module_name}.models import ${module_name_uppercase}
from src.${module_name}.exceptions import ${module_exception_instance_name}


class ${module_service_name}(BaseService):
    pass


${module_name}_service = ${module_service_name}(model=${module_name_uppercase}, not_found_exception=${module_exception_instance_name})

EOF

# create schemas.py file
cat > src/"$module_name"/schemas.py << EOF
# $1 schemas
from pydantic import BaseModel
from src.${module_name}.models import ${module_name_uppercase}


${module_schema_out_name} = ${module_name_uppercase}.get_pydantic()


class ${module_create_schema_name}(BaseModel):
    pass


class ${module_update_schema_name}(BaseModel):
    pass


EOF

# Create models.py file
cat > src/"$module_name"/models.py << EOF
# $1 models
import ormar
from src.db import BaseMeta


class ${module_name_uppercase}(ormar.Model):
    class Meta(BaseMeta):
        tablename = "${module_name}s"

    id: int = ormar.Integer(primary_key=True)


EOF

# Create dependencies.py file
cat > src/"$module_name"/dependencies.py << EOF
# $1 dependencies
from src.${module_name}.models import ${module_name_uppercase}
from src.${module_name}.services import ${module_service_instance_name}


async def ${module_get_valid_name}(${module_name}_id: int) -> ${module_name_uppercase}:
    """
    Get valid ${module_name}
    :param ${module_name}_id:
    :return ${module_name_uppercase}:
    """
    return await ${module_service_instance_name}.get_one(id=${module_name}_id)


EOF
# Create me.py file
cat > src/"$module_name"/views.py << EOF
# $1 views
from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage

from src.auth.dependencies import get_current_active_user
from src.users.models import User


from src.${module_name}.schemas import ${module_schema_out_name}, ${module_create_schema_name}, ${module_update_schema_name}
from src.${module_name}.services import ${module_service_instance_name}
from src.${module_name}.models import ${module_name_uppercase}
from src.${module_name}.enums import ${module_event_name}
from src.${module_name}.dependencies import ${module_get_valid_name}

router = APIRouter()


@router.get("", response_model_exclude_none=True)
async def get_${module_name}s(params: Params = Depends()) -> AbstractPage:
    """
    Get ${module_name}s
    :param params:
    :return AbstractPage:
    """
    ${module_name}s = await ${module_service_instance_name}.get_all(params=params)
    dispatch(event_name=${module_event_name}.GET_ALL, payload={"data": ${module_name}s })
    return ${module_name}s


@router.get("/{${module_name}_id}", response_model_exclude_none=True)
async def get_${module_name}(${module_name}: ${module_name_uppercase} = Depends(${module_get_valid_name})) -> ${module_schema_out_name}:
    """
    Get ${module_name}
    :param ${module_name}_id:
    :param ${module_name}:
    :return ${module_name_uppercase}:
    """
    dispatch(event_name=${module_event_name}.GET_ONE, payload={"data": ${module_name}})
    return ${module_name}

@router.post("")
async def create_${module_name}(
    ${module_name}_data: ${module_create_schema_name},
    user: User = Security(get_current_active_user, scopes=["${module_name}:create"]),
) -> ${module_schema_out_name}:
    """
    Create new ${module_name}.
    :param ${module_name}_data:
    :param user:
    :return:
    """
    new_${module_name} = await ${module_service_instance_name}(**${module_name}_data.dict())
    dispatch(${module_event_name}.CREATE, payload={"data": new_${module_name}})
    return new_${module_name}


@router.put("/{${module_name}_id}")
async def update_${module_name}(
    ${module_name}_data: ${module_update_schema_name},
    ${module_name}: ${module_name_uppercase} = Depends(${module_get_valid_name}),
    user: User = Security(get_current_active_user, scopes=["${module_name}:update"]),

) -> ${module_schema_out_name}:
    """
    Update ${module_name} by id.
    :param ${module_name}_data:
    :param ${module_schema_out_name}:
    :return:
    """
    updated_${module_name} = await ${module_name}.update(**${module_name}_data.dict(exclude_unset=True))
    dispatch(${module_event_name}.UPDATE, payload={"data": updated_${module_name}})
    return updated_${module_name}

EOF

# Create servers.py file
cat > src/"$module_name"/views_admin.py << EOF
# $1 admin views
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def admin_index():
    return {"message": "Hello from $1 module"}



EOF