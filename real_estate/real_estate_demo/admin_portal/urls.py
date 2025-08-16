from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='admin_dashboard'),
    path('properties/', views.AdminPropertyListView.as_view(), name='admin_properties'),
    path('properties/add/', views.AdminPropertyCreateView.as_view(), name='admin_property_add'),
    path('properties/<int:pk>/edit/', views.AdminPropertyUpdateView.as_view(), name='admin_property_edit'),
    path('inquiries/', views.AdminInquiryListView.as_view(), name='admin_inquiries'),
    path('analytics/', views.AnalyticsView.as_view(), name='admin_analytics'),
]