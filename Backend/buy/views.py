from django.shortcuts import render
# from .models import Buystock
from portfolio.models import Portfolio,Stock,User,Asset
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal

#import razorpay
from django.conf import settings
from rest_framework.decorators import api_view,permission_classes
from django.utils import timezone
from django.http import JsonResponse
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buyStock(request):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body)
            stock_name = data['stock_name']
            quantity = data['quantity']
            user = request.user
            # user = User.objects.get(username="admin")
            with open("C:/Users/omtan/OneDrive/Desktop/Niche/Niche2.0/Backend/portfolio/stock.txt", "r") as file:
                stock_data = json.load(file)
                stock_object = next((stock for stock in stock_data if stock['name'] == stock_name), None)

            if not stock_object:
                return JsonResponse({'error': 'Stock not found'}, status=400)

            portfolio, created = Portfolio.objects.get_or_create(user=user)
            asset_allocation = json.loads(portfolio.asset_allocation) if portfolio.asset_allocation else []

            # Check if the asset exists in the asset allocation list
            asset = next((asset for asset in asset_allocation if asset['name'] == stock_name), None)
            if not asset:
                # Create a new asset object and append it to the asset allocation list
                asset1= Asset.objects.create(
                    name=stock_name,
                    quantity=quantity,
                    purchase_price=float(stock_object['price']),
                    purchase_date=timezone.now(),  # Assuming the purchase date is the current date/time
                    portfolio=portfolio
                )
                asset = {
                    'name': stock_name,
                    'quantity': quantity,
                    'purchase_price': stock_object['price'],
                    'purchase_date': timezone.now().isoformat(),  # Convert datetime to ISO format
                    'graph':stock_object['graph']
                }
                # Ensure asset_allocation is a list before attempting to append
                if not isinstance(asset_allocation, list):
                    asset_allocation = []
                asset_allocation.append(asset)
            else:
                # Update the quantity of the existing asset object
                asset1 = Asset.objects.get(name=stock_name, portfolio=portfolio)
                #asset['quantity'] += quantity
                asset_quantity = Decimal(asset['quantity'])  # Convert to Decimal
                asset_quantity += Decimal(quantity)  # Perform addition
                asset['quantity'] = str(asset_quantity)

                asset1.quantity = str(asset_quantity)
                asset1.save()


            # Update the value of the portfolio
            portfolio.value += float(stock_object['price']) * float(quantity)

            # Save the changes
            portfolio.asset_allocation = json.dumps(asset_allocation)
            portfolio.save()

            return JsonResponse({'message': 'Stock purchased successfully'}, status=200)
        except KeyError:
            return JsonResponse({'error': 'Invalid request data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)
