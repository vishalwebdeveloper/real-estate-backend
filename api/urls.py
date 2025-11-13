from django.urls import path, include
from rest_framework import routers 
from .views import *
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register("register", RegisterViewSet, basename="register")
router.register("login", LoginViewSet, basename="login")
router.register("rent-properties", RentPropertyViewSet, basename="rentproperty")
router.register("buy-properties", BuyPropertyViewSet, basename="buyproperty")

# ✅ Public Approved APIs
router.register("approved-rent-properties", ApprovedRentPropertyViewSet, basename="approved-rent")
router.register("approved-buy-properties", ApprovedBuyPropertyViewSet, basename="approved-buy")

urlpatterns = [
    path("", include(router.urls)),
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    