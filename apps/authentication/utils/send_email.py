import math
import random
import threading

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

from apps.authentication.models import UserAuth
from apps.utils.config import MailSubject, OTPString


class EmailTemplate:
    
    def generate_otp(self, user):
        digits = OTPString.otp_string
        otp_code = ""
        # length of password can be changed
        # by changing value in range
        for i in range(6):
            otp_code += digits[math.floor(random.random() * 10)]
        
        # save OTP code
        UserAuth.objects.create(
            user=user,
            auth_code=otp_code
        )
        
        return otp_code
    
    def get_context(self, user):
        context = dict()
        context['user_name'] = user.username
        context['code'] = self.generate_otp(user)
        return context
    
    def send_activation_email(self, user):
        context = self.get_context(user)
        html_message = loader.render_to_string(
            'activation_email.html', context
        )
        thread_sendmail = threading.Thread(
            target=self.send_mail_user,
            args=(user.email, MailSubject.activation, html_message,),
            name='send_activation_email'
        )
        thread_sendmail.start()
    
    @staticmethod
    def send_mail_user(user_mail, subject, html_template):
        send_mail(
            subject,
            '',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_mail],
            html_message=html_template,
            fail_silently=True
        )
