"""toolbox_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('split/', include('excel_split.urls')),
    path('merge/', include('excel_merge.urls')),
    path('rewards/', include('sales_rewards_generator.urls')),
    path('mail/', include('mass_email.urls')),
    path('', include('main.urls')),
    path('billing/', include('wholesaler_billing.urls')),
    path("admin/", admin.site.urls),
]
