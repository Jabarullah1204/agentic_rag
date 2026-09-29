from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from pathlib import Path


output_folder = Path("pdf_knowledge")
output_folder.mkdir(exist_ok=True)


policies = {
    "refund_policy.pdf": (
        "Refund Policy",
        [
            "Customers can request a refund within 7 days of receiving the product.",
            "The product must be unused and returned in its original packaging.",
            "Refund requests are reviewed by the support team.",
            "Once approved, the refund is processed within 5 business days.",
        ],
    ),
    "shipping_policy.pdf": (
        "Shipping Policy",
        [
            "Standard shipping usually takes 3 to 5 business days.",
            "If an order has not arrived after 7 business days, the customer should contact the support team.",
            "The support team will check the shipment status and provide an update.",
        ],
    ),
    "warranty_policy.pdf": (
        "Warranty Policy",
        [
            "Electronics products are covered by a 12-month warranty.",
            "Customers should report a damaged product within 7 days of receiving it.",
            "After verification, eligible products may be replaced.",
            "Physical damage caused by the customer is not covered under the warranty.",
        ],
    ),
}


def create_pdf(filename, title, lines):
    file_path = output_folder / filename

    pdf = canvas.Canvas(str(file_path), pagesize=A4)

    width, height = A4
    y = height - 1 * inch

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(1 * inch, y, title)

    y -= 0.5 * inch

    pdf.setFont("Helvetica", 11)

    for line in lines:
        words = line.split()
        current_line = ""

        for word in words:
            test_line = current_line + word + " "

            if pdf.stringWidth(test_line, "Helvetica", 11) < 6.5 * inch:
                current_line = test_line
            else:
                pdf.drawString(1 * inch, y, current_line.strip())
                y -= 0.25 * inch
                current_line = word + " "

        pdf.drawString(1 * inch, y, current_line.strip())
        y -= 0.4 * inch

    pdf.save()

    print(f"Created: {file_path}")


for filename, (title, lines) in policies.items():
    create_pdf(filename, title, lines)

print("\nAll policy PDFs created successfully.")