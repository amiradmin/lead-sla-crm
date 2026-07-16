"""
URL configuration for the leads application.

This module registers API routes for lead management.

Routes are generated automatically by DRF router
from LeadViewSet.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.leads.views import LeadViewSet


# DRF router automatically creates RESTful routes.
router = DefaultRouter()

router.register(
    prefix="leads",
    viewset=LeadViewSet,
    basename="lead",
)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]
