import re
import datetime
from users.error_handler.views import Error_Handler
from users.response_handler.views import ResponseWrapper
from rest_framework import status
from localflavor.us.us_states import STATE_CHOICES

ssn_re = re.compile(r"^(?P<area>\d{3})[-\ ]?(?P<group>\d{2})[-\ ]?(?P<serial>\d{4})$")
phone_digits_re = re.compile(r'^(?:\+?1-?)?\(?(\d{3})\)?[-\.]?(\d{3})[-\.]?(\d{4})$')

class MobileValidate:
    __mobile = None

    def __init__(self, data):
        self.__mobile = data

    def mobile_provide_validate(self):
        if self.__mobile == None or self.__mobile == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="Mobile Number")
            return data_response
        else:
            return True

    def mobile_format(self):
        match = re.match(phone_digits_re, self.__mobile)
        if not match:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="Mobile_Format", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response
        else:
            return True


    def mobile_validate(self):
        mobile_empty = self.mobile_provide_validate()
        if mobile_empty != True:
            return mobile_empty
        mobile_string = self.mobile_format()
        if mobile_string != True:
            return mobile_string
        return True


class TermsConditionsValidate:
    __tnc =None


    def __init__(self, data):
        self.__tnc = data

    def tnc_provide_validate(self):
        if self.__tnc == None or self.__tnc == "":
            error_handler = Error_Handler()

            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="TermsCondition")
            return data_response
        else:
            return True
    def tnc_value_validate(self):
        if self.__tnc is False:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="ValueError", response={}, code=status.HTTP_200_OK)
            return data_response
        else:
            return True


    def termsconditions_validate(self):
        termsconditions_empty = self.tnc_provide_validate()
        if termsconditions_empty != True:
            return termsconditions_empty
        termsconditions_value = self.tnc_value_validate()
        if termsconditions_value != True:
            return termsconditions_value
        return True


class AddressValidate:
    __address = None

    def __init__(self, data):
        self.__address = data

    def address_provide_validate(self):
        if self.__address == None or self.__address == "":
            error_handler = Error_Handler()

            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="Address")
            return data_response
        else:
            return True

    def address_validate(self):
        address_empty = self.address_provide_validate()
        if address_empty != True:
            return address_empty
        return True


class BirthDateValidation:
    __dob = None

    def __init__(self, data):
        self.__dob = data

    def date_provide_validate(self):
        if self.__dob == None or self.__dob == "":
            error_handler = Error_Handler()

            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="date_of_birth")
            return data_response
        else:
            return True

    def birthdate_validate(self):
        birthdate_empty = self.date_provide_validate()
        if birthdate_empty != True:
            return birthdate_empty
        return True


class EmailValidate:
    __email = None

    def __init__(self, data):
        self.__email = data

    def email_provide_validate(self):
        if self.__email == None or self.__email == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="Email Id")
            return data_response
        else:
            return True

    def email_id_validate(self):
        if '@' in self.__email:
            return True
        else:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_valid", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="Email Id")
            return data_response

    def email_validate(self):

        email_empty = self.email_provide_validate()
        if email_empty != True:
            return email_empty

        email_id = self.email_id_validate()
        if email_id != True:
            return email_id

        return True


class OTPValidate():
    __otp = None

    def __init__(self, data):
        self.__otp = data

    def otp_provide_validate(self):
        if self.__otp == None or self.__otp == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="OTP")
            return data_response
        else:
            return True

    def otp_len_validate(self):
        if len(self.__otp) != 4:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="otp_digit", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response
        else:
            return True

    def otp_numeric_validate(self):
        if not self.__otp.isnumeric():
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_digit", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value='One Time Password (OTP)')
            return data_response
        else:
            return True

    def otp_validate(self):
        otp_empty = self.otp_provide_validate()
        if otp_empty != True:
            return otp_empty

        otp_len = self.otp_len_validate()
        if otp_len != True:
            return otp_len

        otp_numeric = self.otp_numeric_validate()
        if otp_numeric != True:
            return otp_numeric

        return True


class PasswordValidate:
    __password = None

    def __init__(self, data):
        self.__password = data

    def password_provide_validate(self):
        if self.__password == None or self.__password == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="Password")
            return data_response
        else:
            return True

    def password_len_validate(self):
        if len(self.__password) < 8:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="password_min", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response
        else:
            return True

    def password_validate(self):
        password_empty = self.password_provide_validate()
        if password_empty != True:
            return password_empty

        password_len = self.password_len_validate()
        if password_len != True:
            return password_len

        return True


class NameValidate:
    __name = None

    def __init__(self, data):
        self.__name = data

    def name_provide_validate(self):
        if self.__name == None or self.__name == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="Name")
            return data_response
        else:
            return True

    def name_len_validate(self):
        if len(self.__name) <= 2:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="NameMinChar", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response
        else:
            return True

    def name_validate(self):
        name_empty = self.name_provide_validate()
        if name_empty != True:
            return name_empty

        name_len = self.name_len_validate()
        if name_len != True:
            return name_len

        return True


class SSNValidate:
    __ssn = None

    def __init__(self, data):
        self.__ssn = data

    def ssn_provide_validate(self):
        if self.__ssn is None:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="social_security_num")
            return data_response
        else:
            return True

    def ssn_len_validate(self):
        if len(self.__ssn) != 11:
            error_handler = Error_Handler()
            data_response = error_handler.response(key='SSN_MinChar', response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response
        else:
            return True

    def ssn_format_validate(self):
        match = re.match(ssn_re, self.__ssn)
        if not match:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="SSN_Format", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response
        area, group, serial = match.groupdict()['area'], match.groupdict()['group'], match.groupdict()['serial']

        # First pass: no blocks of all zeroes.
        if area == '000' or group == '00' or serial == '0000':
            error_handler = Error_Handler()
            data_response = error_handler.response(key="block_zeros", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response

        # Second pass: promotional and otherwise permanently invalid numbers.
        if (area == '666' or
                area.startswith('9') or
                self.__ssn == '078-05-1120' or
                self.__ssn == '219-09-9999'):
            error_handler = Error_Handler()
            data_response = error_handler.response(key="invalid_credential", response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response

        return True

    def ssn_validate(self):
        ssn_empty = self.ssn_provide_validate()
        if ssn_empty != True:
            return ssn_empty
        ssn_len = self.ssn_len_validate()
        if ssn_len != True:
            return ssn_len
        ssn_numeric = self.ssn_format_validate()
        if ssn_numeric != True:
            return ssn_numeric
        return True


class ZipCodeValidate:
    __zipcode = None

    def __init__(self, data):
        self.__zipcode = data

    def zipcode_provide_validate(self):

        if self.__zipcode == None or self.__zipcode == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="social_security_number")
            return data_response
        else:
            return True

    def zipcode_len_validate(self):
        if len(self.__zipcode) != 5:
            error_handler = Error_Handler()
            data_response = error_handler.response(key='ZipCodeMinChar', response={}, code=status.HTTP_400_BAD_REQUEST)
            return data_response
        else:
            return True

    def zipcode_numeric_validate(self):
        if not self.__zipcode.isnumeric():
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_digit", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value='ZipCode Number')
            return data_response
        else:
            return True

    def zipcode_validate(self):
        zip_empty = self.zipcode_provide_validate()
        if zip_empty != True:
            return zip_empty
        zip_len = self.zipcode_len_validate()
        if zip_len != True:
            return zip_len
        zip_numeric = self.zipcode_numeric_validate()
        if zip_numeric != True:
            return zip_numeric
        return True

class StateValidate:
    __state = None

    def __init__(self, data):
        self.__state = data

    def state_provide_validate(self):

        if self.__state == None or self.__state == "":
            error_handler = Error_Handler()
            data_response = error_handler.response(key="generic_provide", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="State")
            return data_response
        else:
            return True

    def state_choice_validate(self):

        valid_choices = []
        for e in STATE_CHOICES:
            valid_choices.append(e[0])
        if self.__state not in valid_choices:
            error_handler = Error_Handler()
            data_response = error_handler.response(key="Choice_Error", response={}, code=status.HTTP_400_BAD_REQUEST,
                                                   value="State")
            return data_response
        else:
            return True

    def state_validate(self):
        state_empty = self.state_provide_validate()
        if state_empty != True:
            return state_empty
        state_choices = self.state_choice_validate()
        if state_choices != True:
            return state_choices
        return True

class EmailTokenValidate():
    __token = None

    def __init__(self, data):
        self.__token = data

    def token_provide_validate(self):
        if self.__token == None:
            # key = "ProvideOTP"
            # errorObj = Error_Handler(key)
            # data_error = errorObj.error_handle()
            # responseObj = ResponseWrapper()
            # data_response = responseObj.response(False, {}, data_error)
            # return data_response
            responseObj = ResponseWrapper()
            data = responseObj.response(False, {}, "Provide token number.")
            return data
        else:
            return True

    def token_validate(self):
        token_empty = self.token_provide_validate()
        if token_empty != True:
            return token_empty

        return True
