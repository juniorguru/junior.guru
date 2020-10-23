from email.message import EmailMessage as BaseEmailMessage
from email.headerregistry import Address


class EmailMessage(BaseEmailMessage):
    def __repr__(self):
        from_repr = ', '.join([a.addr_spec for a in self['To'].addresses])
        bcc_repr = (
            f" ({', '.join([a.addr_spec for a in self['Bcc'].addresses])})"
            if self.get('Bcc')
            else ''
        )
        return f"<EmailMessage '{self['Subject']}' to {from_repr}{bcc_repr}>"


def create_message(from_email, to_emails, subject, html_content, bcc_emails=None):
    message = EmailMessage()
    message['From'] = Address(display_name=from_email[0], addr_spec=from_email[1])
    message['To'] = [Address(display_name=email[0], addr_spec=email[1])
                     for email in to_emails]
    if bcc_emails:
        message['Bcc'] = [Address(display_name=email[0], addr_spec=email[1])
                          for email in bcc_emails]
    message['Subject'] = subject
    message.add_header('Content-Type', 'text/html; charset="utf-8"')
    message.set_payload(html_content.encode('utf-8'))
    return message
