from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User,Stock
from rest_framework.decorators import api_view,permission_classes
import random,json
from django.http import JsonResponse
from rest_framework import serializers
from .models import User,Portfolio,Asset,Stock,Alert
# from base.models import User
from rest_framework.serializers import ModelSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        
# class PortfolioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Portfolio
#         fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    asset_allocation = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = '__all__'

    def get_asset_allocation(self, obj):
        asset_allocation_data = obj.asset_allocation
        if asset_allocation_data:
            return json.loads(asset_allocation_data)
        return []

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

# class AlertSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Alert
#         fields = '__all__'