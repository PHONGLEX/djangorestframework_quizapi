from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from django.http import JsonResponse
from django.db.models import Q

from .models import Psi, AirTemperature
from .serializers import PsiSerializer, AirTemperatureSerializer, SearchDateSerializer
from .decorators import validate_datetime


class PsiPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'count'
    max_page_size = 2000
    page_query_param = 'p'


class AirTemperaturePagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'count'
    max_page_size = 2000
    page_query_param = 'p'


class PsiViewSet(ModelViewSet):
    serializer_class = PsiSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PsiPagination
    queryset = Psi.objects.all()

    @swagger_auto_schema(request_body=SearchDateSerializer)
    @action(detail=False, methods=['POST'])
    @validate_datetime
    def search(self, request, *args, **kwargs):
        param = kwargs.get('param')

        if param['type'] == 'date':
            data = Psi.objects.filter(Q(updated_timestamp__date=param['date']))
        elif param['type'] == 'datetime':
            data = Psi.objects.filter(Q(updated_timestamp=param['datetime']))

        if not data.exists():
            data = Psi.objects.filter(Q(updated_timestamp__date=Psi.objects.latest('updated_timestamp').updated_timestamp.date()))
        
        serializer = self.serializer_class(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
class AirTemperatureViewSet(ModelViewSet):
    serializer_class = AirTemperatureSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = AirTemperaturePagination
    queryset = AirTemperature.objects.all()

    @swagger_auto_schema(request_body=SearchDateSerializer)
    @action(detail=False, methods=['POST'])
    @validate_datetime
    def search(self, request, *args, **kwargs):
        param = kwargs.get('param')

        if param['type'] == 'date':
            data = AirTemperature.objects.filter(Q(timestamp__date=param['date']))
        elif param['type'] == 'datetime':
            data = AirTemperature.objects.filter(Q(timestamp=param['datetime']))

        if not data.exists():
            data = data | AirTemperature.objects.filter(
                Q(timestamp__date=AirTemperature.objects.latest('timestamp').timestamp.date()))
        
        serializer = self.serializer_class(list(data), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)