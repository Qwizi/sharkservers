import datetime
from venv import logger

from fastapi import APIRouter, Depends, HTTPException, Request, Security
from ormar import NoMatch
from sharkservers.auth.dependencies import get_current_active_user
from sharkservers.logger import logger
from sharkservers.roles.dependencies import get_roles_service
from sharkservers.roles.enums import ProtectedDefaultRolesEnum
from sharkservers.roles.services import RoleService
from sharkservers.settings import Settings, get_settings
from sharkservers.subscryptions.dependencies import get_user_subscryption_service
from sharkservers.subscryptions.services import UserSubscryptionService
from sharkservers.users.dependencies import get_users_service
from sharkservers.users.models import User
from sharkservers.users.services import UserService
from stripe import Subscription
from stripe.error import SignatureVerificationError

router = APIRouter()


@router.get("/")
async def get_subscryption(
    user: User = Security(get_current_active_user, scopes=["users:me"]),
    user_subscryption_service: UserSubscryptionService = Depends(
        get_user_subscryption_service,
    ),
):
    try:
        user_subscryption = await user_subscryption_service.Meta.model.objects.get(
            user=user,
            stripe_customer_id__isnull=False,
        )

        if user_subscryption.stripe_subscription_id is None:
            stripe_session = user_subscryption_service.stripe.checkout.Session.create(
                customer=user_subscryption.stripe_customer_id,
                success_url="http://localhost:3000/settings",
                cancel_url="http://localhost:3000/settings",
                payment_method_types=["card"],
                mode="subscription",
                billing_address_collection="auto",
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
                    },
                ],
                metadata={"user_id": user.id},
            )
            return {"url": stripe_session.url}
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
                },
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
        get_user_subscryption_service,
    ),
    users_service: UserService = Depends(get_users_service),
    roles_service: RoleService = Depends(get_roles_service),
    settings: Settings = Depends(get_settings),
):
    payload = await req.body()
    sig_header = req.headers.get("Stripe-Signature")
    event = None
    _stripe = user_subscryption_service.stripe
    try:
        event = _stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        logger.info(e)
        raise HTTPException(status=400)

    except SignatureVerificationError as e:
        logger.info(e)
        # Invalid signature
        raise HTTPException(400, "Cannot validate signature")

    except Exception as e:
        logger.info(e)
        raise HTTPException(400)

    if event["type"] == "checkout.session.completed":
        session = event.data.object
        subscryption: Subscription = _stripe.Subscription.retrieve(
            session.get("subscription"),
        )
        logger.info(subscryption)
        if "user_id" not in session["metadata"]:
            raise HTTPException(400, "user_id is required")
        user_id = int(session["metadata"]["user_id"])
        user = await users_service.Meta.model.objects.get(pk=user_id)
        timestamp = subscryption.get(
            "current_period_end",
        )  # Assuming you have a Unix timestamp
        current_period_end_datetime = datetime.datetime.fromtimestamp(timestamp)
        old_display_role = user.display_role
        vip_role = await roles_service.Meta.model.objects.get(
            pk=ProtectedDefaultRolesEnum.VIP.value,
        )

        if old_display_role.id == vip_role.id:
            old_display_role = await roles_service.Meta.model.objects.get(
                pk=ProtectedDefaultRolesEnum.USER.value,
            )

        await user.update(display_role=vip_role)
        new_user_subscryption = await user_subscryption_service.create(
            user=user,
            stripe_subscription_id=subscryption.get("id"),
            stripe_customer_id=subscryption.get("customer"),
            stripe_price_id=subscryption["items"]["data"][0]["price"]["id"],
            stripe_current_period_end=current_period_end_datetime,
            old_display_role=old_display_role,
        )

        logger.info(new_user_subscryption)

    elif event["type"] == "invoice.payment_succeeded":
        session = event.data.object
        logger.info("User znowil subscrybcje")
        subscryption: Subscription = _stripe.Subscription.retrieve(
            session.get("subscription"),
        )

        user_subscryption = await user_subscryption_service.get_one(
            stripe_customer_id=subscryption.get("customer"),
        )
        timestamp = subscryption.get(
            "current_period_end",
        )  # Assuming you have a Unix timestamp
        current_period_end_datetime = datetime.datetime.fromtimestamp(timestamp)
        await user_subscryption.update(
            stripe_price_id=subscryption["items"]["data"][0]["price"]["id"],
            stripe_current_period_end=current_period_end_datetime,
            stripe_subscription_id=subscryption.get("id"),
        )

    elif event["type"] == "customer.subscription.deleted":
        session = event.data.object
        user_subscryption = await user_subscryption_service.Meta.model.objects.get(
            stripe_subscription_id=session.get("id"),
        )
        user = user_subscryption.user
        old_display_role = user_subscryption.old_display_role
        if old_display_role.id == ProtectedDefaultRolesEnum.VIP.value:
            await user.load("roles")
            old_display_role = user.roles.all()[0]
        await user.update(display_role=old_display_role)
        await user_subscryption.update(stripe_subscription_id=None)
        logger.info(session)
        logger.info("User skonczyl subscrybcje")

    elif event["type"] == "customer.deleted":
        try:
            session = event.data.object
            logger.info(session)
            user_subscryption = await user_subscryption_service.Meta.model.objects.get(
                stripe_customer_id=session.get("id"),
            )

            await user_subscryption.delete()
        except NoMatch as e:
            logger.error(e)

    logger.info(event["type"])

    return {}
