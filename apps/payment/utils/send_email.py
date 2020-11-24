import threading

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone

from apps.utils.config import MailSubject
from apps.utils.constants import ContractType


class EmailTemplate:
    
    def send_payment_email(self, instance, type_email):
        if type_email == 1:
            subject = MailSubject.warning_payment
            start = instance.start_date.strftime(settings.DATE_FORMATS[1])
            end = instance.end_date.strftime(settings.DATE_FORMATS[1])
        else:
            subject = MailSubject.payment
            start = timezone.now().date()
            end = start + relativedelta(days=7)
        
        context = {
            'username': instance.nguoi_gui.name,
            'so_tien': instance.so_tien,
            'han_thanh_toan': 'từ ngày {} đến ngày {}'.format(start, end),
            'ky_tt': instance.dot_thanh_toan,
            'title': 'Thanh toán tiền môi giới' if instance.hop_dong.type_contract == ContractType.HDMoiGioi.value else 'Thanh toán tiền thuê nhà'
        }
        html_message = loader.render_to_string(
            'payment_email.html', context
        )
        
        thread_sendmail = threading.Thread(
            target=self.send_mail_user,
            args=(instance.nguoi_gui.email, subject, html_message,),
            name='payment_email'
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
