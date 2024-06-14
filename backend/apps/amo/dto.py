import dataclasses
from datetime import datetime
from . import DEAL_FIELD_TO_ID


@dataclasses.dataclass
class DealDTO:
    name: str
    price: int
    event_place: str
    event_name: str
    ticket_type: str
    ticket_price: int
    tickets_amount: int
    datetime: datetime


DEAL_EVENT_PLACE = "Место проведения"
DEAL_EVENT_NAME = "Название мероприятия"
DEAL_TICKET_TYPE = "Тип билета"
DEAL_TICKET_PRICE = "Цена билета"
DEAL_TICKETS_AMOUNT = "Количество билетов"
DEAL_DATETIME = "Дата и время"


def deal_to_json(deal: DealDTO):
    f_id = DEAL_FIELD_TO_ID
    return {
        "name": deal.name,
        "price": deal.price,
        "created_at": int(deal.datetime.astimezone().timestamp()),
        "custom_fields_values": [
            {"field_id": f_id[DEAL_EVENT_PLACE], "values": [{"value": deal.event_place}]},
            {"field_id": f_id[DEAL_EVENT_NAME], "values": [{"value": deal.event_name}]},
            {"field_id": f_id[DEAL_DATETIME], "values": [{"value": deal.datetime.strftime("%Y-%m-%dT%H:%M:%SP")}]},
            {"field_id": f_id[DEAL_TICKET_TYPE], "values": [{"value": deal.ticket_type}]},
            {"field_id": f_id[DEAL_TICKETS_AMOUNT], "values": [{"value": deal.tickets_amount}]},
            {"field_id": f_id[DEAL_TICKET_PRICE], "values": [{"value": deal.ticket_price}]},
        ]
    }
