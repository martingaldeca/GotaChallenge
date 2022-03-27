from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_url_patterns = [
    # path('gotapi/', include('core.api.urls', 'core')),
    path('gotapi/login/', TokenObtainPairView.as_view(), name='login'),
    path('gotapi/refresh/', TokenRefreshView.as_view(), name='refresh'),
]

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('gotadmin/', admin.site.urls),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + api_url_patterns

if not settings.PRODUCTION:
    drf_spectacular_urls = [
        path('gotapi/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('gotapi/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('gotapi/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
    urlpatterns += drf_spectacular_urls
