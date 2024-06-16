import os

import qrcode
from apps.mailer.utils import send_purchase_email
from apps.payments.models import Order
from django.core.files import File
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def generate_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(file_path)


def check_page_space(y_position, c, height):
    if y_position < 100:
        c.showPage()
        c.setFont("Myriad-Bold", 18)
        c.drawString(30, height - 50, "Единый билет")
        return height - 70
    return y_position


def generate_ticket(ticket_info, payment_id):
    try:
        output_file = f"{ticket_info['output_file']}.pdf"

        c = canvas.Canvas(output_file, pagesize=A4)
        width, height = A4

        # Регистрация шрифтов
        pdfmetrics.registerFont(
            TTFont("Myriad", "/usr/local/share/fonts/MyriadPro-Regular.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("Myriad-Bold", "/usr/local/share/fonts/MyriadPro-Bold.ttf")
        )

        # Заголовок билета
        c.setFont("Myriad-Bold", 18)
        c.drawString(30, height - 50, "Единый билет")
        y_position = height - 70

        # Основная информация о билете
        c.setFont("Myriad", 12)
        c.drawString(30, y_position, f"Покупатель: {ticket_info['buyer_name']}")
        c.drawString(
            30, y_position - 20, f"Общая стоимость: {ticket_info['total_cost']} руб"
        )
        c.drawString(
            30, y_position - 40, f"Количество мест: {ticket_info['total_places']}"
        )
        y_position -= 60

        # Генерация и вставка QR-кода
        qr_code_path = f"qrcode_{payment_id}.png"

        generate_qr_code(ticket_info["qr_data"], qr_code_path)
        c.drawImage(qr_code_path, width - 120, height - 120, width=100, height=100)

        # Линия под основную информацию
        c.line(30, y_position, width - 30, y_position)
        y_position -= 20

        # Информация о каждом билете
        for ticket in ticket_info["tickets"]:
            y_position = check_page_space(y_position, c, height)
            c.setFont("Myriad-Bold", 12)
            c.drawString(
                30,
                y_position,
                f"Билет на {ticket['event_name']} - {ticket['place_name']}",
            )
            y_position -= 20
            c.setFont("Myriad", 12)
            c.drawString(
                30,
                y_position,
                f"{ticket['event_name']} - {ticket['date']}, {ticket['time']}",
            )
            y_position -= 20
            c.drawString(
                30,
                y_position,
                f"Стоимость - {ticket['cost']} - количеcтво -  {ticket['ticket_quantity']}",
            )
            y_position -= 20
            c.drawString(30, y_position, f"Тип билета - {ticket['ticket_type']}")
            y_position -= 20
            c.line(30, y_position, width - 30, y_position)
            y_position -= 20

        c.setFont("Myriad", 8)
        c.drawString(30, y_position, "Информация о сервисе мелким шрифтом")

        c.showPage()
        c.save()

        order = Order.objects.filter(payment_id=payment_id).first()

        with open(output_file, "rb") as f:
            order.ticket_file.save(output_file, File(f))

        with open(qr_code_path, "rb") as f:
            order.qr_code.save(qr_code_path, File(f))

        order.save()

        os.remove(qr_code_path)
        os.remove(output_file)

        return True

    except Exception as e:
        print(f"Error creating ticket: {e}")
        return False
