from django.core.mail import send_mail
from django.conf import settings

def send_forget_password_mail(email, token):
    subject = 'Token untuk mengatur ulang password anda  '
    message = f'Halo, kamu bisa klik link ini untuk mengatur ulang password anda \n https://hawariyyun.pythonanywhere.com/accounts/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
