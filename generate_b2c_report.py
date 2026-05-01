from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUT = "B2C_FLOW_ANALYSIS.pdf"

RED    = colors.HexColor("#e74c3c")
ORANGE = colors.HexColor("#e67e22")
GREEN  = colors.HexColor("#27ae60")
BLUE   = colors.HexColor("#2980b9")
DARK   = colors.HexColor("#1a1a2e")
ACCENT = colors.HexColor("#e94560")
LGREY  = colors.HexColor("#cccccc")
BGROW1 = colors.HexColor("#fafafa")
BGROW2 = colors.white
THDR   = colors.HexColor("#2d2d44")
GREY   = colors.HexColor("#555555")

def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontSize=28, textColor=colors.white,
            alignment=TA_CENTER, fontName="Helvetica-Bold", leading=36, spaceAfter=6),
        "sub": ParagraphStyle("sub", parent=base["Normal"], fontSize=13, textColor=colors.HexColor("#dddddd"),
            alignment=TA_CENTER, fontName="Helvetica", leading=18),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontSize=17, textColor=ACCENT,
            fontName="Helvetica-Bold", spaceBefore=16, spaceAfter=5, leading=22),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontSize=13, textColor=DARK,
            fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4, leading=18),
        "h3": ParagraphStyle("h3", parent=base["Heading3"], fontSize=11, textColor=DARK,
            fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3, leading=15),
        "body": ParagraphStyle("body", parent=base["Normal"], fontSize=10, textColor=GREY,
            fontName="Helvetica", spaceAfter=4, leading=15, alignment=TA_JUSTIFY),
        "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=10, textColor=GREY,
            fontName="Helvetica", spaceAfter=3, leading=15, leftIndent=14),
        "bullet2": ParagraphStyle("bullet2", parent=base["Normal"], fontSize=9.5, textColor=GREY,
            fontName="Helvetica", spaceAfter=2, leading=14, leftIndent=28),
        "issue": ParagraphStyle("issue", parent=base["Normal"], fontSize=10, textColor=RED,
            fontName="Helvetica-Bold", spaceAfter=3, leading=15, leftIndent=14),
        "fix": ParagraphStyle("fix", parent=base["Normal"], fontSize=10, textColor=GREEN,
            fontName="Helvetica-Bold", spaceAfter=3, leading=15, leftIndent=14),
        "code": ParagraphStyle("code", parent=base["Normal"], fontSize=9, textColor=colors.HexColor("#c0392b"),
            fontName="Courier", leading=13),
    }

def hr():
    return HRFlowable(width="100%", thickness=1, color=LGREY, spaceAfter=6, spaceBefore=4)

def ahr():
    return HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=8, spaceBefore=2)

def sp(h=8):
    return Spacer(1, h)

def b(text, s):
    return Paragraph(f"\u2022  {text}", s["bullet"])

def b2(text, s):
    return Paragraph(f"\u25e6  {text}", s["bullet2"])

def issue(text, s):
    return Paragraph(f"\u274c  {text}", s["issue"])

def fix(text, s):
    return Paragraph(f"\u2705  {text}", s["fix"])

def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(ACCENT)
    canvas.rect(0, h - 0.5*cm, w, 0.5*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(DARK)
    canvas.drawString(2*cm, h - 1.1*cm, "M&M Fashion — B2C Flow Analysis & Issue Report")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(w - 2*cm, h - 1.1*cm, "Confidential — For Internal Review")
    canvas.setStrokeColor(LGREY)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.5*cm, w - 2*cm, 1.5*cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(w / 2, 1*cm, f"Page {doc.page}")
    canvas.restoreState()

def cover(s):
    elems = []
    d = [[Paragraph("M&amp;M Fashion", s["title"])]]
    t = Table(d, colWidths=[17*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
        ("TOPPADDING",(0,0),(-1,-1),36),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),20),("RIGHTPADDING",(0,0),(-1,-1),20)]))
    elems.append(t)
    d2 = [[Paragraph("B2C Flow Analysis, Issues &amp; Improvement Plan", s["sub"])]]
    t2 = Table(d2, colWidths=[17*cm])
    t2.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#16213e")),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("LEFTPADDING",(0,0),(-1,-1),20),("RIGHTPADDING",(0,0),(-1,-1),20)]))
    elems.append(t2)
    elems.append(sp(24))
    rows = [
        ["Purpose", "Identify all B2C UX issues and define the correct flow"],
        ["Audience", "Development team and project evaluator"],
        ["Scope", "garba.shop — B2C retail domain only"],
        ["Date", "April 2026"],
        ["Status", "Issues identified — fixes pending implementation"],
    ]
    cs = ParagraphStyle("cs", fontSize=10, fontName="Helvetica", textColor=GREY, leading=14)
    ls = ParagraphStyle("ls", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, leading=14)
    td = [[Paragraph(r[0], ls), Paragraph(r[1], cs)] for r in rows]
    it = Table(td, colWidths=[5*cm, 12*cm])
    it.setStyle(TableStyle([("ROWBACKGROUNDS",(0,0),(-1,-1),[BGROW1,BGROW2]),
        ("GRID",(0,0),(-1,-1),0.4,LGREY),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10)]))
    elems.append(it)
    elems.append(PageBreak())
    return elems

def section_current_flow(s):
    elems = []
    elems.append(Paragraph("Section 1: What is B2C and the Correct User Journey", s["h1"]))
    elems.append(ahr())
    elems.append(Paragraph(
        "B2C (Business to Consumer) means selling directly to end customers at retail prices. "
        "On this platform, the B2C domain is <font name='Courier'>garba.shop</font>. "
        "The correct B2C user journey should follow a strict linear flow with no confusion or repeated steps.",
        s["body"]))
    elems.append(sp())

    elems.append(Paragraph("The Correct B2C Flow (Standard E-Commerce)", s["h2"]))
    elems.append(hr())

    steps = [
        ("Step 1", "Home Page", "User lands on homepage. Sees hero banner, featured products, promo offers."),
        ("Step 2", "Browse / Search", "User browses categories or searches for products."),
        ("Step 3", "Product Detail Page", "User views product — images, price, colour, size. Selects variant. Clicks Add to Cart."),
        ("Step 4", "Cart Page", "User reviews cart items, quantities, total. Applies coupon code HERE (only once). Proceeds to checkout."),
        ("Step 5", "Login (if not logged in)", "If user is not logged in, redirect to WhatsApp login. After login, return to checkout."),
        ("Step 6", "Checkout Page", "User fills name, email, phone, address. Reviews order summary. Clicks Place Order."),
        ("Step 7", "Order Success Page", "Confirmation shown with order ID, total, estimated delivery. Option to track order."),
        ("Step 8", "My Orders / Track Order", "User can view all past orders and track current order status."),
    ]

    hdr = [
        Paragraph("<b>Step</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
        Paragraph("<b>Page</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
        Paragraph("<b>What Should Happen</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
    ]
    rows = [hdr]
    for step, page, desc in steps:
        rows.append([
            Paragraph(f"<b>{step}</b>", ParagraphStyle("s", fontSize=9, fontName="Helvetica-Bold", textColor=ACCENT, leading=12)),
            Paragraph(f"<font name='Courier' size='9'>{page}</font>", ParagraphStyle("p", fontSize=9, fontName="Courier", leading=12, textColor=DARK)),
            Paragraph(desc, ParagraphStyle("d", fontSize=9, fontName="Helvetica", leading=12, textColor=GREY)),
        ])
    t = Table(rows, colWidths=[2*cm, 4*cm, 11.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),THDR),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BGROW1,BGROW2]),
        ("GRID",(0,0),(-1,-1),0.4,LGREY),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    elems.append(t)
    elems.append(PageBreak())
    return elems


def section_issues(s):
    elems = []
    elems.append(Paragraph("Section 2: Current Issues and Faults Found", s["h1"]))
    elems.append(ahr())
    elems.append(Paragraph(
        "After reviewing the complete codebase, the following issues were identified that prevent "
        "the B2C flow from working correctly as a professional e-commerce platform.",
        s["body"]))
    elems.append(sp())

    # Issue 1
    elems.append(KeepTogether([
        Paragraph("Issue 1 — Discount Code on Product Detail Page (Critical UX Problem)", s["h2"]),
        hr(),
        Paragraph(
            "The <font name='Courier'>ProductDetailPage.jsx</font> has a full discount code input field "
            "with an Apply button. This is wrong. Discount codes should only be applied in the Cart or Checkout — "
            "not on the product page.",
            s["body"]),
        sp(4),
        issue("Discount code input appears on the product detail page before the user has even added to cart", s),
        issue("If user applies a code here, the discount is calculated on a single item price — not the cart total", s),
        issue("The discount applied here is NOT carried to the cart or checkout — it is lost completely", s),
        issue("This confuses the user — they think they got a discount but the cart shows full price", s),
        issue("Standard e-commerce (Flipkart, Amazon, Myntra) never shows coupon input on product pages", s),
        sp(4),
        Paragraph("<b>Where it should be:</b> Only in CartPage and/or CheckoutPage — applied to the full cart total.", s["body"]),
        sp(8),
    ]))

    # Issue 2
    elems.append(KeepTogether([
        Paragraph("Issue 2 — Discount Code Appears in Both Cart AND Checkout (Duplication)", s["h2"]),
        hr(),
        Paragraph(
            "The discount code input exists in both <font name='Courier'>CartPage.jsx</font> AND "
            "<font name='Courier'>CheckoutPage.jsx</font>. This creates confusion.",
            s["body"]),
        sp(4),
        issue("User applies a coupon in CartPage — discount is shown in cart total", s),
        issue("User proceeds to CheckoutPage — the discount is NOT carried over from cart to checkout", s),
        issue("Checkout shows a fresh discount input — user has to apply the code again", s),
        issue("If user applies a different code in checkout, it overrides the cart discount silently", s),
        issue("The two discount states are completely independent — no shared state between pages", s),
        sp(4),
        Paragraph("<b>Correct approach:</b> Apply coupon ONCE in CartPage. Pass the applied discount code to CheckoutPage via navigation state or context. Checkout should show the applied discount as read-only, not ask again.", s["body"]),
        sp(8),
    ]))

    # Issue 3
    elems.append(KeepTogether([
        Paragraph("Issue 3 — No Review Submission Form for Customers", s["h2"]),
        hr(),
        Paragraph(
            "The <font name='Courier'>ProductDetailPage.jsx</font> shows existing reviews but has NO form "
            "for customers to submit a new review. The backend API <font name='Courier'>POST /api/products/&lt;id&gt;/reviews</font> "
            "exists but is never called from the frontend.",
            s["body"]),
        sp(4),
        issue("Customers can see reviews but cannot write one", s),
        issue("The review submission API endpoint exists in backend but is unused", s),
        issue("No star rating selector, no comment box, no submit button on the product page", s),
        sp(8),
    ]))

    # Issue 4
    elems.append(KeepTogether([
        Paragraph("Issue 4 — WhatsApp Number Field in Checkout is Optional but Confusing", s["h2"]),
        hr(),
        Paragraph(
            "The checkout form has a separate 'WhatsApp Number' field labelled 'If different from phone'. "
            "But the user already logged in with their WhatsApp number. This field should be auto-filled "
            "from localStorage.",
            s["body"]),
        sp(4),
        issue("User already logged in with WhatsApp — asking again is redundant and confusing", s),
        issue("If user leaves it blank, the order is not linked to their account (user_id stays null)", s),
        issue("The whatsapp_number from localStorage should be auto-populated in this field", s),
        sp(8),
    ]))

    # Issue 5
    elems.append(KeepTogether([
        Paragraph("Issue 5 — Cart Quantity Update Does Not Sync to Database", s["h2"]),
        hr(),
        Paragraph(
            "In <font name='Courier'>CartContext.jsx</font>, the <font name='Courier'>updateQuantity</font> "
            "function only updates the React state locally. It does NOT call any backend API to update "
            "the quantity in the database.",
            s["body"]),
        sp(4),
        issue("User increases quantity in cart — React state updates but DB still has old quantity", s),
        issue("If user refreshes the page, cart reloads from DB and shows the old quantity", s),
        issue("No PUT /api/cart/update endpoint exists in the backend", s),
        sp(8),
    ]))

    # Issue 6
    elems.append(KeepTogether([
        Paragraph("Issue 6 — Order Success Page Uses localStorage Instead of API", s["h2"]),
        hr(),
        Paragraph(
            "The <font name='Courier'>OrderSuccessPage.jsx</font> reads order details from "
            "<font name='Courier'>localStorage.getItem('lastOrder')</font>. If the user refreshes "
            "the page or clears storage, the page redirects to home and the order confirmation is lost.",
            s["body"]),
        sp(4),
        issue("Order details are stored in localStorage — not fetched from the database", s),
        issue("Refreshing the order success page redirects to home — user loses confirmation", s),
        issue("Should fetch order details from GET /api/orders/track/<order_id> instead", s),
        sp(8),
    ]))

    # Issue 7
    elems.append(KeepTogether([
        Paragraph("Issue 7 — Hero Banner Uses External Unsplash Image", s["h2"]),
        hr(),
        Paragraph(
            "The homepage hero banner uses a hardcoded Unsplash URL. In production this will fail "
            "if the external image is unavailable, and it shows a generic fashion photo unrelated to the brand.",
            s["body"]),
        sp(4),
        issue("Hero image is from Unsplash — not a brand image", s),
        issue("Will fail in production if Unsplash is blocked or image is removed", s),
        issue("The 'SHOP THE LOOK' button on the hero has no navigation — it does nothing", s),
        sp(8),
    ]))

    # Issue 8
    elems.append(KeepTogether([
        Paragraph("Issue 8 — Search Results Page Does Not Pass price_key", s["h2"]),
        hr(),
        Paragraph(
            "The <font name='Courier'>SearchResultsPage.jsx</font> fetches products but does NOT pass "
            "<font name='Courier'>price_key</font> in the API call. This means search results always "
            "show B2C prices regardless of the active domain.",
            s["body"]),
        sp(4),
        issue("Search results always show price_b2c even when domain is ttd.in or maharashtra", s),
        issue("Inconsistent pricing between search results and product listing pages", s),
        sp(8),
    ]))

    # Issue 9
    elems.append(KeepTogether([
        Paragraph("Issue 9 — Footer Has a Dead Link (/whatsapp-support)", s["h2"]),
        hr(),
        Paragraph(
            "The Footer has a 'WhatsApp Support' link pointing to "
            "<font name='Courier'>/whatsapp-support</font> which does not exist as a route in App.jsx.",
            s["body"]),
        sp(4),
        issue("Clicking WhatsApp Support in footer leads to 404 page", s),
        issue("Should either link to /contact-us or open a WhatsApp chat link directly", s),
        sp(8),
    ]))

    # Issue 10
    elems.append(KeepTogether([
        Paragraph("Issue 10 — No Pincode/State Validation in Checkout", s["h2"]),
        hr(),
        Paragraph(
            "The checkout form accepts any value in pincode and state fields with no validation. "
            "A user can enter '1' as a pincode and the order will be placed.",
            s["body"]),
        sp(4),
        issue("Pincode field accepts any text — no 6-digit validation", s),
        issue("Phone number field accepts any text — no 10-digit validation", s),
        issue("Email field has type='email' but no custom validation message", s),
        sp(8),
    ]))

    elems.append(PageBreak())
    return elems


def section_proper_flow(s):
    elems = []
    elems.append(Paragraph("Section 3: Proper B2C Flow — How It Should Work", s["h1"]))
    elems.append(ahr())
    elems.append(Paragraph(
        "This section defines the correct, complete B2C flow that should be implemented "
        "for a professional e-commerce experience.",
        s["body"]))
    elems.append(sp())

    # Flow 1
    elems.append(Paragraph("3.1  Product Detail Page — Correct Structure", s["h2"]))
    elems.append(hr())
    elems.append(Paragraph("What should be on the product detail page:", s["body"]))
    correct = [
        "Product images gallery with thumbnail navigation",
        "Product name, category, price (from correct domain price column)",
        "Colour selector — clickable circles, one per unique colour",
        "Size selector — clickable buttons, filtered by selected colour",
        "Stock indicator — 'Only X left' when stock is below 5",
        "Quantity selector (+ / - buttons)",
        "Add to Cart button — disabled until colour AND size are selected",
        "Add to Wishlist button",
        "WhatsApp Share button",
        "Product description, fabric, occasion, pattern details",
        "Customer reviews section with star ratings",
        "Write a Review form (star selector + comment box + submit)",
        "Customer photos section (approved photos only)",
        "Upload Your Photo link",
    ]
    wrong = [
        "Discount code input field — REMOVE THIS from product page",
    ]
    for c in correct:
        elems.append(fix(c, s))
    elems.append(sp(4))
    for w in wrong:
        elems.append(issue(w, s))
    elems.append(sp(10))

    # Flow 2
    elems.append(Paragraph("3.2  Cart Page — Correct Structure", s["h2"]))
    elems.append(hr())
    elems.append(Paragraph("What should be on the cart page:", s["body"]))
    cart_correct = [
        "List of all cart items with image, name, colour, size, quantity",
        "Quantity increase/decrease buttons — synced to database on change",
        "Remove item button — removes from DB and context",
        "Move to Wishlist button",
        "Price breakdown: subtotal, discount, delivery, total",
        "Coupon code input — ONE place only, applied to full cart total",
        "Free shipping indicator (free above Rs.999)",
        "Proceed to Checkout button — passes applied discount code to checkout",
        "Continue Shopping link",
    ]
    cart_wrong = [
        "Do NOT have a second coupon input in CheckoutPage — remove it from there",
        "Quantity update must call PUT /api/cart/update to sync with database",
    ]
    for c in cart_correct:
        elems.append(fix(c, s))
    elems.append(sp(4))
    for w in cart_wrong:
        elems.append(issue(w, s))
    elems.append(sp(10))

    # Flow 3
    elems.append(Paragraph("3.3  Checkout Page — Correct Structure", s["h2"]))
    elems.append(hr())
    elems.append(Paragraph("What should be on the checkout page:", s["body"]))
    co_correct = [
        "Contact details: name, email, phone (auto-fill from localStorage if logged in)",
        "WhatsApp number: auto-filled from localStorage — not a separate manual field",
        "Shipping address: line1, line2, city, state, pincode with validation",
        "Pincode: must be exactly 6 digits",
        "Phone: must be exactly 10 digits",
        "Order summary (read-only): items, quantities, prices",
        "Price breakdown: subtotal, discount (from cart — read-only), shipping, total",
        "If discount was applied in cart — show it here as already applied, no new input",
        "Payment method: Cash on Delivery (clearly shown)",
        "Place Order button",
    ]
    co_wrong = [
        "Remove the discount code input from CheckoutPage — it already exists in CartPage",
        "Do not ask for WhatsApp number again — auto-fill from localStorage",
    ]
    for c in co_correct:
        elems.append(fix(c, s))
    elems.append(sp(4))
    for w in co_wrong:
        elems.append(issue(w, s))
    elems.append(sp(10))

    # Flow 4
    elems.append(Paragraph("3.4  Order Success Page — Correct Structure", s["h2"]))
    elems.append(hr())
    os_correct = [
        "Fetch order details from GET /api/orders/track/<order_id> — not from localStorage",
        "Show order ID, date, total, payment method, estimated delivery",
        "Show COD reminder message",
        "Track Order button linking to /trackorder/<order_id>",
        "Continue Shopping button",
        "Page should work even after browser refresh",
    ]
    for c in os_correct:
        elems.append(fix(c, s))
    elems.append(sp(10))

    elems.append(PageBreak())
    return elems


def section_fixes(s):
    elems = []
    elems.append(Paragraph("Section 4: Fix Plan — What Needs to Be Done", s["h1"]))
    elems.append(ahr())

    fixes = [
        ("Fix 1", "HIGH", "Remove discount code from ProductDetailPage.jsx",
         "Delete the entire discount code section (state, input, apply button) from ProductDetailPage. Discount belongs only in CartPage."),
        ("Fix 2", "HIGH", "Remove discount code from CheckoutPage.jsx",
         "Delete the discount code section from CheckoutPage. Pass the applied discount from CartPage to CheckoutPage via React Router navigation state (location.state.discount)."),
        ("Fix 3", "HIGH", "Add cart quantity update API call",
         "Add PUT /api/cart/update endpoint in backend. Call it from CartContext.updateQuantity() so quantity changes sync to database."),
        ("Fix 4", "MEDIUM", "Auto-fill WhatsApp number in checkout",
         "In CheckoutPage, read whatsapp_number from localStorage on mount and pre-fill the form field. Remove the 'If different from phone' label."),
        ("Fix 5", "MEDIUM", "Add review submission form to ProductDetailPage",
         "Add a star rating selector and comment textarea below the reviews list. On submit, call POST /api/products/<id>/reviews with rating, comment, and whatsapp_number from localStorage."),
        ("Fix 6", "MEDIUM", "Fix OrderSuccessPage to fetch from API",
         "Pass order_id via navigation state. On mount, call GET /api/orders/track/<order_id> to load order details. Remove dependency on localStorage."),
        ("Fix 7", "MEDIUM", "Add price_key to SearchResultsPage",
         "Import useDomain in SearchResultsPage. Add price_key to the API query params so search results show correct domain prices."),
        ("Fix 8", "LOW", "Fix footer WhatsApp Support link",
         "Change /whatsapp-support to a direct WhatsApp link: https://wa.me/91XXXXXXXXXX or link to /contact-us."),
        ("Fix 9", "LOW", "Add form validation in CheckoutPage",
         "Validate pincode is exactly 6 digits, phone is exactly 10 digits before allowing order placement."),
        ("Fix 10", "LOW", "Replace hero image with brand image",
         "Replace the Unsplash URL with a local brand image from src/assets/images/. Wire the SHOP THE LOOK button to /products."),
    ]

    hdr = [
        Paragraph("<b>#</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
        Paragraph("<b>Priority</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
        Paragraph("<b>Fix</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
        Paragraph("<b>Description</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
    ]
    rows = [hdr]
    priority_colors = {"HIGH": RED, "MEDIUM": ORANGE, "LOW": GREEN}
    for fix_id, priority, title, desc in fixes:
        pc = priority_colors.get(priority, GREY)
        rows.append([
            Paragraph(f"<b>{fix_id}</b>", ParagraphStyle("fi", fontSize=9, fontName="Helvetica-Bold", textColor=ACCENT, leading=12)),
            Paragraph(f"<font color='{pc.hexval()}'><b>{priority}</b></font>",
                      ParagraphStyle("pr", fontSize=9, fontName="Helvetica-Bold", leading=12)),
            Paragraph(f"<b>{title}</b>", ParagraphStyle("ti", fontSize=9, fontName="Helvetica-Bold", textColor=DARK, leading=12)),
            Paragraph(desc, ParagraphStyle("de", fontSize=9, fontName="Helvetica", textColor=GREY, leading=12)),
        ])
    t = Table(rows, colWidths=[1.5*cm, 2*cm, 5.5*cm, 8.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),THDR),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BGROW1,BGROW2]),
        ("GRID",(0,0),(-1,-1),0.4,LGREY),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    elems.append(t)
    elems.append(PageBreak())
    return elems


def section_future(s):
    elems = []
    elems.append(Paragraph("Section 5: Future Scope for Complete B2C Platform", s["h1"]))
    elems.append(ahr())
    elems.append(Paragraph(
        "The following features are NOT currently built but are required for a complete, "
        "production-ready B2C e-commerce platform.",
        s["body"]))
    elems.append(sp())

    future = [
        ("Real WhatsApp OTP", "HIGH", "Currently OTP is hardcoded as 1234. Integrate WhatsApp Business API to send real OTPs."),
        ("Online Payment Gateway", "HIGH", "Integrate Razorpay or PhonePe for UPI, card, net banking. Currently only COD is supported."),
        ("Saved Addresses", "MEDIUM", "Let users save multiple delivery addresses. The address table exists in DB but is unused."),
        ("Order Cancellation", "MEDIUM", "Allow customers to cancel orders from My Orders page within a time window."),
        ("Return Request Flow", "MEDIUM", "Allow customers to raise a return request from My Orders. Currently only a static policy page exists."),
        ("Product Sorting", "MEDIUM", "The sort dropdown on ProductListPage exists but does nothing — wire it to sort by price or date."),
        ("Pincode Serviceability Check", "MEDIUM", "Check if delivery is available to the entered pincode before placing order."),
        ("Email Order Confirmation", "LOW", "Send order confirmation email to customer after successful order placement."),
        ("Product Recommendations", "LOW", "Show 'You may also like' section on product detail page based on category."),
        ("Recently Viewed Products", "LOW", "Track and show recently viewed products on homepage or product pages."),
        ("Courier Tracking Integration", "LOW", "Integrate Delhivery or Shiprocket API for real-time shipment tracking."),
        ("Admin Product Image Upload", "LOW", "Currently admin enters image URLs manually. Add file upload support."),
    ]

    hdr = [
        Paragraph("<b>Feature</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
        Paragraph("<b>Priority</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
        Paragraph("<b>Description</b>", ParagraphStyle("h", fontSize=9, fontName="Helvetica-Bold", textColor=colors.white, leading=12)),
    ]
    rows = [hdr]
    priority_colors = {"HIGH": RED, "MEDIUM": ORANGE, "LOW": GREEN}
    for feat, priority, desc in future:
        pc = priority_colors.get(priority, GREY)
        rows.append([
            Paragraph(f"<b>{feat}</b>", ParagraphStyle("fe", fontSize=9, fontName="Helvetica-Bold", textColor=DARK, leading=12)),
            Paragraph(f"<font color='{pc.hexval()}'><b>{priority}</b></font>",
                      ParagraphStyle("pr", fontSize=9, fontName="Helvetica-Bold", leading=12)),
            Paragraph(desc, ParagraphStyle("de", fontSize=9, fontName="Helvetica", textColor=GREY, leading=12)),
        ])
    t = Table(rows, colWidths=[5*cm, 2*cm, 10.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),THDR),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BGROW1,BGROW2]),
        ("GRID",(0,0),(-1,-1),0.4,LGREY),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    elems.append(t)
    elems.append(sp(20))

    closing = [[Paragraph(
        "M&amp;M Fashion — B2C Flow Analysis &nbsp;|&nbsp; garba.shop &nbsp;|&nbsp; April 2026",
        ParagraphStyle("cl", fontSize=9, fontName="Helvetica", textColor=colors.white, alignment=TA_CENTER, leading=14))]]
    ct = Table(closing, colWidths=[17*cm])
    ct.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
        ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
        ("LEFTPADDING",(0,0),(-1,-1),20),("RIGHTPADDING",(0,0),(-1,-1),20)]))
    elems.append(ct)
    return elems


def main():
    doc = SimpleDocTemplate(OUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="M&M Fashion B2C Flow Analysis",
        author="M&M Fashion Dev Team")
    s = styles()
    story = []
    story += cover(s)
    story += section_current_flow(s)
    story += section_issues(s)
    story += section_proper_flow(s)
    story += section_fixes(s)
    story += section_future(s)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"Generated: {OUT}")

if __name__ == "__main__":
    main()
