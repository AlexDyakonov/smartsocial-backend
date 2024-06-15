from .utils import get_custom_fields_to_id

DEAL_FIELD_TO_ID = get_custom_fields_to_id(
    "https://forvantar.amocrm.ru/api/v4/leads/custom_fields"
)
CONTACT_FIELD_TO_ID = get_custom_fields_to_id(
    "https://forvantar.amocrm.ru/api/v4/contacts/custom_fields"
)
