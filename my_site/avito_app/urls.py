from .views import (UserProfileViewSet, CategoryListAPIView, UserProfileViewSet, UserProfileListAPIView, SubCategoryListAPIView,
                    ProductListAPIView, ProductDetailAPIView, ReviewViewSet, UserProfileUpdateAPIView,
                    CategoryDetailAPIView, SubCategoryDetailAPIView, RegisterView, CustomLoginView, LogoutView,
                    CartAPIView, CartItemViewSet, FavoriteItemViewSet, FavoriteAPIView)
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'review', ReviewViewSet, basename='review')


urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListAPIView. as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView. as_view(), name='product_detail'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileUpdateAPIView.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login', CustomLoginView.as_view(), name='user_login'),
    path('logout', LogoutView.as_view(), name='user_logout'),


path('cart/', CartAPIView.as_view(), name='cart_detail'),
path('cart_item/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart_item_list'),
path('cart_item/<int:pk>/', CartItemViewSet.as_view({'get': 'retriave', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='cart_item_detail'),


path('favorite/', FavoriteAPIView.as_view(), name='favorite_detail'),
path('favorite_item/', FavoriteItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite_item_list'),
path('favorite_item/<int:pk>', FavoriteItemViewSet.as_view({'get': 'retrieve','delete': 'destroy'}), name='favorite_item_detail')



]