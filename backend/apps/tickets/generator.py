import os

import qrcode
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


def create_ticket_template(ticket_info):
    output_file = ticket_info["output_file"]

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
    c.drawString(30, y_position - 40, f"Количество мест: {ticket_info['seat_count']}")
    y_position -= 60

    # Генерация и вставка QR-кода
    qr_code_path = "qrcode.png"
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
            30, y_position, f"Билет {ticket['ticket_number']} - {ticket['place_name']}"
        )
        y_position -= 20
        c.setFont("Myriad", 12)
        c.drawString(
            30,
            y_position,
            f"{ticket['event_name']} - {ticket['date']}, {ticket['time']}",
        )
        y_position -= 20
        c.drawString(30, y_position, f"Стоимость - {ticket['cost']}")
        y_position -= 20
        c.drawString(30, y_position, f"Тип билета - {ticket['ticket_type']}")
        y_position -= 20
        c.line(30, y_position, width - 30, y_position)
        y_position -= 20

    # Информация о сервисе
    c.setFont("Myriad", 8)
    c.drawString(30, y_position, "Информация о сервисе мелким шрифтом")

    # Завершение и сохранение PDF
    c.showPage()
    c.save()
