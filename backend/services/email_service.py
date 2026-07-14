from flask_mail import Message
from extensions import mail


def send_email(
    subject,
    recipients,
    body=None,
    html=None,
    attachment_path=None
):
    """
    Send email with optional HTML content and attachment.
    """

    msg = Message(
        subject=subject,
        recipients=recipients
    )

    if body:
        msg.body = body

    if html:
        msg.html = html

    if attachment_path:

        with open(attachment_path, "rb") as file:

            msg.attach(
                filename=attachment_path.split("\\")[-1],
                content_type="text/csv",
                data=file.read()
            )

    mail.send(msg)