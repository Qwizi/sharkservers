import datetime
from importlib import metadata
import json
from venv import logger
from fastapi import APIRouter, Depends, Request, Security, HTTPException
from ormar import NoMatch
from src.settings import Settings, get_settings
from src.auth.dependencies import get_current_active_user
from src.logger import logger
from src.users.models import User
from src.subscryptions.dependencies import get_user_subscryption_service
from src.subscryptions.services import UserSubscryptionService
from stripe import Subscription
from stripe.error import SignatureVerificationError

router = APIRouter()


@router.get("/")
async def get_subscryption(
    user: User = Security(get_current_active_user, scopes=["users:me"]),
    user_subscryption_service: UserSubscryptionService = Depends(
        get_user_subscryption_service
    ),
):
    try:
        user_subscryption = await user_subscryption_service.Meta.model.objects.get(
            user=user, stripe_customer_id__isnull=False
        )
        stripe_session = user_subscryption_service.stripe.billing_portal.Session.create(
            customer=user_subscryption.stripe_customer_id,
            return_url="http://localhost:3000/settings/subscription",
        )
        return {"url": stripe_session.url}
    except NoMatch:
        stripe_session = user_subscryption_service.stripe.checkout.Session.create(
            success_url="http://localhost:3000/settings",
            cancel_url="http://localhost:3000/settings",
            payment_method_types=["card"],
            mode="subscription",
            billing_address_collection="auto",
            customer_email=user.email,
            line_items=[
                {
                    "price_data": {
                        "currency": "PLN",
                        "product_data": {
                            "name": "Konto VIP",
                            "description": "Konto vip",
                        },
                        "unit_amount": 1000,
                        "recurring": {"interval": "month"},
                    },
                    "quantity": 1,
                }
            ],
            metadata={"user_id": user.id},
        )
        return {"url": stripe_session.url}

    except Exception as e:
        logger.info(e)


@router.post("/webhook")
async def get_webhook(
    req: Request,
    user_subscryption_service: UserSubscryptionService = Depends(
        get_user_subscryption_service
    ),
    settings: Settings = Depends(get_settings)
):
    payload = await req.body()
    sig_header = req.headers.get('Stripe-Signature')
    event = None
    _stripe = user_subscryption_service.stripe
    try:
        event = _stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        logger.info(e)
        raise HTTPException(status=400)
    
    except SignatureVerificationError as e:
        logger.info(e)
        # Invalid signature
        raise HTTPException(400, "Cannot validate signature")

    

    if event["type"] == "checkout.session.completed":
        session = event.data.object
        logger.info(f"Sessja {session}")
        subscryption: Subscription = _stripe.checkout.Session.retrieve(event['data']['object']['id'])
        if not "user_id" in session["metadata"]:
            raise HTTPException(400, "user_id is required")

        await user_subscryption_service.create(
            user__id=session["metadata"]["user_id"],
            stripe_subscription_id=subscryption.get("subscryption"),
            stripe_customer_id=subscryption.get("customer"),
            stripe_price_id=subscryption["lines"]["data"][0]["price"]["id"],
            stripe_current_period_end=datetime.fromtimestamp(
                subscryption.get("current_period_end") * 1000
            ),
        )

    elif event["type"] == "invoice.payment_succeeded":
        session = event.data.object
        subscryption: Subscription = _stripe.checkout.Session.retrieve(event['data']['object']['id'])

        user_subscryption = await user_subscryption_service.get_one(
            stripe_subscription_id=subscryption.get("subscryption")
        )
        await user_subscryption.update(
            stripe_price_id=subscryption["lines"]["data"][0]["price"]["id"],
            stripe_current_period_end=datetime.fromtimestamp(
                subscryption["current_period_end"] * 1000
            ),
        )
    return {}
