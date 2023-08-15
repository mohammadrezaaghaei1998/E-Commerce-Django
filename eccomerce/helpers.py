# from django.core.mail import send_mail
# from django.conf import settings


# def send_forget_password_mail(email,token):
#     subject = 'Reset Password'
#     message = f'Hello,This message is from website supporter,For reset your password click on the link http://127.0.0.1:8000/reset_password/{token}/'
#     email_from = settings.EMAIL_HOST_USER
#     # email_from = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [email]
#     send_mail(subject,message,email_from,recipient_list)
#     return True