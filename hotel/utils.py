from django.core.mail import send_mail
from django.conf import settings
import random

def send_email(reciepent):
    subject = "OTP"
    message = "Your OTP is: "
    code = str(random.randint(1000, 9999))
    message+= code
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [reciepent]
    send_mail(subject, message, from_email, recipient_list)
    return code
