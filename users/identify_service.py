from users.signup import SignUp, OTP, Password, SignIn


class IdentifyService():
    __action = None

    def __init__(self, action):
        self.__action = action

    def choose_service(self, data):
        if self.__action == "signup":
            signUpObj = SignUp(data)
            setdata = signUpObj.signup()
            return setdata
        #
        # elif self.__action == "resend_link":
        #     otpObj = OTP(data)
        #     data = otpObj.new_user_resend_link()
        #     return data

        elif self.__action == "otp_verify":
            otpObj = OTP(data)
            data = otpObj.new_user_otp_verify()
            return data
        elif self.__action == "resend_otp":
            tokenObj = OTP(data)
            data = tokenObj.new_user_resend_otp()
            return data

        elif self.__action == "reset_password":
            passwordObj = Password(data)
            data = passwordObj.reset_password_token_generate()
            return data

        elif self.__action == "reset_password_token_verify":
            tokenObj = OTP(data)
            data = tokenObj.reset_password_token_verify()
            return data

        elif self.__action == "reset_password_changed":
            passwordObj = Password(data)
            data = passwordObj.reset_password_changed()
            return data

        elif self.__action == "signin":
            signInObj = SignIn(data)
            setdata = signInObj.signin()
            return setdata
