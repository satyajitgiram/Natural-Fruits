"""fruit_trading URL Configuration

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
from django.urls import path, include
from app import urls
from app.views import home, dashboard, pricing, payment, handlerequest, transactions, update_profile_photo, profile


urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('pricing/', pricing, name='pricing'),
    path('transactions/', transactions, name='transactions'),
    path('profile/', profile, name='profile'),
    path('update-profile-photo/', update_profile_photo, name='update_profile_photo'),

    # Payment APIs
    path('payment/', payment, name = 'payment'),
    path('handlerequest/', handlerequest, name = 'handlerequest'),
    

]
