from src.db import BaseService
from src.subscryptions.models import UserSubscription
from src.subscryptions.exceptions import subscryption_not_found


class UserSubscryptionService(BaseService):
    class Meta:
        model = UserSubscription
        not_found_exception = subscryption_not_found

    def __init__(self, stripe):
        self.stripe = stripe