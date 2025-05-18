from flask import Flask, request, send_file
import pdf_generator
import send_email

app = Flask(__name__)

# Add this route to handle root URL
@app.route('/')
def home():
    return "Form to PDF Backend is Running!"

@app.route('/generate-pdf')
def generate_pdf():
    sheet_id = request.args.get('sheetId')
    email = request.args.get('email')
    pdf_path = pdf_generator.create_pdf_from_sheet(sheet_id)
    send_email.send_email_with_pdf(email, pdf_path)
    return "PDF generated and sent via email."

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
