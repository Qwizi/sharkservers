#!/bin/bash
# This script generates a module with the given name
# and creates the necessary files and directories
# for the module to be used in the project.
# Usage: ./generate-module.sh <module-name>
module_name=$1
module_name_uppercase=$(echo "$module_name" | sed 's/\(.\)/\u\1/')
module_name_full_uppercase=$(echo "$module_name" | sed 's/\(.\)/\u\1/g')

# Check if the module name was given
if [ -z "$module_name" ]; then
    echo "Usage: ./generate-module.sh <module-name>"
    exit 1
fi

# Create the module directory
mkdir -p src/"$module_name"

# Create init.py, dependencies.py, schemas.py, tests files
touch src/"$module_name"/__init__.py src/"$module_name"/dependencies.py src/"$module_name"/schemas.py tests/"$module_name"_test.py tests/"$module_name"_admin_test.py
# Create enums.py file
module_exception_name="${module_name_uppercase}ExceptionEnum"
module_event_name="${module_name_uppercase}EventsEnum"
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

# Create views.py file
cat > src/"$module_name"/views.py << EOF
# $1 views
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello from $1 module"}



EOF

# Create views_admin.py file
cat > src/"$module_name"/views_admin.py << EOF
# $1 admin views
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def admin_index():
    return {"message": "Hello from $1 module"}



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

# Create exceptions.py file
module_exception_instance_name="${module_name}_not_found_exception"

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
module_service_name="${module_name_uppercase}Service"
cat > src/"$module_name"/services.py << EOF
# $1 services
from src.db import BaseService
from src.${module_name}.models import ${module_name_uppercase}
from src.${module_name}.exceptions import ${module_exception_instance_name}


class ${module_service_name}(BaseService):
    pass


${module_name}_service = ${module_service_name}(model=${module_name_uppercase}, not_found_exception=${module_exception_instance_name})

EOF