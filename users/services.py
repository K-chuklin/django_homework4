from django.core.mail import send_mail

def send_new_password(email, new_password)
    send_mail(
            subject="Новый пароль от платформы МойМагазин!",
            message=f"Выш новый пароль {new_password}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email]
        )