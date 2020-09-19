class Error_Handler:
    __message = "Unexpected Error Occurred"

    def response(self, key, response, code, value=None, message=None):
        if key == "MobileNotValid":
            self.__message = "Mobile number must be 10 digit long."
        elif key == "NameMinChar":
            self.__message = "Name must be 3 character long."
        elif key == "MobileString":
            self.__message = "Mobile number must be digit."
        elif key == "otp_digit":
            self.__message = "One Time Password (OTP) must be 4 character long."
        elif key == "user_exist":
            self.__message = "User already exist."
        elif key == "SSN_Format":
            self.__message = "Enter a valid U.S. Social Security number in XXX-XX-XXXX format."
        elif key == "Mobile_Format":
            self.__message = "Enter a valid phone number"
        elif key == "skip_forgot":
            self.__message = "Use forgot password option then verify."
        elif key == "something_wrong":
            self.__message = "Something went wrong."
        elif key == "invalid_credential":
            self.__message = "Invalid credentials."
        elif key == "mob_not_verified":
            self.__message = "This mobile number is not verified."
        elif key == "email_not_verified":
            self.__message = "This Email Id is not verified."
        elif key == "generic_expired":
            if value:
                self.__message = "{0} has expired." .format(value)
        elif key == "otp_wrong":
            self.__message = "Invalid One Time Password (OTP)."
        elif key == "link_broken":
            self.__message = "Verification link is invalid or broken."
        elif key == "password_min":
            self.__message = "Password must be 8 character long."
        elif key == "not_find_generic":
            if value:
                self.__message = "We cannot find an account with that {0}." .format(value)
        elif key == "generic_digit":
            if value:
                self.__message = "{0} must be digit." .format(value)
        elif key == "generic_valid":
            if value:
                self.__message = "Enter a valid {0}." .format(value)
        elif key == "generic_provide":
            if value:
                self.__message = "Provide {0}." .format(value)
        elif key == "generic_email_mobile":
            if value:
                self.__message = "Your provided {0} has already been used. Please use another {0}." .format(value)
        elif key == "signup":
            self.__message = "Register your account to verify One Time Password (OTP)."
        elif key == "SSN_MinChar":
            self.__message = "Social security Number must be 11 digits long."
        elif key == 'ZipCodeMinChar':
            self.__message = "ZipCode must be 5 digits long."
        elif key == "Choice_Error":
            if value:
                self.__message = "{0} must be chosen from its choices" .format(value)
        elif key == "ValueError":
            self.__message = "Provided Data is not right. "

        elif key == "object_exists":
            if value:
                self.__message = "This {0} Object is already exist.Please fill another.".format(value)

        elif message is not None:
            self.__message = message

        data = {
            "success": False,
            "response": response,
            "message": self.__message
        }
        return (data, code)