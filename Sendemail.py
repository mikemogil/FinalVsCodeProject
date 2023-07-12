import ssl, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import config



def _send_email(to_addy, body: str, subject: str,  *, 
                        from_addy: str = config.from_add, attachments=None):
    if config.API_DEBUG:
        to_addy = config.dev_email
        subject = f"Debug: {subject}"


    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_addy
    message['To'] = to_addy

    message.attach(MIMEText(body, 'html'))

    for attachment in attachments or []:
        message.attach(attachment)

    # context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

    with smtplib.SMTP(host='192.168.10.22', port=25) as mail:
        # mail.starttls(context=context)
        # mail.login(user=user_name, password=password)
        mail.sendmail(from_addr=from_addy, to_addrs=to_addy, msg=message.as_string())
