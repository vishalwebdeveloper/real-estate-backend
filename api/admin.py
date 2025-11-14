from django.contrib import admin
from .models import Customer, RentProperty, BuyProperty

admin.site.index_template = "admin.html"

admin.site.site_header = "🏠 DwellPoint Admin"
admin.site.site_title = "Welcome to DwellPoint Portal"
admin.site.index_title = "DwellPoint Portal"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone_number", "created_at")
    search_fields = ("email", "full_name")


@admin.register(RentProperty)
class RentPropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "price", "is_approved")
    list_filter = ("is_approved", "city")
    search_fields = ("title",)

    actions = ["approve_properties"]

    def approve_properties(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected properties approved!")

    approve_properties.short_description = "Approve selected rent properties"


@admin.register(BuyProperty)
class BuyPropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "price", "owner_type", "is_approved")
    list_filter = ("is_approved", "city")
    search_fields = ("title",)

    actions = ["approve_buy_properties"]

    def approve_buy_properties(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected buy properties approved!")

    approve_buy_properties.short_description = "Approve selected buy properties"
