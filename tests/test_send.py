from juniorguru.send.__main__ import debug_message


def test_debug_message():
    message = dict(from_email=('From', 'sender@example.com'),
                   to_emails=[('To 1', 'to1@example.com'),
                              ('To 2', 'to2@example.com')],
                   bcc_emails=[('Bcc 1', 'bcc1@example.com'),
                               ('Bcc 2', 'bcc2@example.com')],
                   subject='Subject',
                   html_content='HTML <b>content</b>')
    message = debug_message(message)

    assert message == dict(from_email=('From', 'sender@example.com'),
                           to_emails=[('To 1', 'ahoj@junior.guru'),
                                       ('To 2', 'ahoj@junior.guru')],
                           bcc_emails=[],
                           subject='[DEBUG] Subject',
                           html_content='HTML <b>content</b>')
