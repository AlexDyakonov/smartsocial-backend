import dataclasses
from datetime import datetime
from . import DEAL_FIELD_TO_ID, CONTACT_FIELD_TO_ID, PIPELINE_FIELD_TO_ID
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
    payment_id: str
    name: str
    price: int
    bought_tickets: str
    visited_tickets: str
    created_at: datetime
    contact: ContactDTO
    status_id: int


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
        "status_id": deal.status_id,
        "created_at": int(deal.created_at.astimezone().timestamp()),
        "custom_fields_values": [
            {"field_id": d_f_id[DEAL_BOUGHT_TICKETS], "values": [{"value": deal.bought_tickets}]},
            {"field_id": d_f_id["Посещения"], "values": [{"value": deal.visited_tickets}]},
            {"field_id": d_f_id["ID заказа"], "values": [{"value": deal.payment_id}]},
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
    print(order)
    bookings = group_bookings_by_place_event_time(order)
    visited_bookings = group_visited_by_place_event_time(order)
    p_f_id = PIPELINE_FIELD_TO_ID
    status = p_f_id["оплачен"] if (order.payment_status == "succeeded") else p_f_id["не оплачен"]

    if len(visited_bookings) != 0:
        status = p_f_id["посетил"]

    return DealDTO(
        order.payment_id,
        order.cart.buyer.first_name + " " + order.cart.buyer.last_name + " " + datetime.now().strftime("%d.%m"),
        int(order.total),
        "\n\n".join(list(map(booking_to_string, bookings))),
        "\n\n".join(list(map(booking_to_string, visited_bookings))),
        datetime.now(),
        ContactDTO(
            first_name=order.cart.buyer.first_name,
            last_name=order.cart.buyer.last_name,
            email=order.cart.buyer.email,
            phone=order.cart.buyer.phone,
        ),
        status
    )


def group_bookings_by_place_event_time(order):
    bookings = Booking.objects.filter(cart=order.cart).select_related('event', 'ticket', 'event__place')
    grouped_data = defaultdict(lambda: {'types': defaultdict(int), 'amount': 0, 'price': 0.0})
    print(bookings)
    for booking in bookings:
        key = (booking.event.place.name, booking.event.name, booking.time)
        grouped_data[key]['types'][booking.ticket.get_type_display()] += booking.quantity
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


def group_visited_by_place_event_time(order):
    bookings = Booking.objects.filter(cart=order.cart, visited=True).select_related('event', 'ticket', 'event__place')
    grouped_data = defaultdict(lambda: {'types': defaultdict(int), 'amount': 0, 'price': 0.0})
    print(bookings)
    for booking in bookings:
        key = (booking.event.place.name, booking.event.name, booking.time)
        grouped_data[key]['types'][booking.ticket.get_type_display()] += booking.quantity
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
