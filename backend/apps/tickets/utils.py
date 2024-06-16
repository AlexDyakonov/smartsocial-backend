from apps.booking.models import CartTicket
from apps.payments.models import Order


def get_ticket_info(order_id):
    try:
        order = Order.objects.filter(payment_id=order_id).first()
        if not order:
            raise ValueError("Order not found")

        cart = order.cart
        if not cart:
            raise ValueError("Cart not found for the given order")

        cart_tickets = CartTicket.objects.filter(cart=cart)

        ticket_details = [
            {
                "ticket_number": cart_ticket.id,
                "place_name": cart_ticket.ticket.place.name,
                "event_name": cart_ticket.ticket.name,
                "date": cart_ticket.time.date(),
                "time": cart_ticket.time.time(),
                "cost": f"{cart_ticket.ticket.price} руб.",
                "ticket_type": cart_ticket.ticket.get_type_display(),
                "ticket_quantity": cart_ticket.quantity,
            }
            for cart_ticket in cart_tickets
        ]

        ticket_info = {
            "output_file": f"ticket_{order_id}",
            "buyer_name": f"{cart.buyer.first_name} {cart.buyer.last_name}",
            "total_cost": order.total,
            "total_places": cart.total_places,
            "qr_data": f"https://kolomnago.ru/booking/{order_id}",
            "tickets": ticket_details,
        }
        return ticket_info
    except Exception as e:
        print(f"Error fetching ticket info: {e}")
        return dict()
