from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class EmailService(object):

    def send_email(self, email, host, user_uuid):
        email_context = {
            'email': email,
            'domain': host,
            'uuid': user_uuid
        }
        subject = 'confirm via email'
        html_message = render_to_string('accounts/verify_email.html', email_context)
        message = strip_tags(html_message)
        recepient = email
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recepient], html_message=html_message,
                      fail_silently=False)
        except Exception as e:
            print(e)