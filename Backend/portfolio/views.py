from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User,Stock
from .serializers import UserSerializer
from rest_framework.decorators import api_view,permission_classes
import requests,random,json
from django.http import JsonResponse


class UserDetailView(APIView):
    def get(self, request, *args, **kwargs):
        # Assuming you want to get details of the currently logged-in user
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['POST'])
def get_stocks_by_risk(request):
    if request.method == 'POST':
        try:
            # Get the request body
            data = json.loads(request.body)
            requested_risk = data.get('risk')

            # Read data from the "stock.txt" file
            with open("D:\portfolio-project\mysite_root\portfolio\stock.txt", "r") as file:
                stocks_data = json.load(file)

            # Filter stocks based on the requested risk level
            matching_stocks = [stock for stock in stocks_data if stock.get('risk') == requested_risk]

            return JsonResponse(matching_stocks, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

