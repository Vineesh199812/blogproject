"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from blogapi import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router=DefaultRouter()
router.register("api/v3/oxygen/mobiles",views.MobilesViewSetView,basename="mobiles")
router.register("api/v4/oxygen/mobiles",views.MobilesModelViewSetView,basename="modelmobiles")
router.register("api/v5/account/register",views.UserRegistrationView,basename="registration")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/oxygen/mobiles",views.MobileView.as_view()),
    path("api/v1/oxygen/mobiles/<int:id>",views.MobileDetailsView.as_view()),
    path("api/v2/oxygen/mobiles",views.MobileModelView.as_view()),
    path("api/v2/oxygen/mobiles/<int:id>",views.MobileDetailModelView.as_view()),
    path("accounts/token",obtain_auth_token),
]+router.urls
