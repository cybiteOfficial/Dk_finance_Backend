"""
URL configuration for Dev_Kripa_Finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', include('user_auth.urls')),
    path('api/v1/', include('leads.urls')),
    path('api/v1/',include('kyc.urls')),
    path('api/v1/', include('customer.urls')),
    path('api/v1/', include('applicants.urls')),
    path('api/v1/', include('phonepay.urls')),
    path('api/v1/', include('loan.urls')),
    path('api/v1/', include('collateral_details.urls')),
    path('api/v1/', include('customer_application.urls')),
    path('api/v1/', include('print_document.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)