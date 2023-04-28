import json
from worker import send_email

def test_send_email(mocker):
    mocker.patch('sendgrid.SendGridAPIClient.send')

    email_data = {
        "email": "test@example.com",
        "subject": "Test Subject",
        "body": "Test Body"
    }

    send_email(email_data)

    sendgrid.SendGridAPIClient.send.assert_called_once()

    args, kwargs = sendgrid.SendGridAPIClient.send.call_args

    mail = kwargs["message"]
    assert mail.from_email.email == 'noreply@chatbot.com'
    assert mail.subject == email_data["subject"]
    assert mail.to_emails[0].email == email_data["email"]
    assert mail.html_content == email_data["body"]
