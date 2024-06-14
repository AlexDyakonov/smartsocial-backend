import requests

from backend.settings import AMOCRM_ACCESS_TOKEN


def get_field_to_id() -> dict[str, int]:
    url = 'https://forvantar.amocrm.ru/api/v4/leads/custom_fields'
    headers = {
        'Authorization': f'Bearer {AMOCRM_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        custom_fields = response.json()['_embedded']['custom_fields']
        field_to_id = {}
        for field in custom_fields:
            field_to_id[field['name']] = field['id']
        return field_to_id
    else:
        print('Ошибка при получении пользовательских полей:', response.json())
        return {}
