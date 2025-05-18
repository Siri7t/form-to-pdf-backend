import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

EMAIL_ADDRESS = 'mds66027@gmail.com'
EMAIL_PASSWORD = 'mjwl nonh fevy bxih'

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
