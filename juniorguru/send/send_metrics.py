import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail, To


SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


def main():
    message = Mail(from_email=From('metrics@junior.guru', 'junior.guru'),
                   to_emails=To('mail@honzajavorek.cz', 'Honza Javorek'),
                   subject='Sending with Twilio SendGrid is Fun',
                   plain_text_content='and easy to do anywhere, even with Python',
                   html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        from pprint import pprint; pprint(message.get())
        # client = SendGridAPIClient(SENDGRID_API_KEY)
        # response = client.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
