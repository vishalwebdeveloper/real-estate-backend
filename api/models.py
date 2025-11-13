from django.db import models

from django.contrib.auth.hashers import make_password, check_password


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class RentProperty(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="rent_properties")
    title = models.CharField(max_length=255)
    
    property_type = models.CharField(max_length=100)
    sub_type = models.CharField(max_length=100)

    project_name = models.CharField(max_length=255)    # required
    super_buildup_area_sqft = models.FloatField()      # required
    carpet_area_sqft = models.FloatField()             # required
    owner_type = models.CharField(max_length=100)
    price = models.FloatField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    property_image = models.ImageField(upload_to="", null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.city})"


class BuyProperty(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="buy_properties")
    title = models.CharField(max_length=255)

    owner_type = models.CharField(max_length=100)
    property_type = models.CharField(max_length=100)
    sub_type = models.CharField(max_length=100)

    project_name = models.CharField(max_length=255)    # required
    super_buildup_area_sqft = models.FloatField()      # required
    carpet_area_sqft = models.FloatField()             # required

    price = models.FloatField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    property_image = models.ImageField(upload_to="", null=True, blank=True)
    
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.city})"
