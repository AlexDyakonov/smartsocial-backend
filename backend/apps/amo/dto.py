import dataclasses
import json
from datetime import datetime
from . import DEAL_FIELD_TO_ID
from apps.booking.models import Booking
from collections import defaultdict


@dataclasses.dataclass
class DealDTO:
    name: str
    price: int
    bought_tickets: str
    created_at: datetime


@dataclasses.dataclass
class BookingDTO:
    place_name: str
    event_name: str
    types: dict[str, int]
    price: int
    time: datetime


DEAL_BOUGHT_TICKETS = "Купленные билеты"


def booking_to_string(b: BookingDTO) -> str:
    return b.place_name + " |" \
        + b.event_name + " |" \
        + json.dumps(b.types) + " |" \
        + str(b.price) + " | " \
        + b.time.strftime("%d.%m %H:%M")


def deal_to_json(deal: DealDTO) -> {}:
    f_id = DEAL_FIELD_TO_ID
    return {
        "name": deal.name,
        "price": deal.price,
        "created_at": int(deal.created_at.astimezone().timestamp()),
        "custom_fields_values": [
            {"field_id": f_id[DEAL_BOUGHT_TICKETS], "values": [{"value": deal.bought_tickets}]},
        ]
    }


def order_to_deal(order) -> DealDTO:
    bookings = group_bookings_by_place_event_time(order)
    return DealDTO(
        order.cart.buyer.first_name + " " + order.cart.buyer.last_name + " " + datetime.now().strftime("%d.%m"),
        int(order.total),
        "\n\n".join(list(map(booking_to_string, bookings))),
        datetime.now()
    )


def group_bookings_by_place_event_time(order):
    bookings = Booking.objects.filter(cart=order.cart).select_related('event', 'ticket', 'event__place')
    grouped_data = defaultdict(lambda: {'types': defaultdict(int), 'amount': 0, 'price': 0.0})
    print(bookings)
    for booking in bookings:
        key = (booking.event.place.name, booking.event.name, booking.time)
        grouped_data[key]['types'][booking.ticket.type] += booking
        grouped_data[key]['price'] += booking.ticket.price
    print(grouped_data)
    return [
        BookingDTO(
            place_name=key[0],
            event_name=key[1],
            types=dict(value['types']),
            price=value['price'],
            time=key[2]
        )
        for key, value in grouped_data.items()
    ]
