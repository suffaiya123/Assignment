"""
Collections of classes imported from django rest framework to build api.
"""
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import (api_view,
                                       permission_classes,
                                       authentication_classes)
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


