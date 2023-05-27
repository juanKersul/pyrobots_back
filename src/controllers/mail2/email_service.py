from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config
MAIL_USERNAME_S = config("MAIL_USERNAME")
MAIL_PASSWORD_S = config("MAIL_PASSWORD")
MAIL_PORT_S = config("MAIL_PORT")
MAIL_SERVER_S = config("MAIL_SERVER")


async def send_confirmation_mail(
        email: str,
        code_validation: str,
        username: str):
    """Envía mail de confirmación.

    Args:
        email (str): email al que enviar la confirmación.
        code_validation (str): código a enviar.
        username (str): usuario al que enviar.
    """
    conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME_S,
        MAIL_PASSWORD=MAIL_PASSWORD_S,
        MAIL_FROM=email,
        MAIL_PORT=MAIL_PORT_S,
        MAIL_SERVER=MAIL_SERVER_S,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
    )
    html = open("controllers/mail2/email.html", "r")
    template = html.read().format(
        user=username,
        end_point_verify=code_validation)
    message = MessageSchema(
        subject="Mail de confirmación pyRobots",
        recipients=[email],
        body=template,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
