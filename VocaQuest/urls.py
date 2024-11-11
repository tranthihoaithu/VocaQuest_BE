from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="VocaQuest API",
        default_version='v1',
        description="APIs for VocaQuest",
        contact=openapi.Contact(email="tranhoaithu@gmail.com"),
        license=openapi.License(name="Trần Hoài Thu "),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)
urlpatterns = [
    path ('',include('learn_voca.urls')),
    path('admin/', admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]
