from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated
from .models import User,Stock,Portfolio,Asset
from .serializers import UserSerializer,PortfolioSerializer
from rest_framework.decorators import api_view,permission_classes
import random,json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings



class UserDetailView(APIView):
    def get(self, request, *args, **kwargs):
        # Assuming you want to get details of the currently logged-in user
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_stocks_by_risk(request):
    if request.method == 'POST':
        try:
            # Get the request body
            data = json.loads(request.body)
            requested_risk = data.get('risk')

            # Read data from the "stock.txt" file
            with open("C:/Users/omtan/OneDrive/Desktop/Niche/Niche2.0/Backend/portfolio/stock.txt", "r") as file:
                stocks_data = json.load(file)

            # Filter stocks based on the requested risk level
            matching_stocks = [stock for stock in stocks_data if stock.get('risk') == requested_risk]
            first_50=matching_stocks[:50]
            return JsonResponse(matching_stocks, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_portfolio(request):
    if request.method=='GET':
        user=request.user
        # username = request.data.get('username')
        # if not username:
        #     return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            portfolio = Portfolio.objects.get(user=user)
        except Portfolio.DoesNotExist:
            return Response({'error': 'Portfolio not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PortfolioDetail(generics.RetrieveAPIView):
    serializer_class = PortfolioSerializer
    
    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Portfolio.objects.filter(user=user)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user__username=self.kwargs['username'])
        return obj

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_stop_loss(request):
    if request.method == 'POST':
        stop_loss_level = request.data.get('stop_loss_level')
        if stop_loss_level is None:
            return Response({'error': 'Stop loss level is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stop_loss_level = float(stop_loss_level)
        except ValueError:
            return Response({'error': 'Invalid stop loss level'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username="admin")
        portfolio = Portfolio.objects.get(user=user)
        assets = Asset.objects.filter(portfolio=portfolio)
        for asset in assets:
            if asset.purchase_price > stop_loss_level:
                send_mail(
                    'Stop Loss Alert',
                    f'The price of {asset.name} in your portfolio has fallen below the stop-loss level.',
                    settings.EMAIL_HOST_USER,
                    [portfolio.user.email],
                )
            else:
                send_mail(
                    'Stop Loss Alert',
                    f'The price of {asset.name} in your portfolio has reaped rich dividends! Congratulations!!',
                    settings.EMAIL_HOST_USER,
                    [portfolio.user.email],
                )

        return Response({'message': 'Stop loss check completed. Email notifications sent if necessary.'})
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
