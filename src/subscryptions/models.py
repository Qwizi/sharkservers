import datetime
from enum import unique
import uuid
import ormar

from src.db import BaseMeta, DateFieldsMixins
from src.users.models import User

class UserSubscription(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "user_subscription"

    id: str = ormar.UUID(primary_key=True, default=uuid.uuid4)
    user: User = ormar.ForeignKey(User)
    stripe_customer_id: str = ormar.String(unique=True, max_length=255)
    stripe_subscription_id: str = ormar.String(unique=True, max_length=255)
    stripe_price_id: str = ormar.String(max_length=255)
    stripe_current_period_end: datetime.datetime = ormar.DateTime()