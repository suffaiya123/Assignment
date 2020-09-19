import http.client
import requests
from Paymenypayfort.settings import EMAIL_HOST_USER
from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives

class OTPSMSVerification():
    def new_user_send_otp_msg(self, mobile, token, minute, resend):
        # if resend:
        #     message = '{0} is your RideBag OTP. It is valid for {1} minutes. Do not share it with anyone' .format(token, minute)
        # else:
        #     message = '{0} is your RideBag OTP. It is valid for {1} minutes. Do not share it with anyone' .format(token, minute)
        # url = "https://sms.prowtext.com/sendsms/apikey.php?apikey=snarTomeDdadc137a4009090aaa&type=TEXT&sender=PROWTX&&message={1}&mobile={0}" .format(mobile, message)
        # data = requests.get(url)
        data = '1234'
        return data

    def send_otp(self, mobile, token, minute):
        data = self.new_user_send_otp_msg(mobile,token, minute, resend=False)
        return data


class EmailVerification():
    def new_user_verification_mail(self, token, recipient, valid_minute, fail_silently=False, auth_user=None,
                                   auth_password=None, connection=None, htmlmessage=None):
        recipient = [recipient]
        subject = 'RideBag Token Email Verification'
        message = '<div>' \
                  '<center><h3>Hello there</h3><center>' \
                  '<p>Welcome to Ride Bag' \
                  '.<br> Your One Time Password has been generated and the same is {0}.' \
                  ' One time Password is valid for {1} minutes. ' \
                  '<br>Please use this One Time Password to complete the Signup Process.</p>' \
                  '</div>'.format(token, valid_minute)
        email_from = EMAIL_HOST_USER
        settings.EMAIL_USE_TLS = True
        connection = connection or get_connection(username=auth_user, password=auth_password, host='smtp.gmail.com', port=587, fail_silently=fail_silently)
        mail = EmailMultiAlternatives(subject, message, email_from, recipient, connection=connection,)
        if htmlmessage:
            mail.attach_alternative(htmlmessage, 'text/html')
        mail.content_subtype = "html"
        return mail.send()

    def new_user_link_verification_mail(self, link, recipient, valid_minute, fail_silently=False, auth_user=None, auth_password=None, connection=None, htmlmessage=None):
        recipient = [recipient]
        subject = 'RideBag Email Verification'
        message = '<div align="center" style="width: 50%;"><div style="background-color: blue; ' \
                'alignment: center;">' \
                '<p align="center" style="font-size: x-large; color: white; ">RideBag Email Verification</p></div>' \
                '<p>Welcome to RideBag.<br/>Click ' \
                'on the button bellow to verify your ' \
                'email or copy the link and open in your browser.<br/>Verification link is valid for next {1} minutes.</p><p align="center"><a href="{0}" ' \
                'type="button" style="alignment: center; size: 100px;background-color: ' \
                'blue; color: white">Verify Email</a>' \
                '</p><p>Email Verification Link : {0}</p></div>'.format(link, valid_minute)
        email_from = EMAIL_HOST_USER
        settings.EMAIL_USE_TLS = True
        connection = connection or get_connection(username=auth_user, password=auth_password, host='smtp.gmail.com', port=587, fail_silently=fail_silently)
        mail = EmailMultiAlternatives(subject, message, email_from, recipient, connection=connection,)
        if htmlmessage:
            mail.attach_alternative(htmlmessage, 'text/html')
        mail.content_subtype = "html"
        return mail.send()