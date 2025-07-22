from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer

@api_view(['POST'])
def register(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        customer, created = Customer.objects.update_or_create(
            telegram_id=serializer.validated_data['telegram_id'],
            defaults=serializer.validated_data
        )
        return Response(CustomerSerializer(customer).data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def menu(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return Response({
        'categories': CategorySerializer(categories, many=True).data,
        'products': ProductSerializer(products, many=True).data
    })

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response(OrderSerializer(order).data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def order_history(request):
    telegram_id = request.GET.get('user')
    customer = Customer.objects.filter(telegram_id=telegram_id).first()
    if not customer:
        return Response({'error': 'User not found'}, status=404)
    orders = Order.objects.filter(customer=customer)
    return Response(OrderSerializer(orders, many=True).data)
