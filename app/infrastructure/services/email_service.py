import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:

    def send_activation_email(self, to_email: str, token: str):
        activation_link = (
            f"http://localhost:8000/users/activate?token={token}"
        )

        msg = MIMEMultipart()
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = to_email
        msg["Subject"] = "Activá tu cuenta"

        body = f"""
        Hola 💙

        Gracias por registrarte.
        Para activar tu cuenta hacé click en el siguiente link:

        {activation_link}

        Si no fuiste vos, ignorá este mail.
        """

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(
            os.getenv("SMTP_HOST"),
            int(os.getenv("SMTP_PORT"))
        ) as server:
            server.starttls()
            server.login(
                os.getenv("SMTP_USER"),
                os.getenv("SMTP_PASSWORD")
            )
            server.send_message(msg)
