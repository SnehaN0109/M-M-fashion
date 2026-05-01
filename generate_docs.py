from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import KeepTogether

OUTPUT_FILE = "PROJECT_DOCUMENTATION.pdf"

# ── Colour palette ──────────────────────────────────────────────────────────
BRAND_DARK   = colors.HexColor("#1a1a2e")
BRAND_MID    = colors.HexColor("#16213e")
BRAND_ACCENT = colors.HexColor("#e94560")
BRAND_LIGHT  = colors.HexColor("#f5f5f5")
GREY_TEXT    = colors.HexColor("#444444")
LIGHT_GREY   = colors.HexColor("#cccccc")
TABLE_HEADER = colors.HexColor("#2d2d44")
TABLE_ROW1   = colors.HexColor("#f9f9f9")
TABLE_ROW2   = colors.white

def build_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title", parent=base["Title"],
        fontSize=32, textColor=colors.white,
        spaceAfter=8, alignment=TA_CENTER, leading=40,
        fontName="Helvetica-Bold"
    )
    styles["cover_sub"] = ParagraphStyle(
        "cover_sub", parent=base["Normal"],
        fontSize=14, textColor=colors.HexColor("#dddddd"),
        spaceAfter=6, alignment=TA_CENTER, leading=20,
        fontName="Helvetica"
    )
    styles["section_heading"] = ParagraphStyle(
        "section_heading", parent=base["Heading1"],
        fontSize=18, textColor=BRAND_ACCENT,
        spaceBefore=18, spaceAfter=6, leading=24,
        fontName="Helvetica-Bold", borderPad=4
    )
    styles["sub_heading"] = ParagraphStyle(
        "sub_heading", parent=base["Heading2"],
        fontSize=13, textColor=BRAND_DARK,
        spaceBefore=12, spaceAfter=4, leading=18,
        fontName="Helvetica-Bold"
    )
    styles["sub_sub_heading"] = ParagraphStyle(
        "sub_sub_heading", parent=base["Heading3"],
        fontSize=11, textColor=BRAND_MID,
        spaceBefore=8, spaceAfter=3, leading=16,
        fontName="Helvetica-Bold"
    )
    styles["body"] = ParagraphStyle(
        "body", parent=base["Normal"],
        fontSize=10, textColor=GREY_TEXT,
        spaceAfter=4, leading=15, alignment=TA_JUSTIFY,
        fontName="Helvetica"
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", parent=base["Normal"],
        fontSize=10, textColor=GREY_TEXT,
        spaceAfter=3, leading=15,
        leftIndent=16, bulletIndent=4,
        fontName="Helvetica"
    )
    styles["bullet2"] = ParagraphStyle(
        "bullet2", parent=base["Normal"],
        fontSize=9.5, textColor=GREY_TEXT,
        spaceAfter=2, leading=14,
        leftIndent=32, bulletIndent=20,
        fontName="Helvetica"
    )
    styles["code_inline"] = ParagraphStyle(
        "code_inline", parent=base["Normal"],
        fontSize=9, textColor=colors.HexColor("#c0392b"),
        fontName="Courier", leading=13
    )
    styles["toc_entry"] = ParagraphStyle(
        "toc_entry", parent=base["Normal"],
        fontSize=11, textColor=BRAND_DARK,
        spaceAfter=5, leading=16,
        fontName="Helvetica"
    )
    styles["footer_note"] = ParagraphStyle(
        "footer_note", parent=base["Normal"],
        fontSize=8, textColor=LIGHT_GREY,
        alignment=TA_CENTER, fontName="Helvetica"
    )
    return styles


def hr(width=None):
    return HRFlowable(
        width=width or "100%", thickness=1,
        color=LIGHT_GREY, spaceAfter=6, spaceBefore=4
    )


def accent_hr():
    return HRFlowable(
        width="100%", thickness=2,
        color=BRAND_ACCENT, spaceAfter=8, spaceBefore=2
    )


def sp(h=6):
    return Spacer(1, h)


def bullet_item(text, s, level=1):
    style = s["bullet"] if level == 1 else s["bullet2"]
    marker = "\u2022" if level == 1 else "\u25e6"
    return Paragraph(f"{marker}&nbsp;&nbsp;{text}", style)


def numbered_item(n, text, s):
    return Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{text}", s["bullet"])


def api_row(method, endpoint, desc):
    method_colors = {
        "GET":    colors.HexColor("#27ae60"),
        "POST":   colors.HexColor("#2980b9"),
        "PUT":    colors.HexColor("#f39c12"),
        "DELETE": colors.HexColor("#e74c3c"),
    }
    col = method_colors.get(method, colors.grey)
    return [
        Paragraph(f'<font color="{col.hexval()}"><b>{method}</b></font>',
                  ParagraphStyle("m", fontSize=9, fontName="Courier", leading=12)),
        Paragraph(f'<font name="Courier" size="9">{endpoint}</font>',
                  ParagraphStyle("e", fontSize=9, fontName="Courier", leading=12,
                                 textColor=colors.HexColor("#1a1a2e"))),
        Paragraph(desc,
                  ParagraphStyle("d", fontSize=9, fontName="Helvetica", leading=12,
                                 textColor=GREY_TEXT)),
    ]


def make_api_table(rows):
    col_widths = [1.5*cm, 7.5*cm, 8.5*cm]
    header = [
        Paragraph("<b>Method</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold",
                                                   textColor=colors.white, leading=12)),
        Paragraph("<b>Endpoint</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold",
                                                     textColor=colors.white, leading=12)),
        Paragraph("<b>Description</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold",
                                                        textColor=colors.white, leading=12)),
    ]
    data = [header] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ])
    t.setStyle(style)
    return t


# ═══════════════════════════════════════════════════════════════════════════
#  CONTENT BUILDERS
# ═══════════════════════════════════════════════════════════════════════════

def cover_page(s):
    elems = []
    # Dark background block via a 1-row table
    cover_data = [[
        Paragraph("M&amp;M Fashion", s["cover_title"]),
    ]]
    cover_table = Table(cover_data, colWidths=[17*cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 40),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
    ]))
    elems.append(cover_table)

    sub_data = [[
        Paragraph("Multi-Domain E-Commerce Platform", s["cover_sub"]),
    ]]
    sub_table = Table(sub_data, colWidths=[17*cm])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_MID),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
    ]))
    elems.append(sub_table)
    elems.append(sp(30))

    info_rows = [
        ["Project", "M&amp;M Fashion — Multi-Domain E-Commerce Platform"],
        ["Type", "Full-Stack Web Application (B2C + B2B)"],
        ["Frontend", "React 19 + Vite 7 + Tailwind CSS 4"],
        ["Backend", "Python 3 + Flask + SQLAlchemy"],
        ["Database", "MySQL (14 tables)"],
        ["Domains", "garba.shop &nbsp;|&nbsp; ttd.in &nbsp;|&nbsp; maharashtra"],
        ["Pages", "27 Frontend Pages"],
        ["API Routes", "30+ REST API Endpoints"],
    ]
    cell_style = ParagraphStyle("ci", fontSize=10, fontName="Helvetica",
                                 textColor=GREY_TEXT, leading=14)
    label_style = ParagraphStyle("cl", fontSize=10, fontName="Helvetica-Bold",
                                  textColor=BRAND_DARK, leading=14)
    table_data = [[Paragraph(r[0], label_style), Paragraph(r[1], cell_style)]
                  for r in info_rows]
    info_table = Table(table_data, colWidths=[5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    elems.append(info_table)
    elems.append(sp(30))
    elems.append(Paragraph("Project Technical Documentation", s["cover_sub"]))
    elems.append(PageBreak())
    return elems


def toc_page(s):
    elems = []
    elems.append(Paragraph("Table of Contents", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(8))
    toc = [
        ("1", "Project Overview"),
        ("2", "Technology Stack"),
        ("3", "Database Structure — 14 Tables"),
        ("4", "API Endpoints"),
        ("5", "Frontend Pages (27 Pages)"),
        ("6", "How Key Features Work"),
        ("7", "Project Folder Structure"),
        ("8", "Future Scope"),
    ]
    for num, title in toc:
        elems.append(Paragraph(
            f'<b>Section {num}</b>&nbsp;&nbsp;&nbsp;{title}',
            s["toc_entry"]
        ))
        elems.append(hr())
    elems.append(PageBreak())
    return elems


def section1(s):
    elems = []
    elems.append(Paragraph("Section 1: Project Overview", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(4))

    elems.append(Paragraph(
        "M&amp;M Fashion is a full-stack e-commerce web application built for an Indian ethnic and western "
        "clothing manufacturer. The platform solves the challenge of managing both retail (B2C) and wholesale "
        "(B2B) customers on a single codebase, with different pricing and branding for each audience.",
        s["body"]
    ))
    elems.append(sp(10))

    elems.append(Paragraph("The 3-Domain Concept", s["sub_heading"]))
    elems.append(hr())
    elems.append(Paragraph(
        "The same codebase runs on three different domains. Each domain shows different prices and branding, "
        "automatically detected from <font name='Courier'>window.location.hostname</font>:",
        s["body"]
    ))
    elems.append(sp(6))

    domain_data = [
        [
            Paragraph("<b>Domain</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                       textColor=colors.white, leading=13)),
            Paragraph("<b>Audience</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                         textColor=colors.white, leading=13)),
            Paragraph("<b>Price Column</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                             textColor=colors.white, leading=13)),
            Paragraph("<b>Description</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                            textColor=colors.white, leading=13)),
        ],
        [
            Paragraph('<font name="Courier">garba.shop</font>',
                      ParagraphStyle("c", fontSize=10, fontName="Courier", leading=13,
                                     textColor=colors.HexColor("#27ae60"))),
            Paragraph("B2C Retail", s["body"]),
            Paragraph('<font name="Courier">price_b2c</font>',
                      ParagraphStyle("c", fontSize=10, fontName="Courier", leading=13)),
            Paragraph("End customers — retail prices", s["body"]),
        ],
        [
            Paragraph('<font name="Courier">ttd.in</font>',
                      ParagraphStyle("c", fontSize=10, fontName="Courier", leading=13,
                                     textColor=colors.HexColor("#2980b9"))),
            Paragraph("B2B Wholesale (TTD)", s["body"]),
            Paragraph('<font name="Courier">price_b2b_ttd</font>',
                      ParagraphStyle("c", fontSize=10, fontName="Courier", leading=13)),
            Paragraph("TTD distributors — wholesale prices", s["body"]),
        ],
        [
            Paragraph('<font name="Courier">maharashtra</font>',
                      ParagraphStyle("c", fontSize=10, fontName="Courier", leading=13,
                                     textColor=colors.HexColor("#8e44ad"))),
            Paragraph("B2B Wholesale (MH)", s["body"]),
            Paragraph('<font name="Courier">price_b2b_maharashtra</font>',
                      ParagraphStyle("c", fontSize=10, fontName="Courier", leading=13)),
            Paragraph("Maharashtra distributors — wholesale prices", s["body"]),
        ],
    ]
    domain_table = Table(domain_data, colWidths=[3.5*cm, 3.5*cm, 4.5*cm, 6*cm])
    domain_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elems.append(domain_table)
    elems.append(sp(10))

    elems.append(Paragraph("How Domain Detection Works", s["sub_heading"]))
    elems.append(hr())
    steps = [
        "The website loads and <b>DomainContext</b> reads <font name='Courier'>window.location.hostname</font>.",
        "It matches the hostname to one of the 3 domain configs.",
        "Each config has a <font name='Courier'>priceKey</font>: <font name='Courier'>price_b2c</font>, <font name='Courier'>price_b2b_ttd</font>, or <font name='Courier'>price_b2b_maharashtra</font>.",
        "Every API call to fetch products passes this <font name='Courier'>priceKey</font> as a query parameter.",
        "The backend reads the <font name='Courier'>priceKey</font> and returns the correct price column from the <font name='Courier'>productvariant</font> table.",
        "On localhost, a floating <b>DevDomainSwitcher</b> widget lets developers switch between domains for testing.",
    ]
    for i, step in enumerate(steps, 1):
        elems.append(numbered_item(i, step, s))
    elems.append(PageBreak())
    return elems


def section2(s):
    elems = []
    elems.append(Paragraph("Section 2: Technology Stack", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(4))

    # Frontend
    elems.append(Paragraph("Frontend", s["sub_heading"]))
    elems.append(hr())
    frontend = [
        ("React 19", "JavaScript library for building the user interface"),
        ("Vite 7", "Fast build tool and development server"),
        ("React Router DOM 7", "Client-side routing between pages"),
        ("Tailwind CSS 4", "Utility-first CSS framework for styling"),
        ("Lucide React", "Icon library used throughout the UI"),
        ("Context API", "Built-in React state management for cart, wishlist, and domain"),
    ]
    tech_data = [[
        Paragraph("<b>Library / Tool</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                           textColor=colors.white, leading=13)),
        Paragraph("<b>Purpose</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                    textColor=colors.white, leading=13)),
    ]] + [
        [Paragraph(f'<font name="Courier">{t}</font>',
                   ParagraphStyle("c", fontSize=10, fontName="Courier", leading=13,
                                  textColor=BRAND_DARK)),
         Paragraph(d, s["body"])]
        for t, d in frontend
    ]
    t = Table(tech_data, colWidths=[5*cm, 12.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elems.append(t)
    elems.append(sp(12))

    # Backend
    elems.append(Paragraph("Backend", s["sub_heading"]))
    elems.append(hr())
    backend = [
        ("Python 3", "Programming language for the backend"),
        ("Flask", "Lightweight web framework for building REST APIs"),
        ("Flask-SQLAlchemy", "ORM for database operations"),
        ("Flask-CORS", "Handles Cross-Origin Resource Sharing for frontend-backend communication"),
        ("PyMySQL", "MySQL database driver for Python"),
        ("PyJWT", "JSON Web Token library for user authentication"),
        ("python-dotenv", "Loads environment variables from .env file"),
    ]
    tech_data2 = [[
        Paragraph("<b>Library / Tool</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                           textColor=colors.white, leading=13)),
        Paragraph("<b>Purpose</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                    textColor=colors.white, leading=13)),
    ]] + [
        [Paragraph(f'<font name="Courier">{t}</font>',
                   ParagraphStyle("c", fontSize=10, fontName="Courier", leading=13,
                                  textColor=BRAND_DARK)),
         Paragraph(d, s["body"])]
        for t, d in backend
    ]
    t2 = Table(tech_data2, colWidths=[5*cm, 12.5*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elems.append(t2)
    elems.append(sp(12))

    elems.append(Paragraph("Database", s["sub_heading"]))
    elems.append(hr())
    elems.append(bullet_item("MySQL — Relational database for storing all application data", s))
    elems.append(bullet_item("SQLAlchemy ORM — Maps Python classes to database tables", s))
    elems.append(PageBreak())
    return elems


def section3(s):
    elems = []
    elems.append(Paragraph("Section 3: Database Structure — 14 Tables", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(4))
    elems.append(Paragraph(
        "The MySQL database consists of 14 tables that cover all aspects of the platform — "
        "users, products, orders, cart, reviews, photos, and discount codes.",
        s["body"]
    ))
    elems.append(sp(10))

    tables = [
        ("1", "user",
         "Stores customer accounts.",
         ["id", "whatsapp_number", "email", "name", "created_at"],
         "Users register via WhatsApp number."),
        ("2", "address",
         "Stores saved delivery addresses for users.",
         ["id", "user_id", "full_name", "phone", "line1", "line2", "city", "state", "pincode", "is_default"],
         "Currently scaffolded for future saved address feature."),
        ("3", "product",
         "Stores the main product information.",
         ["id", "name", "description", "category", "fabric", "occasion", "pattern", "gender",
          "image_url", "video_url", "created_at"],
         "Categories: Men, Women, Kids, Ethnic, Western, Party Wear."),
        ("4", "productvariant",
         "Stores each colour+size combination of a product with separate stock and 3 price columns.",
         ["id", "product_id", "design_id", "color", "size", "quantity",
          "price_b2c", "price_b2b_ttd", "price_b2b_maharashtra"],
         "This is the core of the multi-domain pricing system."),
        ("5", "productimage",
         "Stores multiple images per product for the image gallery.",
         ["id", "product_id", "image_url", "is_primary", "sort_order"],
         ""),
        ("6", "productvideo",
         "Stores video URLs for products.",
         ["id", "product_id", "video_url"],
         ""),
        ("7", "cart",
         "One cart per user.",
         ["id", "user_id", "session_id", "created_at"],
         ""),
        ("8", "cartitem",
         "Individual items inside a cart.",
         ["id", "cart_id", "variant_id", "quantity"],
         "Links cart to specific product variants."),
        ("9", "order",
         "Stores placed orders with full customer and address details.",
         ["id", "user_id", "customer_name", "customer_email", "customer_phone",
          "address fields", "subtotal", "discount_amount", "discount_code",
          "shipping_charge", "tax_amount", "total_amount", "domain_origin",
          "payment_method", "status", "tracking_number", "created_at"],
         "Status flow: pending_payment → confirmed → packed → shipped → delivered."),
        ("10", "orderitem",
         "Individual products inside an order with price snapshot.",
         ["id", "order_id", "variant_id", "quantity", "price_at_purchase"],
         "Price is saved at time of purchase so future price changes don't affect old orders."),
        ("11", "review",
         "Customer product reviews.",
         ["id", "product_id", "user_id", "rating (1–5)", "comment", "created_at"],
         ""),
        ("12", "userphoto",
         "Customer-uploaded photos wearing the product.",
         ["id", "product_id", "user_id", "photo_url", "is_approved", "created_at"],
         "Admin must approve before photos are shown publicly."),
        ("13", "discountcode",
         "Promotional discount codes.",
         ["id", "code", "discount_percentage", "discount_flat", "min_cart_value", "is_active", "created_at"],
         "Supports both percentage and flat discounts."),
        ("14", "wishlist",
         "Products saved to wishlist by users.",
         ["id", "user_id", "product_id", "created_at"],
         ""),
    ]

    for num, name, desc, fields, note in tables:
        block = []
        block.append(Paragraph(
            f'<b>{num}. <font name="Courier">{name}</font></b> — {desc}',
            s["sub_sub_heading"]
        ))
        fields_str = ", ".join(f'<font name="Courier">{f}</font>' for f in fields)
        block.append(Paragraph(f"<b>Fields:</b> {fields_str}", s["body"]))
        if note:
            block.append(Paragraph(f"<i>{note}</i>", s["body"]))
        block.append(sp(4))
        elems.append(KeepTogether(block))

    elems.append(sp(10))
    elems.append(Paragraph("Table Relationships", s["sub_heading"]))
    elems.append(hr())
    relationships = [
        "user → order (one user can have many orders)",
        "user → cart (one user has one cart)",
        "user → review (one user can write many reviews)",
        "user → userphoto (one user can upload many photos)",
        "user → wishlist (one user can have many wishlist items)",
        "product → productvariant (one product has many variants)",
        "product → productimage (one product has many images)",
        "product → productvideo (one product has many videos)",
        "product → review (one product has many reviews)",
        "product → userphoto (one product has many customer photos)",
        "cart → cartitem (one cart has many items)",
        "cartitem → productvariant (each cart item is a specific variant)",
        "order → orderitem (one order has many items)",
        "orderitem → productvariant (each order item is a specific variant)",
    ]
    for r in relationships:
        parts = r.split("→")
        if len(parts) == 2:
            left = parts[0].strip()
            right_full = parts[1].strip()
            paren_start = right_full.find("(")
            if paren_start != -1:
                right_table = right_full[:paren_start].strip()
                right_note = right_full[paren_start:]
                text = (f'<font name="Courier"><b>{left}</b></font> → '
                        f'<font name="Courier"><b>{right_table}</b></font> '
                        f'<i>{right_note}</i>')
            else:
                text = (f'<font name="Courier"><b>{left}</b></font> → '
                        f'<font name="Courier"><b>{right_full}</b></font>')
        else:
            text = r
        elems.append(bullet_item(text, s))
    elems.append(PageBreak())
    return elems


def section4(s):
    elems = []
    elems.append(Paragraph("Section 4: API Endpoints", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(4))

    # AUTH
    elems.append(Paragraph("Auth Routes  (prefix: /api/auth)", s["sub_heading"]))
    elems.append(hr())
    auth_rows = [
        api_row("POST", "/api/auth/send-otp",
                "Sends OTP to WhatsApp number. Takes: whatsapp_number. Returns: success message. (Demo: OTP hardcoded as 1234)"),
        api_row("POST", "/api/auth/verify-otp",
                "Verifies OTP and returns JWT token. Takes: whatsapp_number, otp. Returns: token, user_id, whatsapp_number."),
        api_row("POST", "/api/auth/whatsapp-login",
                "Legacy login route. Takes: whatsapp_number. Returns: user_id."),
    ]
    elems.append(make_api_table(auth_rows))
    elems.append(sp(12))

    # PRODUCTS
    elems.append(Paragraph("Product Routes  (prefix: /api/products)", s["sub_heading"]))
    elems.append(hr())
    product_rows = [
        api_row("GET", "/api/products/",
                "Get all products with filters. Takes: domain, price_key, category, size, color, min_price, max_price, search."),
        api_row("GET", "/api/products/<id>",
                "Get single product detail. Takes: price_key. Returns: product with all variants, images, prices."),
        api_row("GET", "/api/products/<id>/reviews",
                "Get all reviews for a product. Returns: list of reviews with rating and comment."),
        api_row("POST", "/api/products/<id>/reviews",
                "Submit a review. Takes: rating, comment, whatsapp_number. Returns: success."),
        api_row("GET", "/api/products/<id>/photos",
                "Get approved customer photos for a product. Returns: list of photo URLs."),
        api_row("POST", "/api/products/<id>/photos",
                "Upload a customer photo. Takes: photo file, whatsapp_number. Returns: success."),
    ]
    elems.append(make_api_table(product_rows))
    elems.append(sp(12))

    # CART
    elems.append(Paragraph("Cart Routes  (prefix: /api)", s["sub_heading"]))
    elems.append(hr())
    cart_rows = [
        api_row("GET", "/api/cart",
                "Get cart items for a user. Takes: whatsapp_number (query param). Returns: cart items with product details and all 3 prices."),
        api_row("POST", "/api/cart/add",
                "Add item to cart. Takes: whatsapp_number, variant_id, quantity. Returns: cart_item_id."),
        api_row("DELETE", "/api/cart/remove",
                "Remove item from cart. Takes: whatsapp_number, variant_id. Returns: success."),
        api_row("DELETE", "/api/cart/clear",
                "Clear entire cart after order placed. Takes: whatsapp_number. Returns: success."),
        api_row("POST", "/api/cart/apply_discount",
                "Validate and apply discount code. Takes: code, cart_total. Returns: discount_percentage or discount_flat."),
    ]
    elems.append(make_api_table(cart_rows))
    elems.append(sp(12))

    # ORDERS
    elems.append(Paragraph("Order Routes  (prefix: /api/orders)", s["sub_heading"]))
    elems.append(hr())
    order_rows = [
        api_row("POST", "/api/orders/checkout",
                "Place an order. Takes: customer details, address, items array, domain, price_key, discount_code. Returns: order_id, total_amount, status."),
        api_row("GET", "/api/orders/track/<order_id>",
                "Track order by ID. Returns: status, tracking_number, customer details, items."),
        api_row("GET", "/api/orders/my-orders",
                "Get all orders for a user. Takes: whatsapp_number. Returns: list of orders."),
        api_row("GET", "/api/track/<identifier>",
                "Smart track route. Accepts order ID (number) or tracking number (string). Returns: order status."),
    ]
    elems.append(make_api_table(order_rows))
    elems.append(sp(12))

    # ADMIN
    elems.append(Paragraph("Admin Routes  (prefix: /api/admin)", s["sub_heading"]))
    elems.append(hr())
    admin_rows = [
        api_row("POST", "/api/admin/login",
                "Admin login. Takes: password. Returns: token."),
        api_row("GET", "/api/admin/products",
                "List all products. Returns: products with variant count."),
        api_row("POST", "/api/admin/products/add",
                "Add new product with variants. Takes: all product fields + variants array."),
        api_row("PUT", "/api/admin/products/<id>",
                "Edit product details. Takes: product fields."),
        api_row("DELETE", "/api/admin/products/<id>",
                "Delete product and all variants."),
        api_row("GET", "/api/admin/orders",
                "List all orders with optional status filter."),
        api_row("PUT", "/api/admin/orders/<id>/status",
                "Update order status and tracking number."),
        api_row("GET", "/api/admin/discount-codes",
                "List all discount codes."),
        api_row("POST", "/api/admin/discount-codes",
                "Create new discount code."),
        api_row("PUT", "/api/admin/discount-codes/<id>",
                "Toggle discount code active/inactive."),
        api_row("DELETE", "/api/admin/discount-codes/<id>",
                "Delete discount code."),
        api_row("GET", "/api/admin/photos/pending",
                "Get photos pending admin approval."),
        api_row("POST", "/api/admin/photos/<id>/approve",
                "Approve a customer photo."),
        api_row("DELETE", "/api/admin/photos/<id>/reject",
                "Reject and delete a customer photo."),
    ]
    elems.append(make_api_table(admin_rows))
    elems.append(PageBreak())
    return elems


def section5(s):
    elems = []
    elems.append(Paragraph("Section 5: Frontend Pages (27 Pages)", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(4))
    elems.append(Paragraph(
        "The frontend consists of 27 page components built with React 19. "
        "Each page is a separate file inside the <font name='Courier'>src/pages/</font> directory.",
        s["body"]
    ))
    elems.append(sp(8))

    pages = [
        ("1", "HomePage",
         "Landing page with hero banner, featured products grid, trust badges.",
         "GET /api/products/"),
        ("2", "ProductListPage",
         "Browse all products with sidebar filters (category, size, color, price range).",
         "GET /api/products/ with filter params"),
        ("3", "ProductDetailPage",
         "Full product detail with image gallery, colour/size selector, add to cart, reviews, customer photos.",
         "GET /api/products/<id>, GET /api/products/<id>/reviews, GET /api/products/<id>/photos"),
        ("4", "CartPage",
         "Shopping cart with quantity controls, coupon code, price summary.",
         "Loads from CartContext (synced with DB)"),
        ("5", "CheckoutPage",
         "Order form with customer details, shipping address, discount code, order summary.",
         "POST /api/orders/checkout"),
        ("6", "OrderSuccessPage",
         "Confirmation page shown after successful order placement.",
         "—"),
        ("7", "PaymentPage",
         "Placeholder page. Payment is COD only. Future scope for Razorpay integration.",
         "—"),
        ("8", "MyOrdersPage",
         "List of all past orders for logged-in user.",
         "GET /api/orders/my-orders"),
        ("9", "TrackOrderPage",
         "Order tracking with visual status timeline.",
         "GET /api/orders/track/<id>"),
        ("10", "SearchResultsPage",
         "Search results page.",
         "GET /api/products/?search=query"),
        ("11", "WishlistPage",
         "Saved products wishlist.",
         "Managed via WishlistContext (localStorage)"),
        ("12", "WhatsAppLoginPage",
         "Two-step login: enter phone number → enter OTP → get JWT token.",
         "POST /api/auth/send-otp, POST /api/auth/verify-otp"),
        ("13", "AdminLoginPage",
         "Admin password login page.",
         "POST /api/admin/login"),
        ("14", "AdminDashboardPage",
         "Full admin panel with 4 tabs: Products (add/edit/delete), Orders (view/update status), Discounts (create/toggle), Photos (approve/reject).",
         "Multiple admin endpoints"),
        ("15", "AboutUsPage",
         "Static page about the company.",
         "—"),
        ("16", "ContactUsPage",
         "Contact information and form.",
         "—"),
        ("17", "ShippingPolicyPage",
         "Shipping policy with delivery timelines.",
         "—"),
        ("18", "ReturnRefundPage",
         "Return and refund policy.",
         "—"),
        ("19", "PrivacyPolicyPage",
         "Privacy policy.",
         "—"),
        ("20", "FAQPage",
         "Frequently asked questions with accordion-style expandable answers.",
         "—"),
        ("21", "TermsOfServicePage",
         "Terms and conditions.",
         "—"),
        ("22", "UploadUserPhotosPage",
         "Page for customers to upload photos of themselves wearing products.",
         "POST /api/products/<id>/photos"),
        ("23–27", "MenPage, WomenPage, KidsPage, EthnicPage, WesternPage, PartyWearPage",
         "Category pages — all use ProductListPage with a category filter pre-applied.",
         "GET /api/products/?category=..."),
    ]

    page_data = [[
        Paragraph("<b>#</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold",
                                              textColor=colors.white, leading=12)),
        Paragraph("<b>Page</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold",
                                                 textColor=colors.white, leading=12)),
        Paragraph("<b>Description</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold",
                                                        textColor=colors.white, leading=12)),
        Paragraph("<b>API Calls</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold",
                                                      textColor=colors.white, leading=12)),
    ]]
    for num, name, desc, api in pages:
        page_data.append([
            Paragraph(num, ParagraphStyle("n", fontSize=9, fontName="Helvetica-Bold",
                                          textColor=BRAND_ACCENT, leading=12)),
            Paragraph(f'<font name="Courier" size="9">{name}</font>',
                      ParagraphStyle("p", fontSize=9, fontName="Courier", leading=12,
                                     textColor=BRAND_DARK)),
            Paragraph(desc, ParagraphStyle("d", fontSize=9, fontName="Helvetica", leading=12,
                                           textColor=GREY_TEXT)),
            Paragraph(f'<font name="Courier" size="8">{api}</font>',
                      ParagraphStyle("a", fontSize=8, fontName="Courier", leading=11,
                                     textColor=colors.HexColor("#555555"))),
        ])

    pt = Table(page_data, colWidths=[1*cm, 4*cm, 7*cm, 5.5*cm], repeatRows=1)
    pt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(pt)
    elems.append(PageBreak())
    return elems


def section6(s):
    elems = []
    elems.append(Paragraph("Section 6: How Key Features Work", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(4))

    # 3-Domain
    elems.append(Paragraph("3-Domain Pricing System", s["sub_heading"]))
    elems.append(hr())
    domain_steps = [
        "When the website loads, <b>DomainContext</b> reads <font name='Courier'>window.location.hostname</font>.",
        "It matches the hostname to one of 3 configs: <font name='Courier'>garba.shop</font> (B2C), <font name='Courier'>ttd.in</font> (B2B TTD), <font name='Courier'>maharashtra</font> (B2B MH).",
        "Each config has a <font name='Courier'>priceKey</font>: <font name='Courier'>price_b2c</font>, <font name='Courier'>price_b2b_ttd</font>, or <font name='Courier'>price_b2b_maharashtra</font>.",
        "Every API call to fetch products passes this <font name='Courier'>priceKey</font> as a query parameter.",
        "The backend reads the <font name='Courier'>priceKey</font> and returns the correct price column from the <font name='Courier'>productvariant</font> table.",
        "On localhost, a floating <b>DevDomainSwitcher</b> widget lets developers switch between domains for testing.",
    ]
    for i, step in enumerate(domain_steps, 1):
        elems.append(numbered_item(i, step, s))
    elems.append(sp(10))

    # WhatsApp Login
    elems.append(Paragraph("WhatsApp Login Flow", s["sub_heading"]))
    elems.append(hr())
    login_steps = [
        "User enters their 10-digit WhatsApp number.",
        "Frontend calls <font name='Courier'>POST /api/auth/send-otp</font> — backend creates user if not exists.",
        "OTP input field appears. (Demo: OTP is hardcoded as <b>1234</b> for presentation. Real WhatsApp OTP is future scope.)",
        "User enters 1234 and clicks Verify.",
        "Frontend calls <font name='Courier'>POST /api/auth/verify-otp</font> — backend validates OTP and returns JWT token.",
        "Token, user_id, and whatsapp_number are saved to <font name='Courier'>localStorage</font>.",
        "User is now logged in. <b>AuthGuard</b> protects cart, checkout, and my orders pages.",
    ]
    for i, step in enumerate(login_steps, 1):
        elems.append(numbered_item(i, step, s))
    elems.append(sp(10))

    # Cart & Checkout
    elems.append(Paragraph("Cart and Checkout Flow", s["sub_heading"]))
    elems.append(hr())
    cart_steps = [
        "User browses products and selects colour + size on <b>ProductDetailPage</b>.",
        "Clicks Add to Cart — <b>CartContext</b> calls <font name='Courier'>POST /api/cart/add</font> with <font name='Courier'>variant_id</font>.",
        "Cart is stored in both React Context (for instant UI updates) and MySQL database (for persistence).",
        "User goes to <b>CartPage</b> — items are loaded from database via <font name='Courier'>GET /api/cart</font>.",
        "User proceeds to <b>CheckoutPage</b> — fills in name, email, phone, address.",
        "Clicks Place Order — frontend calls <font name='Courier'>POST /api/orders/checkout</font>.",
        "Backend validates stock, calculates total, creates order with status <font name='Courier'>pending_payment</font>.",
        "On success: cart is cleared (<font name='Courier'>DELETE /api/cart/clear</font>), user is redirected to <b>OrderSuccessPage</b>.",
        "Admin can then update order status from the Admin Dashboard.",
    ]
    for i, step in enumerate(cart_steps, 1):
        elems.append(numbered_item(i, step, s))
    elems.append(sp(10))

    # Admin Dashboard
    elems.append(Paragraph("Admin Dashboard", s["sub_heading"]))
    elems.append(hr())
    admin_steps = [
        "Admin goes to <font name='Courier'>/admin-login</font> and enters password from <font name='Courier'>.env</font> file.",
        "Password is verified by <font name='Courier'>POST /api/admin/login</font> — returns a token stored in <font name='Courier'>localStorage</font>.",
        "<b>AdminGuard</b> component protects the <font name='Courier'>/admin</font> route — redirects to login if no token.",
        "Dashboard has 4 tabs:",
    ]
    for i, step in enumerate(admin_steps, 1):
        elems.append(numbered_item(i, step, s))
    tabs = [
        "<b>Products:</b> Add products with comma-separated colours and sizes (auto-generates all combinations). Edit product details. Delete products.",
        "<b>Orders:</b> View all orders, filter by status, update status (confirmed/packed/shipped/delivered), add tracking number.",
        "<b>Discounts:</b> Create percentage or flat discount codes with minimum cart value. Enable/disable codes.",
        "<b>Photos:</b> View customer-uploaded photos pending approval. Approve or reject each photo.",
    ]
    for tab in tabs:
        elems.append(bullet_item(tab, s, level=2))
    elems.append(sp(10))

    # Product Images
    elems.append(Paragraph("Product Images", s["sub_heading"]))
    elems.append(hr())
    img_points = [
        "Primary image is stored as <font name='Courier'>image_url</font> directly on the <font name='Courier'>product</font> table.",
        "Additional images are stored in the <font name='Courier'>productimage</font> table with <font name='Courier'>sort_order</font>.",
        "Customer-uploaded photos are stored as files in <font name='Courier'>backend/uploads/photos/</font> folder.",
        "The file path is saved in the <font name='Courier'>userphoto</font> table.",
        "Flask serves uploaded files via <font name='Courier'>GET /uploads/photos/&lt;filename&gt;</font>.",
        "Admin must approve customer photos before they appear on the product page.",
    ]
    for pt in img_points:
        elems.append(bullet_item(pt, s))
    elems.append(PageBreak())
    return elems


def section7(s):
    elems = []
    elems.append(Paragraph("Section 7: Project Folder Structure", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(4))

    elems.append(Paragraph("Root Folder", s["sub_heading"]))
    elems.append(hr())
    root_files = [
        ("index.html", "Entry HTML file for the React app"),
        ("vite.config.js", "Vite build configuration"),
        ("package.json", "Frontend dependencies and npm scripts"),
        ("eslint.config.js", "Code linting rules"),
        (".gitignore", "Files excluded from git"),
    ]
    for fname, desc in root_files:
        elems.append(bullet_item(
            f'<font name="Courier">{fname}</font> — {desc}', s
        ))
    elems.append(sp(10))

    elems.append(Paragraph("src/ — Frontend Source", s["sub_heading"]))
    elems.append(hr())
    src_files = [
        ("main.jsx", "React app entry point, wraps app with all Context providers"),
        ("App.jsx", "Main router with all page routes and AuthGuard/AdminGuard protection"),
        ("App.css, index.css", "Global styles"),
        ("pages/", "All 27 page components (one file per page)"),
        ("components/", "Reusable components: Header, Footer, ProductCard, Filters, AdminGuard, AuthGuard, DevDomainSwitcher, WhatsAppShare"),
        ("context/", "React Context providers: CartContext, WishlistContext, DomainContext"),
        ("assets/images/", "Static product images used in the app"),
    ]
    for fname, desc in src_files:
        elems.append(bullet_item(
            f'<font name="Courier">{fname}</font> — {desc}', s
        ))
    elems.append(sp(10))

    elems.append(Paragraph("backend/ — Backend Source", s["sub_heading"]))
    elems.append(hr())
    backend_files = [
        ("app.py", "Flask app factory, registers all blueprints, CORS config"),
        ("models.py", "All 14 SQLAlchemy database models"),
        ("config.py", "Database and app configuration loaded from .env"),
        ("init_db.py", "Script to create all database tables"),
        ("verify.py", "Utility script"),
        (".env", "Environment variables (DB credentials, admin password, secret key)"),
        ("routes/products.py", "Product listing, detail, reviews, photo upload"),
        ("routes/orders.py", "Checkout, order tracking, my orders"),
        ("routes/auth.py", "WhatsApp OTP login, JWT token generation"),
        ("routes/cart_orders.py", "Cart CRUD operations, discount code validation"),
        ("routes/admin_dashboard.py", "Admin product/order/discount/photo management"),
    ]
    for fname, desc in backend_files:
        elems.append(bullet_item(
            f'<font name="Courier">{fname}</font> — {desc}', s
        ))
    elems.append(PageBreak())
    return elems


def section8(s):
    elems = []
    elems.append(Paragraph("Section 8: Future Scope", s["section_heading"]))
    elems.append(accent_hr())
    elems.append(sp(4))
    elems.append(Paragraph(
        "The following features are planned for future development phases:",
        s["body"]
    ))
    elems.append(sp(8))

    future_items = [
        ("Real WhatsApp OTP",
         "Integrate WhatsApp Business API to send actual OTP messages instead of hardcoded 1234."),
        ("Online Payment Gateway",
         "Integrate Razorpay or PhonePe for UPI, card, and net banking payments."),
        ("Saved Addresses",
         "Use the existing address table to let users save and reuse delivery addresses."),
        ("Product Edit with Variants",
         "Admin can edit individual variant prices and stock quantities."),
        ("Courier Tracking API",
         "Integrate with Delhivery or Shiprocket API to show real-time courier tracking."),
        ("WhatsApp Order Notifications",
         "Send order confirmation and status update messages via WhatsApp Business API."),
        ("Push Notifications",
         "Browser push notifications for order updates."),
        ("Product Reviews with Photos",
         "Allow customers to attach photos to their reviews."),
        ("Bulk Product Import",
         "CSV/Excel upload for adding many products at once."),
        ("Analytics Dashboard",
         "Sales reports, revenue charts, top products for admin."),
    ]

    future_data = [[
        Paragraph("<b>#</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                              textColor=colors.white, leading=13)),
        Paragraph("<b>Feature</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                    textColor=colors.white, leading=13)),
        Paragraph("<b>Description</b>", ParagraphStyle("h", fontSize=10, fontName="Helvetica-Bold",
                                                        textColor=colors.white, leading=13)),
    ]]
    for i, (feat, desc) in enumerate(future_items, 1):
        future_data.append([
            Paragraph(str(i), ParagraphStyle("n", fontSize=10, fontName="Helvetica-Bold",
                                              textColor=BRAND_ACCENT, leading=13)),
            Paragraph(f"<b>{feat}</b>", ParagraphStyle("f", fontSize=10, fontName="Helvetica-Bold",
                                                         textColor=BRAND_DARK, leading=13)),
            Paragraph(desc, s["body"]),
        ])

    ft = Table(future_data, colWidths=[1*cm, 5*cm, 11.5*cm])
    ft.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elems.append(ft)
    elems.append(sp(20))

    # Closing note
    closing_data = [[
        Paragraph(
            "M&amp;M Fashion — Technical Documentation &nbsp;|&nbsp; "
            "Full-Stack E-Commerce Platform &nbsp;|&nbsp; "
            "React 19 + Flask + MySQL",
            ParagraphStyle("cl", fontSize=9, fontName="Helvetica",
                           textColor=colors.white, alignment=TA_CENTER, leading=14)
        )
    ]]
    closing_table = Table(closing_data, colWidths=[17*cm])
    closing_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
    ]))
    elems.append(closing_table)
    return elems


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE TEMPLATE — header/footer on every page
# ═══════════════════════════════════════════════════════════════════════════

def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4

    # Top accent bar
    canvas.setFillColor(BRAND_ACCENT)
    canvas.rect(0, h - 0.5*cm, w, 0.5*cm, fill=1, stroke=0)

    # Header text
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(BRAND_DARK)
    canvas.drawString(2*cm, h - 1.1*cm, "M&M Fashion — Technical Documentation")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(w - 2*cm, h - 1.1*cm, "Multi-Domain E-Commerce Platform")

    # Footer line
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.5*cm, w - 2*cm, 1.5*cm)

    # Page number
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(w / 2, 1*cm, f"Page {doc.page}")

    canvas.restoreState()


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        title="M&M Fashion — Technical Documentation",
        author="M&M Fashion Dev Team",
        subject="Multi-Domain E-Commerce Platform",
    )

    s = build_styles()
    story = []

    story += cover_page(s)
    story += toc_page(s)
    story += section1(s)
    story += section2(s)
    story += section3(s)
    story += section4(s)
    story += section5(s)
    story += section6(s)
    story += section7(s)
    story += section8(s)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF generated successfully: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
