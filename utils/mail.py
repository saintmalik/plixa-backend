import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from pathlib import Path
from typing import Union, Optional

import jinja2
from pydantic import BaseModel, EmailStr, field_validator

from settings import SMTPSettings

MAX_RECIPIENTS = 5_000


class File(BaseModel):
    """Model for attachment files"""

    name: str
    content: BytesIO

    class Config:
        arbitrary_types_allowed = True


Attachment = Union[Path, File]


class Recipient(BaseModel):
    """A model used to build the email for a single recipient

    Attributes
        email: The email address with the email is sent to.
        context: A dict of data specific to the recipient used
        to build the user's personalized email
        attachments: Attachments specific to the recipient.
    """

    email: EmailStr
    context: dict = {}
    attachments: list[Attachment] = []


class EmailContent(BaseModel):
    from_: str
    recipients: list[Recipient]
    subject: str
    template: Union[str, Path]
    attachments: list[Attachment] = []

    @field_validator("recipients")
    @classmethod
    def validate_min_recipients(cls, recipients: list[Recipient]) -> list[Recipient]:
        if not recipients:
            raise ValueError("A minimum of one recipient is required")
        return recipients

    @field_validator("recipients")
    @classmethod
    def validate_max_recipient(cls, recipients: list[Recipient]) -> list[Recipient]:
        if len(recipients) > MAX_RECIPIENTS:
            raise ValueError(
                (
                    f"A maximum of {MAX_RECIPIENTS} recipients "
                    "can be sent an email in a batch"
                )
            )
        return recipients

    @field_validator("recipients")
    @classmethod
    def ensure_no_duplicate_recipient(
        cls, recipients: list[Recipient]
    ) -> list[Recipient]:
        email_to_recipients_mapping = {
            recipient.email: recipient for recipient in recipients
        }
        return list(email_to_recipients_mapping.values())

    @field_validator("template")
    @classmethod
    def validate_template(cls, template: Union[str, Path]) -> str:
        if isinstance(template, Path):
            try:
                with template.open() as file:
                    template = file.read()
            except FileNotFoundError:
                raise ValueError(f"File path {template} does not exist")
        return template


def add_attachments(email_message: MIMEMultipart, attachments: list[Attachment]):
    """Adds attachments to an email.

    Args:
        email_message: the email message which the attachments are added to.
        attachments: files to be added to the email message as attachments.
    """
    for attachment in attachments:
        filename = attachment.name
        if isinstance(attachment, Path):
            with attachment.open() as file_content:
                file_attachment = MIMEApplication(file_content.read())
        else:
            attachment.content.seek(0)
            file_attachment = MIMEApplication(attachment.content.read())
        file_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}",
        )
        email_message.attach(file_attachment)


def send_email(
    smtp_settings: SMTPSettings,
    email_content: EmailContent,
    attachments: Optional[list[Attachment]] = None,
):
    """
    Send HTML email with template rendering support.

    Args:
        smtp_settings: configurations for connecting with the SMTP email server
        email_content: context for composing the email
        attachments: file attachments if any
    """
    context = ssl.create_default_context()
    smtp_server = None
    if smtp_settings.SECURITY == "ssl":
        smtp_server = smtplib.SMTP_SSL(
            host=smtp_settings.host,
            port=smtp_settings.port,
            context=context,
        )
        smtp_server.login(user=smtp_settings.user, password=smtp_settings.password)
    elif smtp_settings.SECURITY == "tls":
        smtp_server = smtplib.SMTP(smtp_settings.host, smtp_settings.port)
        smtp_server.starttls(context=context)
        smtp_server.login(user=smtp_settings.user, password=smtp_settings.password)
    else:
        smtp_server = smtplib.SMTP(smtp_settings.host, smtp_settings.port)

    environment = jinja2.Environment()
    template_engine = environment.from_string(email_content.template)

    for recipient in email_content.recipients:
        message = MIMEMultipart()
        message["From"] = email_content.from_
        message["To"] = recipient.email
        message["Subject"] = environment.from_string(email_content.subject).render(
            recipient.context
        )
        message_body = template_engine.render(recipient.context)
        message.attach(MIMEText(message_body, "html"))

        if email_content.attachments:
            add_attachments(email_message=message, attachments=attachments)

        if recipient.attachments:
            add_attachments(email_message=message, attachments=attachments)

        smtp_server.sendmail(
            from_addr=email_content.from_,
            to_addrs=recipient.email,
            msg=message.as_string(),
        )
    smtp_server.quit()
