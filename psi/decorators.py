from rest_framework.response import Response
from rest_framework import status

from datetime import datetime


def validate_datetime(func):
    def search(self, request, *args, **kwargs):
        try:
            param = request.data
            if param.get('date_param') is not None:
                kwargs['param'] = {
                    'type': 'date',
                    'date': datetime.strptime(param.get('date_param'), '%Y-%m-%d')
                }
            elif param.get('datetime_param') is not None:
                kwargs['param'] = {
                    'type': 'datetime',
                    'datetime': datetime.strptime(param.get('datetime_param'), '%Y-%m-%d %H:%M:%S')
                }
            else:
                return Response({'error': "Please provide either date or datetime for filtering"}, status=status.HTTP_400_BAD_REQUEST)
            return func(self, request, *args, **kwargs)
        except Exception as e:
            return Response({'error': 'Invalid date or datetime format'}, status=status.HTTP_400_BAD_REQUEST)

    return search