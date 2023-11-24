from fastapi import Depends
from src.settings import Settings, get_settings
from src.subscryptions.services import UserSubscryptionService
import stripe


def get_stripe(settings: Settings = Depends(get_settings)):
    stripe.api_key = settings.STRIPE_API_KEY
    return stripe

async def get_user_subscryption_service(stripe = Depends(get_stripe)):
    return UserSubscryptionService(stripe=stripe)

