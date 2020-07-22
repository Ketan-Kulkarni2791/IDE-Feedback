import smtplib
from email.mime.text import MIMEText


def send_email(customer, editor, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '8a378a5408b5e9'
    password = 'b4fa69488ec5c4'
    message = f"<h3>New Feedback Submission</h3>" \
              f"<ul><li>Customer : {customer}</li></ul>" \
              f"<ul><li>Editor : {editor}</li></ul>" \
              f"<ul><li>Rating : {rating}</li></ul>" \
              f"<ul><li>Comments : {comments}</li></ul>"

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

