# apps services
import random
import string

from ormar import pre_save
from sharkservers.apps.exceptions import apps_not_found_exception
from sharkservers.apps.models import App
from sharkservers.db import BaseService


class AppService(BaseService):
    class Meta:
        model = App
        not_found_exception = apps_not_found_exception

    @staticmethod
    def generate_random_string(length: int):
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )

    @staticmethod
    def generate_client_id():
        return AppService.generate_random_string(16)

    @staticmethod
    def generate_client_secret():
        return AppService.generate_random_string(50)


@pre_save(App)
def generate_client_id_and_secret(sender, instance, **kwargs):
    instance.client_id = AppService.generate_client_id()
    instance.client_secret = AppService.generate_client_secret()
    instance.secret_key = AppService.generate_random_string(32)
