from pathlib import Path
from textwrap import wrap

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "assets"
OUTPUT = ROOT / "docs" / "laboratorio-1-sabor-cusqueno.pdf"

PAGE_W, PAGE_H = 612, 792
INK = HexColor("#25231f")
MUTED = HexColor("#706b63")
PAPER = HexColor("#f8f5ef")
TERRACOTTA = HexColor("#bd5f42")
TERRACOTTA_DARK = HexColor("#91452e")
GOLD = HexColor("#d79c45")
LINE = HexColor("#e9e1d4")

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))


def cover_image(pdf, path, x, y, width, height):
    with Image.open(path) as source:
        image = source.convert("RGB")
        source_ratio = image.width / image.height
        target_ratio = width / height
        if source_ratio > target_ratio:
            crop_width = int(image.height * target_ratio)
            left = (image.width - crop_width) // 2
            image = image.crop((left, 0, left + crop_width, image.height))
        else:
            crop_height = int(image.width / target_ratio)
            top = (image.height - crop_height) // 2
            image = image.crop((0, top, image.width, top + crop_height))
        pdf.drawImage(ImageReader(image), x, y, width, height, mask="auto")


def wrapped_lines(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(pdf, text, x, y, width, font="Arial", size=11, color=INK, leading=17):
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    lines = wrapped_lines(text, font, size, width)
    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading
    return y


def heading(pdf, kicker, title):
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(TERRACOTTA)
    pdf.setFont("Arial-Bold", 9)
    pdf.drawString(52, 738, kicker.upper())
    pdf.setFillColor(INK)
    pdf.setFont("Arial-Bold", 30)
    pdf.drawString(52, 695, title)
    pdf.setStrokeColor(LINE)
    pdf.line(52, 674, 560, 674)


def footer(pdf, number):
    pdf.setStrokeColor(LINE)
    pdf.line(52, 42, 560, 42)
    pdf.setFillColor(MUTED)
    pdf.setFont("Arial", 8)
    pdf.drawString(52, 25, "Sabor Cusqueño · Laboratorio 1 · Ingeniería de Software")
    pdf.drawRightString(560, 25, f"{number:02d}")


def rounded_card(pdf, x, y, width, height, fill=white, stroke=LINE, radius=12):
    pdf.setFillColor(fill)
    pdf.setStrokeColor(stroke)
    pdf.roundRect(x, y, width, height, radius, fill=1, stroke=1)


def draw_cover(pdf):
    photo = ASSETS / "comida-andina-1.jpg"
    cover_image(pdf, photo, 0, 0, PAGE_W, PAGE_H)
    pdf.setFillColor(HexColor("#1d211f"))
    pdf.setFillAlpha(0.7)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(GOLD)
    pdf.setFont("Arial-Bold", 10)
    pdf.drawString(52, 710, "LABORATORIO 1  /  INGENIERÍA DE SOFTWARE")
    pdf.setFillColor(white)
    pdf.setFont("Arial-Bold", 48)
    pdf.drawString(52, 610, "Sabor")
    pdf.drawString(52, 554, "Cusqueño")
    pdf.setFont("Arial", 15)
    paragraph(
        pdf,
        "Introducción al entorno de desarrollo y Git",
        55,
        505,
        380,
        size=15,
        color=white,
        leading=22,
    )
    pdf.setFillColor(white)
    pdf.setFont("Arial", 10)
    pdf.drawString(55, 105, "Proyecto web estático para gestionar pedidos de comida local")
    pdf.setFillColor(GOLD)
    pdf.setFont("Arial-Bold", 10)
    pdf.drawString(55, 78, "Cusco · 2026")


def draw_case(pdf):
    heading(pdf, "01 · Contexto", "El caso práctico")
    pdf.setFillColor(TERRACOTTA)
    pdf.setFont("Arial-Bold", 11)
    pdf.drawString(52, 638, "Una startup local necesita ordenar su operación.")
    y = paragraph(
        pdf,
        "Sabor Cusqueño representa una primera versión de un sistema web para una startup de Cusco que ofrece comida local. La experiencia permite explorar platos, agregar productos a un pedido y confirmar el resumen antes de coordinar la entrega.",
        52,
        612,
        285,
        size=11,
        color=INK,
        leading=17,
    )
    y -= 10
    pdf.setFillColor(INK)
    pdf.setFont("Arial-Bold", 11)
    pdf.drawString(52, y, "Objetivos del laboratorio")
    y -= 23
    for item in [
        "Comprender el control de versiones.",
        "Configurar un proyecto web básico.",
        "Gestionar un repositorio local y remoto.",
    ]:
        pdf.setFillColor(TERRACOTTA)
        pdf.circle(58, y + 3, 3, fill=1, stroke=0)
        y = paragraph(pdf, item, 70, y, 260, size=10, color=MUTED, leading=16) - 3

    cover_image(pdf, ASSETS / "comida-andina-3.jpg", 365, 425, 195, 225)
    pdf.setFillColor(MUTED)
    pdf.setFont("Arial", 8)
    pdf.drawString(365, 411, "Referencia visual de la propuesta gastronómica")

    cover_image(pdf, ASSETS / "comida-andina-1.jpg", 52, 115, 245, 180)
    cover_image(pdf, ASSETS / "comida-andina-2.jpg", 315, 115, 245, 180)
    pdf.setFillColor(white)
    pdf.setFillAlpha(0.9)
    pdf.rect(52, 115, 245, 32, fill=1, stroke=0)
    pdf.rect(315, 115, 245, 32, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(INK)
    pdf.setFont("Arial-Bold", 9)
    pdf.drawString(65, 127, "Identidad cálida y artesanal")
    pdf.drawString(328, 127, "Producto local para compartir")
    footer(pdf, 2)


def draw_prototype(pdf):
    heading(pdf, "02 · Propuesta", "Prototipo funcional")
    paragraph(
        pdf,
        "La interfaz fue construida con HTML5, CSS3 y JavaScript vanilla para mantener el foco en los fundamentos: estructura, estilos, interacción y control de cambios.",
        52,
        640,
        505,
        size=11,
        color=MUTED,
        leading=17,
    )

    # Mockup visual del sitio, compuesto con elementos reales del proyecto.
    x, y, w, h = 52, 150, 508, 410
    rounded_card(pdf, x, y, w, h, fill=white, stroke=HexColor("#dcd3c6"), radius=14)
    pdf.setFillColor(HexColor("#f1ece4"))
    pdf.roundRect(x, y + h - 28, w, 28, 14, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#d2c5b3"))
    for dot in [x + 16, x + 28, x + 40]:
        pdf.circle(dot, y + h - 14, 3, fill=1, stroke=0)
    pdf.setFillColor(TERRACOTTA_DARK)
    pdf.setFont("Arial-Bold", 9)
    pdf.drawString(x + 75, y + h - 17, "Sabor Cusqueño")
    pdf.setFillColor(MUTED)
    pdf.setFont("Arial", 8)
    pdf.drawRightString(x + w - 18, y + h - 17, "Mi pedido  2")

    cover_image(pdf, ASSETS / "comida-andina-1.jpg", x + 16, y + h - 185, w - 32, 135)
    pdf.setFillColor(HexColor("#1d211f"))
    pdf.setFillAlpha(0.48)
    pdf.rect(x + 16, y + h - 185, w - 32, 135, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(white)
    pdf.setFont("Arial-Bold", 20)
    pdf.drawString(x + 32, y + h - 105, "Pedí lo mejor de nuestra cocina.")
    pdf.setFont("Arial", 8)
    pdf.drawString(x + 32, y + h - 124, "Sabores cusqueños preparados por emprendimientos locales.")

    cards_y = y + 30
    card_w = 145
    for index, (name, price) in enumerate([("Chiri Uchu", "S/ 28.00"), ("Kapchi de habas", "S/ 18.00"), ("Picarones", "S/ 12.00")]):
        card_x = x + 16 + index * (card_w + 18)
        rounded_card(pdf, card_x, cards_y, card_w, 105, fill=HexColor("#fffdf9"), stroke=LINE, radius=8)
        pdf.setFillColor(HexColor("#f7ead0"))
        pdf.roundRect(card_x + 10, cards_y + 56, 34, 34, 8, fill=1, stroke=0)
        pdf.setFillColor(TERRACOTTA_DARK)
        pdf.setFont("Arial-Bold", 8)
        pdf.drawString(card_x + 53, cards_y + 73, name)
        pdf.setFillColor(MUTED)
        pdf.setFont("Arial", 8)
        pdf.drawString(card_x + 53, cards_y + 58, price)
        pdf.setFillColor(TERRACOTTA)
        pdf.roundRect(card_x + 10, cards_y + 15, 80, 22, 5, fill=1, stroke=0)
        pdf.setFillColor(white)
        pdf.setFont("Arial-Bold", 7)
        pdf.drawString(card_x + 25, cards_y + 23, "AGREGAR")

    pdf.setFillColor(INK)
    pdf.setFont("Arial-Bold", 11)
    pdf.drawString(52, 105, "Interacciones implementadas")
    pdf.setFillColor(MUTED)
    pdf.setFont("Arial", 9)
    pdf.drawString(52, 88, "Catálogo · carrito · total automático · confirmación · diseño responsive")
    footer(pdf, 3)


def draw_git(pdf):
    heading(pdf, "03 · Entregable", "Git y GitHub")
    paragraph(
        pdf,
        "El repositorio mantiene un historial pequeño y legible. Cada commit representa una unidad de trabajo y utiliza Conventional Commits para comunicar la intención del cambio.",
        52,
        640,
        505,
        size=11,
        color=MUTED,
        leading=17,
    )

    rounded_card(pdf, 52, 430, 508, 125, fill=HexColor("#272522"), stroke=HexColor("#272522"), radius=12)
    pdf.setFillColor(HexColor("#f2ca83"))
    pdf.setFont("Arial", 10)
    commands = [
        "$ git init -b main",
        "$ git add .",
        "$ git commit -m \"chore: initialize food ordering project\"",
        "$ git push -u origin main",
    ]
    for index, command in enumerate(commands):
        pdf.drawString(72, 525 - index * 22, command)

    commits = [
        ("04e897e", "chore: initialize food ordering project"),
        ("76a2c5b", "feat: add local food ordering interface"),
    ]
    pdf.setFillColor(INK)
    pdf.setFont("Arial-Bold", 12)
    pdf.drawString(52, 385, "Evidencia de commits")
    for index, (sha, message) in enumerate(commits):
        yy = 350 - index * 42
        pdf.setFillColor(TERRACOTTA)
        pdf.circle(61, yy + 4, 4, fill=1, stroke=0)
        pdf.setFillColor(INK)
        pdf.setFont("Arial-Bold", 10)
        pdf.drawString(76, yy, sha)
        pdf.setFont("Arial", 10)
        pdf.drawString(145, yy, message)

    pdf.setFillColor(TERRACOTTA_DARK)
    pdf.setFont("Arial-Bold", 11)
    pdf.drawString(52, 235, "Repositorio remoto")
    pdf.setFillColor(INK)
    pdf.setFont("Arial", 10)
    pdf.drawString(52, 215, "github.com/hectorDev2/lab-1-ing-software-pedidos-cusco")
    paragraph(
        pdf,
        "Git es crítico en equipos colaborativos porque permite trazabilidad, revisión y recuperación de versiones. Evita perder cambios, sobrescribir trabajo ajeno y desconocer el origen de una modificación.",
        52,
        172,
        505,
        size=10,
        color=MUTED,
        leading=15,
    )
    footer(pdf, 4)


def draw_sources(pdf):
    heading(pdf, "04 · Cierre", "Reflexión y fuentes")
    paragraph(
        pdf,
        "El laboratorio permitió recorrer el flujo completo de un proyecto pequeño: definir una idea, crear una interfaz funcional, documentar el trabajo, versionarlo y publicarlo en un repositorio remoto.",
        52,
        640,
        505,
        size=12,
        color=INK,
        leading=19,
    )
    pdf.setFillColor(GOLD)
    pdf.roundRect(52, 438, 508, 92, 12, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.setFont("Arial-Bold", 16)
    pdf.drawString(76, 492, "Siguiente paso")
    paragraph(
        pdf,
        "Conectar el prototipo a una API y una base de datos para persistir clientes, pedidos y estados de entrega.",
        76,
        470,
        435,
        size=11,
        color=INK,
        leading=16,
    )

    pdf.setFillColor(INK)
    pdf.setFont("Arial-Bold", 11)
    pdf.drawString(52, 380, "Fotografías de referencia")
    pdf.setFillColor(MUTED)
    pdf.setFont("Arial", 8)
    sources = [
        "Unsplash · images.unsplash.com/photo-1515003197210-e0cd71810b5f",
        "Unsplash · images.unsplash.com/photo-1504674900247-0877df9cc836",
        "Unsplash · images.unsplash.com/photo-1547592180-85f173990554",
    ]
    for index, source in enumerate(sources):
        pdf.drawString(52, 357 - index * 18, source)

    pdf.setFillColor(TERRACOTTA)
    pdf.setFont("Arial-Bold", 10)
    pdf.drawString(52, 270, "Proyecto publicado")
    pdf.setFillColor(INK)
    pdf.setFont("Arial", 10)
    pdf.drawString(52, 250, "https://github.com/hectorDev2/lab-1-ing-software-pedidos-cusco")
    footer(pdf, 5)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    draw_cover(pdf)
    pdf.showPage()
    draw_case(pdf)
    pdf.showPage()
    draw_prototype(pdf)
    pdf.showPage()
    draw_git(pdf)
    pdf.showPage()
    draw_sources(pdf)
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()

