from django.core.mail import send_mail


def send_email_to_admin(subject,message,phone, sender_email):
    full_message = f'Phone: {phone}\n{message}'
    recipient_list = ['khantech0101@gmail.com']
    send_mail(subject, message=full_message,from_email=sender_email, recipient_list=recipient_list, fail_silently=False, auth_user=None, auth_password=None,
          connection=None, html_message=None)



