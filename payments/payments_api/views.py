from users.models import Users,Token
from users.rest_frameworks_imports import *
from users.error_handler.views import Error_Handler
from django.utils.crypto import get_random_string
from users.response_handler.views import ResponseWrapper
from users.authentication.api_authentication import TokenAuthentication
from users.authentication.api_permission import IsAuthenticated, AllowAny
from payments.models import Customer
from .serializers import CustomerSerializer,OrderSerializer


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def customer_id_api(request):
    try:
        token = (request.META['HTTP_AUTHORIZATION']).split()[-1]
        try:
            token_qs = Token.objects.get(key=token)
            user = token_qs.user

        except:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST)
            return Response(data, code)
        token_user_id = user.user_id

        user = Users.objects.get(user_id=token_user_id)
        user_id = user.user_id

        if user_id is "":
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        message='User Does Not Exist')
            return Response(data, code)

        customer = Customer.objects.create(customer_id=get_random_string(length=8), associated_user=user)
        return Response({'customer_id': customer.customer_id}, status=status.HTTP_201_CREATED)

    except Exception as e:
        error = Error_Handler()
        data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=repr(e))
        return Response(data, code)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def transaction_api(request):
    try:
        token = (request.META['HTTP_AUTHORIZATION']).split()[-1]
        try:
            token_qs = Token.objects.get(key=token)
            user = token_qs.user
        except:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST)
            return Response(data, code)
        token_user_id = user.user_id

        user = Users.objects.get(user_id=token_user_id)

        if user is "" or user is None:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        message='User Does Not Exist')
            return Response(data, code)

        if 'application/json' not in request.content_type:
            error = Error_Handler()
            data, code = error.response(key="not", response={}, code=status.HTTP_400_BAD_REQUEST)
            return Response(data, code)

        data = request.data
        order_no = get_random_string(length=8)
        customer_id = Customer.objects.get(associated_user=user)
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save(customer_id=customer_id,  order_no=order_no)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    except Exception as e:
        error = Error_Handler()
        data, code = error.response(key="not", response={}, code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=repr(e))
        return Response(data, code)