from flask import Flask, request, jsonify
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from fpdf import FPDF
import tempfile
import requests

app = Flask(__name__)

# Environment Variables (set these in Render or local .env)
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # Example: 'mds66027@gmail.com'
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Example: '1234567890'

# ========= Helper: Generate PDF from Sheet ==========
def create_pdf_from_sheet(sheet_id):
    sheet_url = f"https://docs.google.com/spreadsheets/d/1-SAWcbnx_L-cwMuZuc0gjBtuC706BFDNKQpCiSP7zHw/export?format=csv"
    response = requests.get(sheet_url)

    if response.status_code != 200:
        raise Exception("Failed to fetch Google Sheet data. Check permissions.")

    lines = response.text.splitlines()
    headers = lines[0].split(',')
    values = lines[1].split(',')

    data = dict(zip(headers, values))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Student Details", ln=True, align='C')
    pdf.ln(10)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(tmp_file.name)
    return tmp_file.name

# ========= Helper: Send Email ==========
def send_email_with_pdf(to_email, pdf_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = 'Your Student Details PDF'

    body = MIMEText('Attached is your Student Details PDF.', 'plain')
    msg.attach(body)

    with open(pdf_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name='student_details.pdf')
        part['Content-Disposition'] = 'attachment; filename="student_details.pdf"'
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# ========= Routes ==========
@app.route('/')
def home():
    return "Form to PDF Backend is Running!"

@app.route('/generate-pdf')
def generate_pdf():
    sheet_id = request.args.get('sheetId')
    email = request.args.get('email')

    if not sheet_id or not email:
        return jsonify({'error': 'Missing sheetId or email'}), 400

    try:
        pdf_path = create_pdf_from_sheet(sheet_id)
        send_email_with_pdf(email, pdf_path)
        return jsonify({'message': 'PDF generated and sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========= Main ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
