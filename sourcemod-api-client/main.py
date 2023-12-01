import asyncio
from sourcemod_api_client import APIConfig
from sourcemod_api_client.services.async_adminss_service import adminss_get_admins

async def main():

    api_config = APIConfig(base_path="http://localhost:8081/")

    ## get all admins
    admins = await adminss_get_admins(api_config_override=api_config)

    print(admins)


if __name__ == "__main__":
    asyncio.run(main())