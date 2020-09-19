import datetime
from django.shortcuts import render
from users.signup import OTP
from users.validation import (MobileValidate,
                              NameValidate,
                              EmailValidate,
                              SSNValidate,
                              ZipCodeValidate,
                              StateValidate,
                              AddressValidate)
from users.models import Token, Users, TempUser
from ..rest_frameworks_imports import *
from users.error_handler.views import Error_Handler
from django.utils.timezone import now
from .serializers import UserDetailSerializer, ProfileImageSerializer, UserEditSerializer
from users.response_handler.views import ResponseWrapper
from ..identify_service import IdentifyService
from users.authentication.api_authentication import TokenAuthentication
from users.authentication.api_permission import IsAuthenticated, AllowAny
from users.verification import OTPSMSVerification, EmailVerification


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup_api(request):
    try:
        json_data = request.data
        action = json_data.get("action", None)
        if action == None:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST,
                                        message="Please provide action")
            return Response(data, code)
        identifyObj = IdentifyService(action)
        data, code = identifyObj.choose_service(json_data)
        return Response({"data": data}, status=code)
    except Exception as e:
        error = Error_Handler()
        data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=repr(e))
        return Response(data, code)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def users_details(request):
    try:
        token = (request.META['HTTP_AUTHORIZATION']).split()[-1]
        try:
            token_qs = Token.objects.get(key=token)
            user = token_qs.user

        except:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST)
            return Response(data, code)
        serializer = UserDetailSerializer(user).data
        response = ResponseWrapper()
        msg = "User Details"
        data, code = response.response(serializer, msg, status.HTTP_200_OK)
        return Response(data, code)
    except Exception as e:
        error = Error_Handler()
        data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=repr(e))
        return Response(data, code)


@api_view(['POST'])
def tempprofileimage(request):
    try:
        if 'multipart/form-data' not in request.content_type:
            return Response({'error': 'Content type is not sent in specified format.'},
                            status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer = ProfileImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = ResponseWrapper()
            msg = "Image uploaded successfully."
            data, code = response.response(serializer.data, msg, status.HTTP_200_OK)
            return Response(data, code)
        error = Error_Handler()
        data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST)
        return Response(data, code)
    except Exception as e:
        error = Error_Handler()
        data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=repr(e))
        return Response(data, code)


@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def user_profile_edit(request):
    try:
        token = (request.META['HTTP_AUTHORIZATION']).split()[-1]
        try:
            token_qs = Token.objects.get(key=token)
            user = token_qs.user

        except:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST)
            return Response(data, code)
        if 'multipart/form-data' not in request.content_type:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        message='Content type is not sent in specified format.')
            return Response(data, code)
        token_user_id = user.user_id

        # user_id = request.GET.get('user_id', None)
        # if user_id is None or user_id == '':
        #     error = Error_Handler()
        #     data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #                                 message='user is not registered. Please register the user')
        #     return Response(data, code)
        # print(user_id)
        # if not (user_id == token_user_id):
        #     error = Error_Handler()
        #     data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST,
        #                                 message='provide right authentication credential.')
        #     return Response(data, code)
        name = request.data.get('full_name', None)
        ssn = request.data.get('ssn', None)
        zipcode = request.data.get('zipcode', None)
        state = request.data.get('state', None)
        profile_image = request.data.get('profile_image', None)
        address = request.data.get('address', None)

        user = Users.objects.get(user_id=token_user_id)
        if user is None:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        message='User Does Not Exist')
            return Response(data, code)

        name_validateObj = NameValidate(name)
        name_validate = name_validateObj.name_validate()
        if name_validate != True:
            return name_validate

        ssn_validateObj = SSNValidate(ssn)
        ssn_validate = ssn_validateObj.ssn_validate()
        if ssn_validate != True:
            return ssn_validate

        zipcode_validateObj = ZipCodeValidate(zipcode)
        zipcode_validate = zipcode_validateObj.zipcode_validate()
        if zipcode_validate != True:
            return zipcode_validate

        state_validateObj = StateValidate(state)
        state_validate = state_validateObj.state_validate()
        if state_validate != True:
            return state_validate

        addressObj = AddressValidate(address)
        address_validate = addressObj.address_validate()
        if address_validate != True:
            return address_validate
        #
        # user = Users.objects.filter(user_id=user_id).filter(phone_number=mobile)
        # user_pass = user.password
        # print(user_pass)
        # user_dob = user.date_of_birth
        # user_tnc = user.termsconditions
        #
        # if not user.exists():
        #     tokenObj = OTP()
        #     token_mobile = tokenObj.token_generate()
        #     token_email = tokenObj.token_generate_email()
        #     temp_user = TempUser.objects.create(full_name=name, password=user_pass, phone_number=mobile,
        #                                         email=email, zipcode=zipcode, mobile_token=token_mobile, state=state,
        #                                         email_token=token_email, ssn=ssn, profile_image=profile_image,
        #                                         date_of_birth=user_dob,
        #                                         created_on_mobile=now(), created_on_email=now(),
        #                                         termsconditions=user_tnc, address=address)
        #     user.delete()
        #     OTPObj = OTPSMSVerification()
        #     minute = tokenObj.minute_validity()
        #     data_response = OTPObj.send_otp(mobile, token_mobile, minute)
        #
        #     response = ResponseWrapper()
        #     message = "A text with a One Time Password (OTP) has been sent to your mobile number."
        #     data, code = response.response({"data": data_response}, message,
        #                                    status.HTTP_201_CREATED)
        #     return Response(data, code)

        serializer = UserEditSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save(full_name=name, ssn=ssn, address=address, zipcode=zipcode, state=state,
                            profile_image=profile_image)
            response = ResponseWrapper()
            msg = "User Edit Details."
            data, code = response.response(serializer.data, msg, status.HTTP_200_OK)
            return Response(data, code)
        error = Error_Handler()
        data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST)
        return Response(data, code)
    except Exception as e:
        error = Error_Handler()
        data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=repr(e))
        return Response(data, code)
