from apps.payments.models import Order
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from .tasks import send_mail_with_attachment


def send_purchase_email(email, payment_id):
    order = Order.objects.filter(payment_id=payment_id).first()
    qr_code_url = order.qr_code.url
    context = {"order": {"qr_code": {"url": qr_code_url}}}
    html_message = render_to_string("ticket-mail-template.html", context)
    soup = BeautifulSoup(html_message, "html.parser")
    html_message = str(soup)

    mail_data = {
        "subject": "Билеты в Коломне",
        "html_message": html_message,
    }

    send_mail_with_attachment([email], mail_data, "Ticket.pdf")
