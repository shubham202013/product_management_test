from django.shortcuts import render
from rest_framework import generics,views
from .models import Category, Product
from .serializers import CategorySerializer, registerUserSerializer, ProductSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

import pandas as pd
from django.http import HttpResponse
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from celery import shared_task
import os
import base64
from rest_framework.response import Response
# Create your views here.
AES_KEY = os.urandom(16) 

def encrypt_response(data):
    json_data = json.dumps(data).encode('utf-8')
    iv = os.urandom(12)  # 96-bit IV for AES-GCM
    aesgcm = AESGCM(AES_KEY)
    encrypt_data = aesgcm.encrypt(iv, json_data, None)
    
    return {
        'iv': base64.b64encode(iv).decode(),
        'data': base64.b64encode(encrypt_data).decode()
    }

class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = self.get_serializer(categories, many=True)
        
        # Encrypt the response data
        encrypted_data = encrypt_response(serializer.data)
        
        return Response(encrypted_data)
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class  UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = registerUserSerializer
    
    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     response = super().create(request, *args, **kwargs)
    #     response.data['message'] = 'User created successfully'
    #     return response
    
class ProductListView(generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ExportProductCSV(views.APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    
    
    def get(self, request):
        products = Product.objects.all().values('id', 'title', 'price', 'Category_id')
        products_df = pd.DataFrame(products)
        
        products_df.rename(columns={'Category_id': 'category'}, inplace=True)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        products_df.to_csv(path_or_buf=response, index=False)
        
        return response
    
class ImportProduct(views.APIView):
    
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]   
    
    def get(self, request):
        return render(request, 'import_product.html')
    
    def post(self, request):
        
        count = request.data.get('number_of_products')
        insert_product_task.delay(count)
        return render(request, 'import_product.html', {'message': f'{count} products are being inserted.'})
    
    
@shared_task
def insert_product_task(count):
    
    category = Category.objects.get(id=1)  # Assuming you have a category with ID 1
    
    for i in range(int(count)):
        product = Product(
            title=f'Product {i}',
            description='Description {i}',
            price=100.00,
            status='active',
            Category_id=category,  # Assuming you have a category with ID 1
        )
        product.save()
        
    return f'{count} products inserted successfully'