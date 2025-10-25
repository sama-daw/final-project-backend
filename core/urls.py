from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from shop.views import ProductViewSet, OrderCreateView, OrderDetailView
from .views import api_home


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')


urlpatterns = [
  
    path('', api_home, name='api-home'),
    
 
    path('admin/', admin.site.urls),
    
  
    path('api/', include(router.urls)),
    path('api/orders/', OrderCreateView.as_view(), name='order-create'),
    path('api/orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    
   
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
  
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
