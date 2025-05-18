from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_pdf_from_sheet(sheet_id):
    # Simulated student data
    data = {
        'Name': 'John Doe',
        'DOB': '2005-06-15',
        'Father': 'Richard Roe',
        'Mother': 'Jane Roe',
        'Roll No': '23',
        'Class': '10',
        'Subject': 'Maths',
        'School': 'ABC High School',
        'Address': '123 Street, City'
    }

    pdf_path = '/tmp/student_details.pdf'
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Student Details")
    c.setFont("Helvetica", 12)
    y = 770
    for key, value in data.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20
    c.save()
    return pdf_path