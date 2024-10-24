from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from .models import *
from .forms import *
from .credentials import *

@api_view(['POST'])
def register_view(request):
    serializers = RegisterSerializer(data=request.data)

    if serializers.is_valid():
        user = serializers.save()
        return Response({'success': 'User registered successfully', 'user': RegisterSerializer(user).data})
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    serializers = LoginSerializer(data=request.data)
    if serializers.is_valid():
        user = serializers.validated_data['user']
        refresh = RefreshToken.for_user(user)

        refresh['username'] = user.username

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    serializers = LogoutSerilizer(data=request.data)

    if serializers.is_valid():
        refresh_token = serializers.validated_data['refresh']

        try:
            OutstandingToken.objects.filter(token=refresh_token).delete()
            return Response({'detail': 'User logged out'}, status=status.HTTP_205_RESET_CONTENT) 
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    print(request.data)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET']) # View to display product retrived from database
def product_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        serialiser = ProductSerializer(product, many=True)
        return Response(serialiser.data)
    
@api_view(['POST']) # View to create a new product and get stored to the database
def product_create(request):
    if request.method == 'POST':
        serialiser = ProductSerializer(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'GET']) # View to update an existing product
def product_update(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialiser = ProductSerializer(product)
        return Response(serialiser.data)
    
    if request.method == 'PUT':
        serialiser = ProductSerializer(product, data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET', 'DELETE'])
def product_delete(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serialiser = ProductSerializer(product)
    return Response(serialiser.data)

@api_view(['POST', 'GET'])
def mpesa_view(request, slug):
    try: 
        product = Product.objects.get(slug=slug)
    except  Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialiser = ProductSerializer(product)
        product_data = serialiser.data
        product_data['price'] = float(product_data['price'])
        return Response(product_data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        phone = request.data.get('phone')

        if not phone:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        amount = product.price

        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}

        payment_request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": float(amount),
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "PYMENT001",
            "TransactionDesc": "Product Payment"
        }

        response = requests.post(api_url, json=payment_request, headers=headers)
        
        # Print the response for debugging
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code == 200:
            # Payment initiated successfully
            return Response({"success": "Payment Initiated"}, status=status.HTTP_200_OK)
        else:
            # Handle payment failure or errors here
            return Response({"error": "Payment has failed"},status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)


