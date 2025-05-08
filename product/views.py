from django.shortcuts import render
from rest_framework import generics,views
from .models import Category, Product
from .serializers import CategorySerializer, registerUserSerializer, ProductSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import pandas as pd
from django.http import HttpResponse
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Create your views here.

def encrypt_response(data):
    json_data = json.dumps(data).encode()

class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
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