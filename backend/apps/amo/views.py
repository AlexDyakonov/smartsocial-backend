import requests

from apps.amo.dto import DealDTO, deal_to_json, order_to_deal
from backend.settings import AMOCRM_ACCESS_TOKEN


def post_deals(deals: list[DealDTO]):
    url = 'https://forvantar.amocrm.ru/api/v4/leads/complex'
    json_data = list(map(deal_to_json, deals))
    headers = {
        'Authorization': f'Bearer {AMOCRM_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    print(requests.post(url, json=json_data, headers=headers).text)


def post_orders(orders):
    return post_deals(list(map(order_to_deal, orders)))
