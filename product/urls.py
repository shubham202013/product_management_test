from django.urls import path
from .views import CategoryListView, CategoryDetailView, UserRegisterView, ProductListView, ProductDetailView, ExportProductCSV
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [   
   path('register/', UserRegisterView.as_view(), name='register'),
   path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('category/', CategoryListView.as_view(), name='category-list'),
   path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('product/', ProductListView.as_view(), name='product-list'),
   path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
   path('product/export/csv/', ExportProductCSV.as_view(), name='export-product-csv')
]
