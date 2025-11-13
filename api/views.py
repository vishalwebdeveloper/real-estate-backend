from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer, RentProperty, BuyProperty
from .serializers import (
    CustomerRegisterSerializer,
    CustomerLoginSerializer,
    RentPropertySerializer,
    BuyPropertySerializer,
)


# ✅ REGISTER API
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer
    permission_classes = [AllowAny]


# ✅ LOGIN API WITH JWT TOKENS
class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = serializer.validated_data["customer"]

        refresh = RefreshToken.for_user(customer)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "customer": {
                "id": customer.id,
                "full_name": customer.full_name,
                "email": customer.email,
                "phone_number": customer.phone_number,
            }
        })
        

# ✅ RENT PROPERTY — ONLY LOGGED-IN USERS CAN ADD
class RentPropertyViewSet(viewsets.ModelViewSet):
    queryset = RentProperty.objects.all()
    serializer_class = RentPropertySerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    @action(detail=True, methods=["patch"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        obj = self.get_object()
        obj.is_approved = True
        obj.save()
        return Response({"message": "Rent property approved!"})


# ✅ BUY PROPERTY — ONLY LOGGED-IN USERS CAN ADD
class BuyPropertyViewSet(viewsets.ModelViewSet):
    queryset = BuyProperty.objects.all()
    serializer_class = BuyPropertySerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["patch"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        obj = self.get_object()
        obj.is_approved = True
        obj.save()
        return Response({"message": "Buy property approved!"})


# ✅ Public APIs for frontend
class ApprovedRentPropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RentProperty.objects.filter(is_approved=True)
    serializer_class = RentPropertySerializer
    permission_classes = [AllowAny]


class ApprovedBuyPropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BuyProperty.objects.filter(is_approved=True)
    serializer_class = BuyPropertySerializer
    permission_classes = [AllowAny]
