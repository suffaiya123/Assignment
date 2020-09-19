import datetime
from users.validation import (MobileValidate,
                              EmailValidate,
                              OTPValidate,
                              PasswordValidate,
                              EmailTokenValidate,
                              SSNValidate,
                              ZipCodeValidate,
                              NameValidate,
                              StateValidate,
                              TermsConditionsValidate,
                              AddressValidate,
                              BirthDateValidation)
import datetime
import math, random
from django.utils.timezone import now
from .models import Users, ResetPassword, Token, TempUser
from Paymenypayfort.settings import URL
from rest_framework import status
from users.data import set_password, check_password
from users.error_handler.views import Error_Handler
from users.response_handler.views import ResponseWrapper
from users.verification import OTPSMSVerification, EmailVerification
import binascii
import os


class SignUp:
    __data = None

    def __init__(self, data):
        self.__data = data

    def signup(self):
        name = self.__data.get("full_name", None)
        mobile = self.__data.get("phone_number", None)
        email = self.__data.get("email", None)
        password = self.__data.get("password", None)
        ssn = self.__data.get('ssn', None)
        zipcode = self.__data.get('zipcode', None)
        state = self.__data.get('state', None)
        date_of_birth = self.__data.get('date_of_birth', None)
        profile_image = self.__data.get('profile_image')
        termsconditions = self.__data.get('termsconditions', None)
        address = self.__data.get('address', None)

        name_validateObj = NameValidate(name)
        name_validate = name_validateObj.name_validate()
        if name_validate != True:
            return name_validate

        mobile_validateObj = MobileValidate(mobile)
        mobile_validate = mobile_validateObj.mobile_validate()
        if mobile_validate != True:
            return mobile_validate

        email_validateObj = EmailValidate(email)
        email_validate = email_validateObj.email_validate()
        if email_validate != True:
            return email_validate

        password_validateObj = PasswordValidate(password)
        password_validate = password_validateObj.password_validate()
        if password_validate != True:
            return password_validate

        ssn_validateObj = SSNValidate(ssn)
        ssn_validate = ssn_validateObj.ssn_validate()
        if ssn_validate != True:
            return ssn_validate

        birthdatevalidateObj = BirthDateValidation(date_of_birth)
        birthdate_validate =birthdatevalidateObj.birthdate_validate()
        if birthdate_validate != True:
            return birthdate_validate

        zipcode_validateObj = ZipCodeValidate(zipcode)
        zipcode_validate = zipcode_validateObj.zipcode_validate()
        if zipcode_validate != True:
            return zipcode_validate

        state_validateObj = StateValidate(state)
        state_validate = state_validateObj.state_validate()
        if state_validate != True:
            return state_validate

        termsandconditionsObj = TermsConditionsValidate(termsconditions)
        termsconditions_validate = termsandconditionsObj.termsconditions_validate()
        if termsconditions_validate != True:
            return termsconditions_validate

        addressObj = AddressValidate(address)
        address_validate = addressObj.address_validate()
        if address_validate != True:
            return address_validate


        user = Users.objects.filter(phone_number=mobile,email=email)
        if user.exists():
            error_handler = Error_Handler()
            data_response = error_handler.response(key="user_exist", response={}, code=status.HTTP_200_OK)
            return data_response

        user = Users.objects.filter(phone_number=mobile)
        if user.exists():
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_email_mobile", response={}, code=status.HTTP_200_OK,
                                                   value="Mobile Number")
            return data_response

        user = Users.objects.filter(email=email)
        if user.exists():
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_email_mobile", response={}, code=status.HTTP_200_OK,
                                                   value="Email Id")
            return data_response

        if profile_image == "null":
            profile_image = ""

        elif "/temp_profile_images" in profile_image:
            image = profile_image
            img_path = "temp_profile_images"
            image_path = image.split(img_path)
            profile_image = img_path + image_path[-1]
        else:
            profile_image=""

        try:
            dob = datetime.datetime.strptime(date_of_birth,'%b/%d/%y')
        except:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="ValueError", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response

        tokenObj = OTP()
        token_mobile = tokenObj.token_generate()
        token_email = tokenObj.token_generate_email()


        try:
            temp_user = TempUser.objects.get(phone_number=mobile)
            temp_user.full_name = name
            temp_user.password = set_password(password)
            temp_user.phone_number = mobile
            temp_user.email = email
            temp_user.ssn = ssn
            temp_user.state = state
            temp_user.date_of_birth = dob
            temp_user.profile_image = profile_image
            temp_user.zipcode = zipcode
            temp_user.mobile_token = token_mobile
            temp_user.email_token = token_email
            temp_user.created_on_mobile = now()
            temp_user.created_on_email = now()
            temp_user.email_verification_status = False
            temp_user.mobile_verification_status = False
            temp_user.termsconditions = termsconditions
            temp_user.address = address
            temp_user.save()
        except:
            temp_user = TempUser.objects.create(full_name=name, password=set_password(password), phone_number=mobile,
                                                email=email, zipcode=zipcode, mobile_token=token_mobile, state=state,
                                                email_token=token_email, ssn=ssn, profile_image=profile_image,
                                                date_of_birth=dob,
                                                created_on_mobile=now(), created_on_email=now(),
                                                termsconditions=termsconditions, address=address)

        # otp send to user mobile  number
        OTPObj = OTPSMSVerification()
        minute = tokenObj.minute_validity()
        data_response = OTPObj.send_otp(mobile, token_mobile, minute)
        # otp send to user mobile  number

        # # # link send to user email id
        # link = "%s/api/v1/signup/link_verify/?email=%s&email_token=%s" % (URL, email, str(token_email))
        # valid_minute = tokenObj.minute_validity()
        # emailObj = EmailVerification()
        # email_data = emailObj.new_user_link_verification_mail(link, email, valid_minute)        # link send to mail
        # # # link send to user email id

        response = ResponseWrapper()
        message = "A text with a One Time Password (OTP) has been sent to your mobile number."
        data = response.response({"data": data_response}, message,
                                 status.HTTP_201_CREATED)
        return data


class OTP:
    __data = None
    __otp_minute = 20

    def __init__(self, data=None):
        self.__data = data

    def minute_validity(self):
        token_minute = self.__otp_minute
        return token_minute

    def token_generate(self):
        token_random = random.randint(1000, 9999)
        token = str(token_random)
        token = "1234"
        return token

    def token_generate_email(self):
        token_random = binascii.hexlify(os.urandom(10)).decode()
        return token_random


    def new_user_otp_verify(self):
        mobile = self.__data.get("phone_number", None)
        token = self.__data.get("token", None)

        mobile_validateObj = MobileValidate(mobile)
        mobile_validate = mobile_validateObj.mobile_validate()
        if mobile_validate != True:
            return mobile_validate

        otp_validateObj = OTPValidate(token)
        otp_validate = otp_validateObj.otp_validate()
        if otp_validate != True:
            return otp_validate

        user = Users.objects.filter(phone_number=mobile)
        if user.exists():
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_email_mobile", response={}, code=status.HTTP_200_OK,
                                                   value="Mobile Number")
            return data_response

        try:
            temp_user = TempUser.objects.get(phone_number=mobile)
        except:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="signup", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response

        if (temp_user.created_on_mobile + datetime.timedelta(minutes=self.__otp_minute)) < now():
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_expired", response={}, code=status.HTTP_200_OK,
                                                   value="One Time Password (OTP)")
            return data_response

        if not temp_user.email_verification_status:
            temp_user.email_verification_status = True

        if temp_user.mobile_token == token:
            temp_user.mobile_verification_status = True
            temp_user.save()
            created_user = Users.objects.create(full_name=temp_user.full_name, email=temp_user.email,
                                                phone_number=temp_user.phone_number,
                                                password=temp_user.password, zipcode=temp_user.zipcode,
                                                ssn=temp_user.ssn, state=temp_user.state,
                                                date_of_birth=temp_user.date_of_birth,
                                                profile_image=temp_user.profile_image,
                                                email_verification_status=temp_user.email_verification_status,
                                                mobile_verification_status=temp_user.mobile_verification_status,
                                                termsconditions=temp_user.termsconditions,
                                                address=temp_user.address,
                                                remember_me=temp_user.remember_me,
                                                created_on=now(), is_active=True, last_accessed_on=now())
            ResetPassword.objects.create(user=created_user)

            token, created = Token.objects.get_or_create(user=created_user)
            response = ResponseWrapper()
            message = "Mobile number is verified."
            data = response.response({"token": token.key}, message, status.HTTP_200_OK)
            return data

        elif temp_user.mobile_token != token:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="otp_wrong", response={}, code=status.HTTP_200_OK)
            return data_response
    #
    # def new_user_resend_link(self):
    #     email = self.__data.get("email", None)
    #     email_validateObj = EmailValidate(email)
    #     email_validate = email_validateObj.email_validate()
    #     if email_validate != True:
    #         return email_validate
    #     user = Users.objects.filter(email=email)
    #     if user.exists():
    #         error_handler = Error_Handler()
    #         data_response = error_handler.response(key="generic_email_mobile", response={}, code=status.HTTP_200_OK,
    #                                                value="Email")
    #         return data_response
    #
    #     temp_user = TempUser.objects.get(email=email)
    #     tokenObj = OTP()
    #     token_email = tokenObj.token_generate_email()
    #
    #     temp_user.email_token = token_email
    #     temp_user.created_on_email = now()
    #     temp_user.save()
    #
    #     # # link send to user email id
    #     link = "%s/api/v1/signup/link_verify/?email=%s&email_token=%s" % (URL, email, str(token_email))
    #     valid_minute = tokenObj.minute_validity()
    #     emailObj = EmailVerification()
    #     email_data = emailObj.new_user_link_verification_mail(link, email, valid_minute)  # link send to mail
    #     # # link send to user email id
    #     response = ResponseWrapper()
    #     message = "Verification Link is send to your Email."
    #     data = response.response({"data": {}}, message, status.HTTP_201_CREATED)
    #     return data

    def new_user_resend_otp(self):
        mobile = self.__data.get("phone_number", None)
        mobile_validateObj = MobileValidate(mobile)
        mobile_validate = mobile_validateObj.mobile_validate()
        if mobile_validate != True:
            return mobile_validate

        user = Users.objects.filter(phone_number=mobile)
        if user.exists():
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_email_mobile", response={}, code=status.HTTP_200_OK,
                                                   value="Mobile Number")
            return data_response

        temp_user = TempUser.objects.get(phone_number=mobile)

        tokenObj = OTP()
        token_mobile = tokenObj.token_generate()

        temp_user.mobile_token = token_mobile
        temp_user.created_on_mobile = now()
        temp_user.save()

        # otp send to user mobile  number
        OTPObj = OTPSMSVerification()
        minute = tokenObj.minute_validity()
        data_response = OTPObj.send_otp(mobile, token_mobile, minute)
        # otp send to user mobile  number

        response = ResponseWrapper()
        message = "A text with a One Time Password (OTP) has been sent to your mobile number."
        data = response.response({"data": data_response}, message, status.HTTP_201_CREATED)
        return data

    def reset_password_token_verify(self):
        user = self.__data.get("user", None)
        token = self.__data.get("token", None)
        if user is None or user == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="Mobile Number/Email Id.")
            return data_response
        mobile = None
        email = None
        if '@' in user:
            email = user
        else:
            mobile = user

        if mobile != None:
            mobile_validateObj = MobileValidate(mobile)
            mobile_validate = mobile_validateObj.mobile_validate()
            if mobile_validate != True:
                return mobile_validate

            token_validateObj = OTPValidate(token)
            token_validate = token_validateObj.otp_validate()
            if token_validate != True:
                return token_validate

            try:
                user = Users.objects.get(phone_number=mobile)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="not_find_generic", response={},
                                                       code=status.HTTP_404_NOT_FOUND, value="mobile number")
                return data_response

            if user.mobile_verification_status != True:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="mob_not_verified", response={}, code=status.HTTP_200_OK)
                return data_response

            try:
                user_reset = ResetPassword.objects.get(user=user)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="something_wrong", response={}, code=status.HTTP_200_OK)
                return data_response

            if (user_reset.created_on_mobile + datetime.timedelta(minutes=self.__otp_minute)) < now():
                error_handler = Error_Handler()
                data_response = error_handler.response(key="generic_expired", response={}, code=status.HTTP_200_OK,
                                                       value="One Time Password (OTP)")
                return data_response

            elif user_reset.mobile_token == token:
                user_reset.mobile_verification_status = True
                user_reset.save()

                response = ResponseWrapper()
                message = "Verified."
                data = response.response({}, message, status.HTTP_200_OK)
                return data

            elif user_reset.mobile_token != token:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="otp_wrong", response={}, code=status.HTTP_200_OK)
                return data_response

        elif email != None:
            email_validateObj = EmailValidate(email)
            email_validate = email_validateObj.email_validate()
            if email_validate != True:
                return email_validate

            token_validateObj = EmailTokenValidate(token)
            token_validate = token_validateObj.token_validate()
            if token_validate != True:
                return token_validate

            try:
                user = Users.objects.get(email=email)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="not_find_generic", response={},
                                                       code=status.HTTP_404_NOT_FOUND, value="Email Id")
                return data_response

            if user.email_verification_status != True:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="email_not_verified", response={}, code=status.HTTP_200_OK,
                                                       value="Email Id")
                return data_response

            try:
                user_reset = ResetPassword.objects.get(user=user)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="something_wrong", response={},
                                                       code=status.HTTP_400_BAD_REQUEST)
                return data_response

            if (user_reset.created_on_email + datetime.timedelta(minutes=self.__otp_minute)) < now():
                error_handler = Error_Handler()
                data_response = error_handler.response(key="generic_expired", response={}, code=status.HTTP_200_OK,
                                                       value='Verification link')
                return data_response

            elif user_reset.email_token == token:
                user_reset.email_verification_status = True
                user_reset.save()

                response = ResponseWrapper()
                message = "Verified."
                data = response.response({}, message, status.HTTP_200_OK)
                return data

            elif user_reset.email_token != token:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="link_broken", response={}, code=status.HTTP_200_OK)
                return data_response

        else:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value='Mobile Number/Email')
            return data_response


class Password():
    __data = None

    def __init__(self, data):
        self.__data = data

    def reset_password_token_generate(self):
        # mobile = self.__data.get("mobile", None)
        # email = self.__data.get("email", None)
        user = self.__data.get("user", None)

        if user == None:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value='Mobile Number/Email')
            return data_response
        mobile = None
        email = None
        if '@' in user:
            email = user
        else:
            mobile = user

        if mobile != None:
            mobile_validateObj = MobileValidate(mobile)
            mobile_validate = mobile_validateObj.mobile_validate()
            if mobile_validate != True:
                return mobile_validate

            try:
                user = Users.objects.get(phone_number=mobile)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="not_find_generic", response={},
                                                       code=status.HTTP_404_NOT_FOUND, value="mobile number")
                return data_response

            if user.mobile_verification_status != True:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="mob_not_verified", response={}, code=status.HTTP_200_OK)
                return data_response

            try:
                user_reset = ResetPassword.objects.get(user=user)
                tokenObj = OTP()
                token_mobile = tokenObj.token_generate()
                user_reset.mobile_token = token_mobile
                user_reset.mobile_verification_status = False
                user_reset.created_on_mobile = now()
                user_reset.save()

                # otp send to user mobile  number
                OTPObj = OTPSMSVerification()
                minute = tokenObj.minute_validity()
                data_response = OTPObj.send_otp(mobile, token_mobile, minute)
                # otp send to user mobile  number

                response = ResponseWrapper()
                message = "A text with a One Time Password (OTP) has been sent to your mobile number."
                data = response.response({}, message, status.HTTP_201_CREATED)
                return data

            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="something_wrong", response={},
                                                       code=status.HTTP_400_BAD_REQUEST)
                return data_response

        elif email != None:
            email_validateObj = EmailValidate(email)
            email_validate = email_validateObj.email_validate()
            if email_validate != True:
                return email_validate

            try:
                user = Users.objects.get(email=email)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="not_find_generic", response={},
                                                       code=status.HTTP_404_NOT_FOUND, value="Email Id")
                return data_response

            if user.email_verification_status != True:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="email_not_verified", response={}, code=status.HTTP_200_OK,
                                                       value="Email Id")
                return data_response

            try:
                user_reset = ResetPassword.objects.get(user=user)
                tokenObj = OTP()
                token_email = tokenObj.token_generate_email()

                user_reset.email_token = token_email
                user_reset.email_verification_status = False
                user_reset.created_on_email = now()
                user_reset.save()

                # link send to user email number
                link = "%s/passwordresetemail?email=%s&token=%s" % (URL, email, str(token_email))
                valid_minute = tokenObj.minute_validity()
                emailObj = EmailVerification()
                email_data = emailObj.new_user_link_verification_mail(link, email, valid_minute)  # link send to mail
                # link send to user email number

                response = ResponseWrapper()
                message = "Verification link has been sent to your Email Id."
                data = response.response({}, message, status.HTTP_200_OK)
                return data

            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="something_wrong", response={},
                                                       code=status.HTTP_400_BAD_REQUEST)
                return data_response

    def reset_password_changed(self):
        user = self.__data.get("user", None)
        token = self.__data.get("token", None)
        if user == None:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value='Mobile Number/Email')
            return data_response
        mobile = None
        email = None
        if '@' in user:
            email = user
        else:
            mobile = user

        password = self.__data.get("password", None)
        # password = password.strip()
        # mobile= mobile.strip()

        if mobile != None:
            mobile_validateObj = MobileValidate(mobile)
            mobile_validate = mobile_validateObj.mobile_validate()
            if mobile_validate != True:
                return mobile_validate

            password_validateObj = PasswordValidate(password)
            password_validate = password_validateObj.password_validate()
            if password_validate != True:
                return password_validate

            try:
                user = Users.objects.get(phone_number=mobile)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="not_find_generic", response={},
                                                       code=status.HTTP_404_NOT_FOUND, value="mobile number")
                return data_response

            if user.mobile_verification_status != True:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="mob_not_verified", response={}, code=status.HTTP_200_OK)
                return data_response

            try:
                user_reset = ResetPassword.objects.get(user=user)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="something_wrong", response={},
                                                       code=status.HTTP_400_BAD_REQUEST)
                return data_response

            if user_reset.mobile_verification_status == True:
                user_reset.mobile_verification_status = False
                user_reset.save()
                user.password = set_password(password)
                user.save()

                response = ResponseWrapper()
                message = "Your Password has been changed."
                data = response.response({}, message, status.HTTP_200_OK)
                return data

            elif user_reset.mobile_verification_status == False:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="skip_forgot", response={}, code=status.HTTP_400_BAD_REQUEST)
                return data_response


        elif email != None:
            email_validateObj = EmailValidate(email)
            email_validate = email_validateObj.email_validate()
            if email_validate != True:
                return email_validate

            password_validateObj = PasswordValidate(password)
            password_validate = password_validateObj.password_validate()
            if password_validate != True:
                return password_validate

            try:
                user = Users.objects.get(email=email)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="not_find_generic", response={},
                                                       code=status.HTTP_404_NOT_FOUND, value="Email Id")
                return data_response

            if user.email_verification_status != True:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="email_not_verified", response={}, code=status.HTTP_200_OK,
                                                       value="Email Id")
                return data_response

            try:
                user_reset = ResetPassword.objects.get(user=user)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="something_wrong", response={},
                                                       code=status.HTTP_400_BAD_REQUEST)
                return data_response

            if user_reset.email_verification_status == True:
                user_reset.email_verification_status = False
                user_reset.save()
                user.password = set_password(password)
                user.save()

                response = ResponseWrapper()
                message = "Your Password has been changed."
                data = response.response({}, message, status.HTTP_200_OK)
                return data

            elif user_reset.email_verification_status == False:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="skip_forgot", response={}, code=status.HTTP_400_BAD_REQUEST)
                return data_response

        else:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value='Mobile Number/Email')
            return data_response


class SignIn():
    __data = None

    def __init__(self, data):
        self.__data = data

    def signin(self):
        user = self.__data.get("user", "")
        password = self.__data.get("password", None)
        remember_me = self.__data.get("remember_me")
        # password = password.strip()
        if remember_me == False:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="ValueError", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response
        user = user.strip()
        if user == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value='Mobile Number/Email')
            return data_response

        mobile = None
        email = None

        if '@' in user:
            email = user
        else:
            mobile = user

        if mobile != None:
            mobile_validateObj = MobileValidate(mobile)
            mobile_validate = mobile_validateObj.mobile_validate()
            if mobile_validate != True:
                return mobile_validate

            password_validateObj = PasswordValidate(password)
            password_validate = password_validateObj.password_validate()
            if password_validate != True:
                return password_validate
            try:
                user_data = Users.objects.get(phone_number=mobile)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="not_find_generic", response={},
                                                       code=status.HTTP_404_NOT_FOUND, value="mobile number")
                return data_response

            if user_data.mobile_verification_status == False:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="mob_not_verified", response={}, code=status.HTTP_200_OK)
                return data_response
            user_data.remember_me = remember_me

            password_enc = check_password(user_data.password, password)

            if user_data.password != password_enc:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="invalid_credential", response={}, code=status.HTTP_401_UNAUTHORIZED)
                return data_response

            user_data.last_login = now()
            user_data.save()
            token, created = Token.objects.get_or_create(user=user_data)

            response = ResponseWrapper()
            message = "Login Successfully."

            data = response.response({"token": token.key}, message, status.HTTP_200_OK)
            return data

        elif email != None:
            email_validateObj = EmailValidate(email)
            email_validate = email_validateObj.email_validate()
            if email_validate != True:
                return email_validate

            password_validateObj = PasswordValidate(password)
            password_validate = password_validateObj.password_validate()
            if password_validate != True:
                return password_validate

            try:
                user_data = Users.objects.get(email=email)
            except:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="not_find_generic", response={},
                                                       code=status.HTTP_404_NOT_FOUND, value="Email Id")
                return data_response

            if user_data.email_verification_status == False:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="email_not_verified", response={}, code=status.HTTP_200_OK,
                                                       value="Email Id")
                return data_response
            user_data.remember_me = remember_me
            password_enc = check_password(user_data.password, password)

            if user_data.password != password_enc:
                error_handler = Error_Handler()
                data_response = error_handler.response(key="invalid_credential", response={},
                                                       code=status.HTTP_401_UNAUTHORIZED)
                return data_response

            user_data.last_login = now()
            user_data.save()
            token, created = Token.objects.get_or_create(user=user_data)

            response = ResponseWrapper()
            message = "Login Successfully."

            data = response.response({"token": token.key}, message, status.HTTP_200_OK)
            return data



        else:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value='Mobile Number/Email')
            return data_response

