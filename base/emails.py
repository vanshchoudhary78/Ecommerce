
from django.conf import settings
from django.core.mail import send_mail




# def send_account_activation_email(email , email_token):
#     return
#     subject = 'Your account needs to be verified'
#     email_from = settings.EMAIL_HOST_USER
#     message = f'Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
#     send_mail(subject , message , email_from , [email])
def send_account_activation_email(email, email_token):
    subject = 'Activate your account'
    activation_link = f"http://127.0.0.1:8000/accounts/activate/{email_token}/"
    message = f'Click the link to activate your account: {activation_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)