from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views

# Docs
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API for SmartSocial Hackathon",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    # Docs
    # path(
    #    "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    # ),
    # Custom
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/sandbox/", include("apps.sandbox.urls")),
]

swagger_patterns = [
    path(
        "api/v1/swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/v1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

if settings.DEBUG:
    urlpatterns += swagger_patterns
