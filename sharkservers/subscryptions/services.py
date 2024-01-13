from sharkservers.db import BaseService
from sharkservers.subscryptions.exceptions import subscryption_not_found
from sharkservers.subscryptions.models import UserSubscription


class UserSubscryptionService(BaseService):
    class Meta:
        model = UserSubscription
        not_found_exception = subscryption_not_found

    def __init__(self, stripe):
        self.stripe = stripe
