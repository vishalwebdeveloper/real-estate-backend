from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer, RentProperty, BuyProperty

class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        required = ["full_name", "email", "password", "phone_number"]
        for field in required:
            if not data.get(field):
                raise serializers.ValidationError({field: "This field is required"})
        return data

    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        customer = Customer(**validated_data)
        customer.set_password(raw_password)   # hashes correctly once
        customer.save()
        return customer

    def update(self, instance, validated_data):
        # handle password update safely
        raw_password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if raw_password:
            instance.set_password(raw_password)
        instance.save()
        return instance



class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            customer = Customer.objects.get(email=data["email"])
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Email not found")

        if not customer.check_password(data["password"]):
            raise serializers.ValidationError("Incorrect password")

        data["customer"] = customer
        return data


class RentPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = RentProperty
        fields = "__all__"


class BuyPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyProperty
        fields = "__all__"
