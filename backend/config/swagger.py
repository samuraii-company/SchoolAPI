from rest_framework import permissions
from django.urls import include, path, re_path
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Akib service API",
      default_version='v1',
      description="Leave me alone",
      terms_of_service="https://www.google.com/policies/terms/",
      license=openapi.License(name="MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
