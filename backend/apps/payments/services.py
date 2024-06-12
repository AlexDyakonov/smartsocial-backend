import base64
import logging
import uuid

import requests

from backend.settings import YOOKASSA_ACCOUNT_ID, YOOKASSA_SECRET_KEY


class Logger:
    @staticmethod
    def get_logger():
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)


logger = Logger.get_logger()


class YooKassaService:
    @staticmethod
    def create_payment_embedded(
        amount, order_id, description="Оплата билетов в Коломне.", currency="RUB"
    ):
        try:
            response = send_yookassa_payment_request(
                amount, currency, description, order_id
            )
            if response.status_code == 200:
                logger.info(
                    f"Payment for order {order_id} created successfully: {response.json()}"
                )
                return response.json()
            else:
                logger.error(
                    f"Failed to create payment for order {order_id}: {response.status_code}, {response.text}"
                )
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"An error occurred while creating payment: {e}")
            raise


def send_yookassa_payment_request(amount, currency, description, order_id):
    shop_id = YOOKASSA_ACCOUNT_ID
    secret_key = YOOKASSA_SECRET_KEY
    idempotence_key = generate_idempotence_key()

    auth = base64.b64encode(f"{shop_id}:{secret_key}".encode("utf-8")).decode("utf-8")
    headers = {
        "Idempotence-Key": idempotence_key,
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth}",
    }
    data = {
        "amount": {"value": amount, "currency": currency},
        "confirmation": {"type": "embedded"},
        "capture": True,
        "description": f"Заказ №{order_id} | {description}",
    }

    url = "https://api.yookassa.ru/v3/payments"
    return requests.post(url, headers=headers, json=data)


def generate_idempotence_key():
    return str(uuid.uuid4())
