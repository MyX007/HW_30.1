from decimal import Decimal

import stripe
import requests

from config import settings


def create_price(title, description, amount):
    """Создание продукта и цены к нему для сервиса оплаты."""

    stripe.api_key = settings.API_KEY

    price_to_stripe = amount * 100

    product = stripe.Product.create(
        name=title,
        description=description,
    )

    price = stripe.Price.create(
        currency='rub',
        unit_amount= price_to_stripe,
        product=product['id']
    )

    return price["id"]


def create_payment_link(obj):
    """Создание ссылки на оплату."""
    stripe.api_key = settings.API_KEY

    payment = stripe.checkout.Session.create(
        line_items=[
            {
                "price": obj,
                "quantity": 1,
            }
        ],
        success_url="http://localhost:8000/payment/",
        mode="payment"
    )

    return {"payment_id": payment.get("id"), "payment_link": payment.get("url")}


