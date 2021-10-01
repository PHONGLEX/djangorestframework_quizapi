from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('psi', views.PsiViewSet)
router.register('air-temperature', views.AirTemperatureViewSet)

urlpatterns = [
    path('', include(router.urls))
]