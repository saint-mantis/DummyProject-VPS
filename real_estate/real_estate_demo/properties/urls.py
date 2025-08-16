from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('property/<slug:slug>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('search/', views.PropertySearchView.as_view(), name='property_search'),
    path('contact/', views.contact_agent, name='contact_agent'),
    path('contact-form/', views.contact_form, name='contact_form'),
    path('api/favorites/add/', views.add_to_favorites, name='add_to_favorites'),
    path('api/favorites/remove/', views.remove_from_favorites, name='remove_from_favorites'),
]