from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Real Estate API",
        default_version="v1",
        description="API documentation for Rent & Buy Property System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ Your API urls
    path("", include("api.urls")),

    # ✅ Swagger UI
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # ✅ Redoc UI (optional)
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
