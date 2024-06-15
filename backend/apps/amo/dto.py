import dataclasses
from datetime import datetime
from . import DEAL_FIELD_TO_ID, CONTACT_FIELD_TO_ID
from apps.booking.models import Booking
from collections import defaultdict


@dataclasses.dataclass
class ContactDTO:
    first_name: str
    last_name: str
    email: str
    phone: str


@dataclasses.dataclass
class DealDTO:
    name: str
    price: int
    bought_tickets: str
    created_at: datetime
    contact: ContactDTO


@dataclasses.dataclass
class BookingDTO:
    place_name: str
    event_name: str
    types: dict[str, int]
    price: int
    time: datetime


DEAL_BOUGHT_TICKETS = "Купленные билеты"


def display_types(types) -> str:
    ss = []
    for key, val in types.items():
        ss.append(key + ": " + str(val))
    return ", ".join(ss)


def booking_to_string(b: BookingDTO) -> str:
    return b.place_name + "\n" \
        + b.event_name + "\n" \
        + display_types(b.types) + "\n" \
        + b.time.strftime("%d.%m %H:%M")


def deal_to_json(deal: DealDTO) -> {}:
    d_f_id = DEAL_FIELD_TO_ID
    c_f_id = CONTACT_FIELD_TO_ID
    return {
        "name": deal.name,
        "price": deal.price,
        "created_at": int(deal.created_at.astimezone().timestamp()),
        "custom_fields_values": [
            {"field_id": d_f_id[DEAL_BOUGHT_TICKETS], "values": [{"value": deal.bought_tickets}]},
        ],
        "_embedded": {
            "contacts": [
                {
                    "first_name": deal.contact.first_name,
                    "last_name": deal.contact.last_name,
                    "custom_fields_values": [
                        {"field_id": c_f_id["Телефон"], "values": [{"value": deal.contact.phone}]},
                        {"field_id": c_f_id["Email"], "values": [{"value": deal.contact.email}]}
                    ]
                }
            ]
        }
    }


def order_to_deal(order) -> DealDTO:
    bookings = group_bookings_by_place_event_time(order)
    return DealDTO(
        order.cart.buyer.first_name + " " + order.cart.buyer.last_name + " " + datetime.now().strftime("%d.%m"),
        int(order.total),
        "\n\n".join(list(map(booking_to_string, bookings))),
        datetime.now(),
        contact=ContactDTO(
            first_name=order.cart.buyer.first_name,
            last_name=order.cart.buyer.last_name,
            email=order.cart.buyer.email,
            phone=order.cart.buyer.phone,
        )
    )


def group_bookings_by_place_event_time(order):
    bookings = Booking.objects.filter(cart=order.cart).select_related('event', 'ticket', 'event__place')
    grouped_data = defaultdict(lambda: {'types': defaultdict(int), 'amount': 0, 'price': 0.0})
    print(bookings)
    for booking in bookings:
        key = (booking.event.place.name, booking.event.name, booking.time)
        grouped_data[key]['types'][booking.ticket.get_type_display()] += 1
        grouped_data[key]['price'] += int(booking.ticket.price)

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
